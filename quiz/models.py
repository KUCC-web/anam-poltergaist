from django.db import models


class Store(models.Model):
    name = models.CharField(max_length=100, null=False)
    score = models.IntegerField(default=0, null=False)
    image_url = models.CharField(max_length=1000, null=False)

    def __gt__(self, other):
        return self.pk > other

    def __ge__(self, other):
        return self.pk >= other

    def __lt__(self, other):
        return self.pk < other

    def __le__(self, other):
        return self.pk <= other

    def __eq__(self, other):
        return self.pk == other
