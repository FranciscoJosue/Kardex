from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

class ProductColor(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    
class ProductSize(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(ProductColor)
    size = models.ForeignKey(ProductSize)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'color', 'size'], 
                name='unique_product_variant')
        ]
    def __str__(self):
        return f"{self.product.name} - {self.color.name} - {self.size.name}"
    
class ProductEan(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='eans')
    ean = models.CharField(max_length=13, unique=True, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.ean:
            self.ean = self.ean.strip()
            if self.ean == '':
                self.ean = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.ean or ''


class PriceType(models.TextChoices):
    preco = 'P', 'Preço'
    custo = 'C', 'Custo'


class ProductPrice(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='prices')
    price_type = models.CharField(max_length=1, choices=PriceType.choices)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    update_at = models.DateTimeField(auto_now=True)