from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User


def validate_image(image):
    file_size = image.file.size
    limit_kb = 512
    if file_size > limit_kb * 1024:
        raise ValidationError("Max size of file is %s KB" % limit_kb)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to='user_profile',
                               validators=[validate_image, FileExtensionValidator(['jpg', 'png', 'svg', 'jpeg'])])

    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        else:
            if self.nick_name == "":
                return 'https://icotar.com/initials/' + self.user.username + '.svg'
            else:
                return 'https://icotar.com/initials/' + self.nick_name + '.svg'


class Category(models.Model):
    name = models.CharField(max_length=20)
    

class Store(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    
    
class Goods(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    price = models.IntegerField(blank=False)
    publish = models.BooleanField(default=False, blank=False)
    
    
class GoodsImage(models.Model):
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    url = models.URLField(blank=False)
    
    
class Ad(models.Model):
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)


class Cart(models.Model):
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    consumer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False, default=1)
    current_price = models.IntegerField(blank=False)
    