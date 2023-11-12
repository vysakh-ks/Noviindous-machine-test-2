from django.db import models

# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=100,null=True)
    amount = models.FloatField(null=True)
    amount_text = models.TextField(null=True)
    subtitle = models.CharField(max_length=100,null=True)
    description = models.TextField(null=True,default="join immediately")
    status = models.BooleanField(default=True,null=True)
    image = models.ImageField(upload_to='images',null=True)

    def __str__(self):
        return self.title
