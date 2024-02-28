from django.db import models

# Create your models here.

class Proxy(models.Model):
    ip = models.CharField(max_length=15)
    port = models.IntegerField()
    protocol = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
    uptime = models.CharField(max_length=10)

    class Meta:
        db_table = "proxy"
        app_label = 'proxy'
        managed = True

    def __str__(self):
        return f"<{self.__class__.__name__} > IP: {self.ip} | Port: {self.port}"





