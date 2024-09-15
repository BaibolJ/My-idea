from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

# __________________________________________________________
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_supplier = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # Для базовой реализации возвращаем True, если пользователь администратор
        return self.is_staff

    def has_module_perms(self, app_label):
        # Для базовой реализации возвращаем True, если пользователь администратор
        return self.is_staff

# _____________________________________________________________


class Objects(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Variety(models.Model):
    title = models.CharField(max_length=123)
    img = models.ImageField(upload_to='media/img_product')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_this = models.ForeignKey(Objects, on_delete=models.CASCADE)
    description = models.TextField()
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.title


# class Product(models.Model):
#     title = models.CharField(max_length=123)
#     img = models.FileField(upload_to='media/img_product')
#     price = models.PositiveIntegerField()
#     variety = models.ForeignKey(Variety, on_delete=models.CASCADE)
#     stock = models.PositiveIntegerField()
#
#     def __str__(self):
#         return self.title


class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Variety, on_delete=models.CASCADE)
    kilogram = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Рассчитываем общую стоимость заказа
        self.total_price = self.product.price * self.kilogram

        # Уменьшаем количество на складе
        if self.product.stock >= self.kilogram:
            self.product.stock -= self.kilogram
            self.product.save()  # Сохраняем изменения в продукте
        else:
            raise ValueError("Недостаточно товара на складе")

        super().save(*args, **kwargs)

    def __str__(self):
        return f'Order {self.product} by {self.customer.name}'


# class Delivery(models.Model):
#     order = models.OneToOneField(Order, on_delete=models.CASCADE)
#     delivery_address = models.CharField(max_length=200)
#     delivery_price = models.DecimalField(max_digits=10, decimal_places=2)
#     is_active = models.BooleanField(default=True)
#
#     def __str__(self):
#         return f'Delivery {self.id} for order {self.order.id}'
