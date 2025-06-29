from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=512)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True
    )
    rating = models.DecimalField(
        max_digits=3, decimal_places=2,
        null=True, blank=True
    )
    review_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name
