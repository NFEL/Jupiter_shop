from django.db import models


class Address(models.Model):
    city = models.CharField(max_length=30)
    detail = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.city
