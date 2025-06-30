**WB Scraper** — это одностраничное веб‑приложение, состоящее из бэкенда на Django и фронтенда на Vue 3 с Vite, которое позволяет:

* Парсить товары с сайта Wildberries по любому запросу (к примеру, «смартфон», «наушники» и т. д.)
* Сохранять информацию о товарах (название, цену, цену со скидкой, рейтинг, число отзывов) в базе данных (SQLite или PostgreSQL)
* Просматривать и фильтровать товары через REST‑API (`/api/products/`) по цене, рейтингу и числу отзывов
* Отображать таблицу товаров с динамическими фильтрами и сортировкой
* Строить интерактивные графики: гистограмму распределения цен и линейный график «скидка vs рейтинг»

---

## Возможности

* **Парсинг данных**

  * CLI‑команда `python manage.py scrape_products --query "<ваш запрос>" --pages <N>`
  * Использует внутренний JSON‑API Wildberries для быстрого и надёжного сбора данных

* **REST‑API**

  * Эндпоинт `GET /api/products/`
  * Параметры фильтрации: `min_price`, `max_price`, `min_rating`, `min_reviews`
  * Пример:

    ```
    GET /api/products/?min_price=5000&min_rating=4
    ```

* **Веб‑интерфейс на Vue 3**

  * Таблица товаров с клиентской сортировкой и серверной фильтрацией
  * Слайдер для диапазона цен, поля для минимального рейтинга и отзывов
  * Графики на базе Chart.js: распределение цен и зависимость скидки от рейтинга

---

## Технологии

* **Бэкенд**: Django, Django REST Framework, django‑filter, BeautifulSoup/requests или JSON‑API Wildberries
* **База данных**: SQLite (по умолчанию) или PostgreSQL
* **Фронтенд**: Vue 3, Vite, Axios, vue‑chartjs, Chart.js
* **Упаковка и сборка**: npm, Vite

---

## Установка и запуск

### 1. Клонирование и настройка бэкенда

```bash
git clone https://github.com/ВашUsername/WB_Scraper.git
cd WB_Scraper/backend

# создаём виртуальное окружение и устанавливаем зависимости
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

# создаём миграции и БД
python manage.py makemigrations
python manage.py migrate
```

### 2. Парсинг товаров

```bash
# по умолчанию парсится первая страница JSON‑API
python manage.py scrape_products --query "смартфон" --pages 3
```

### 3. Запуск сервера API

```bash
python manage.py runserver
# API будет доступен по адресу http://127.0.0.1:8000/api/products/
```

### 4. Настройка и запуск фронтенда

```bash
cd ../frontend
npm install
npm run dev
```

* Откройте в браузере [http://localhost:5173/](http://localhost:5173/)

---

## Примеры использования

* **Получить все товары дороже 5000 ₽ и с рейтингом от 4**

  ```
  GET http://127.0.0.1:8000/api/products/?min_price=5000&min_rating=4
  ```
* **Фильтрация и сортировка**
  На UI задайте диапазон цен, минимальный рейтинг/число отзывов — таблица и графики обновятся автоматически.

---

## Структура репозитория

```
WB_Scraper/
├── backend/
│   ├── manage.py
│   ├── wb_scraper/       # настройки Django
│   └── products/         # приложение для парсинга и API
├── frontend/
│   ├── index.html
│   ├── src/
│   │   ├── main.js       # инициализация Vue
│   │   ├── App.vue
│   │   └── components/   # ProductTable, PriceHistogram, DiscountRatingChart
│   └── vite.config.js
└── README.md             # этот файл
```

---

## Вклад в проект

1. Задачи (issues) и pull‑requests приветствуются
2. Пишите подробные описания изменений
3. Соблюдайте стиль кода и оформляйте коммиты по шаблону «<тип>: <краткое описание>»

---

## Лицензия

MIT © 2025 Ваше Имя
Разрешается свободно использовать, копировать и модифицировать данный проект.
