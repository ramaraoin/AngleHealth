from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=10, blank=False, unique=True, help_text='Product name')
    price = models.PositiveIntegerField(blank=False, help_text="Product price in cents")
    start_date = models.DateField(help_text="Product start date")

    class Meta:
        managed = True
        db_table = 'Product'
        verbose_name_plural = 'Products'
        verbose_name = 'Product'
        ordering = ['name']

    def __str__(self):
        return self.name
