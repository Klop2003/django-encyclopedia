from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    founded = models.PositiveIntegerField()
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "country", "founded"],
                name="uniq_brand_name_country_founded"
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.country})"
