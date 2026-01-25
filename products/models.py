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
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE)
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
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