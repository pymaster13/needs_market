from django.db import models


class Code(models.Model):
    username = models.CharField(max_length = 12)
    code = models.CharField(max_length=4)
    created = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = "Код"
        verbose_name_plural = "Коды"

    def __str__(self):
        return "{} - {}".format(self.username, self.code)
