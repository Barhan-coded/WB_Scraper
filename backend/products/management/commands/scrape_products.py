# import json
# import requests
from django.core.management.base import BaseCommand
from products.models import Product
from requests import Session, exceptions


class Command(BaseCommand):
    help = 'Парсит товары Wildberries через JSON‑API по запросу и сохраняет в БД'

    def add_arguments(self, parser):
        parser.add_argument(
            '--query', '-q',
            required=True,
            help='Поисковый запрос или категория на Wildberries'
        )
        parser.add_argument(
            '--pages', '-p',
            type=int,
            default=1,
            help='Сколько страниц выдачи JSON запрашивать (по умолчанию 1)'
        )

    def handle(self, *args, **opts):
        query = opts['query']
        pages = opts['pages']

        session = Session()
        session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "ru-RU,ru;q=0.9",
            "Referer": "https://www.wildberries.ru/",
        })

        try:
            session.get("https://www.wildberries.ru/", timeout=5)
        except exceptions.RequestException as e:
            self.stderr.write(f'Не удалось получить куки: {e}')
            return

        products_processed = 0

        # 2) Перебираем страницы JSON‑API
        for page in range(1, pages + 1):
            # Формируем URL JSON‑API вместо HTML‑страницы
            url = (
                "https://search.wb.ru/exactmatch/ru/common/v4/search"
                f"?appType=1&curr=rub&dest=-1257786"
                f"&page={page}&query={'%20'.join(query.split())}"
                "&resultset=catalog&sort=popular&spp=24"
            )

            try:
                resp = session.get(url, timeout=10)
                resp.raise_for_status()
            except exceptions.RequestException as e:
                self.stderr.write(f'Ошибка запроса JSON‑API (страница {page}): {e}')
                continue

            data = resp.json()  # получаем чистый dict из JSON

            # 3) В JSON‑ответе список товаров лежит в data["data"]["products"]
            products = data.get("data", {}).get("products", [])
            if not products:
                self.stderr.write(f'На странице {page} товаров не найдено или структура изменилась')
                continue

            # 4) Пробегаем по каждому товару и сохраняем в БД
            for item in products:
                nmId = item.get("id")
                name = item.get("name", "").strip()
                # ценники приходят в копейках, делим на 100
                price = item.get("priceU", 0) / 100
                discounted = item.get("salePriceU", 0) / 100 or None
                rating = item.get("rating")
                reviews = item.get("feedbacks", 0)

                Product.objects.update_or_create(
                    # лучше по уникальному id, а не по имени
                    defaults={
                        'name': name,
                        'price': price,
                        'discounted_price': discounted,
                        'rating': rating,
                        'review_count': reviews,
                    },
                    # если в модели есть поле nmId, то:
                    # nmId=nmId
                    # иначе временно используем name
                    name=name
                )
                products_processed += 1

        self.stdout.write(self.style.SUCCESS(
            f'Успешно обработано товаров: {products_processed}'
        ))
