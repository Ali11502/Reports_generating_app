from django.db import models

# Create your models here.
class Products(models.Model):
    name=models.CharField(max_length=200)
    image=models.ImageField(upload_to='products',default='no_picture.jpeg')
    price=models.FloatField(help_text='in PKR')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}-{self.created.strftime('%d/%m/%Y')}"