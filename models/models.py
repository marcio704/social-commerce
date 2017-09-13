from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Vendor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name


class Brand(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.name


class Store(models.Model):
    vendor = models.ForeignKey(Vendor, null=False, blank=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=False)

    def __str__(self):
        return "{0} (Owned by: {1})".format(self.name, self.vendor.user.first_name)


class Product(TimeStampedModel):
    brand = models.ForeignKey(Brand, null=False, blank=False, on_delete=models.CASCADE, related_name="products")
    store = models.ForeignKey(Store, null=False, blank=False, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    photo = models.ImageField(null=False, blank=False)
    url = models.URLField(null=False, blank=False)

    def __str__(self):
        return "{0} - {1} - {2}".format(self.name, self.brand.name, self.store.name)


class Post(TimeStampedModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False, on_delete=models.CASCADE)
    description = models.TextField(null=False, blank=False)

    def __str__(self):
        return "{0} --> {1}".format(self.author.first_name, self.id)


class Clooset(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False, on_delete=models.CASCADE,
                             related_name="user_cloosets")
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE,
                                related_name="product_cloosets")

    def __str__(self):
        return "{0} --> {1}".format(self.user.first_name, self.product.name)

    class Meta:
        unique_together = (("user", "product"), )
