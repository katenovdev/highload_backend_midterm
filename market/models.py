from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        """Создать и вернуть пользователя."""
        if not login:
            raise ValueError('The Login field must be set')
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None, **extra_fields):
        """Создать и вернуть суперпользователя."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(login, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя."""
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('customer', 'Customer'),
    )

    login = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['role']  

    def __str__(self):
        return self.login


class Category(models.Model):
    """Модель категории."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель продукта."""
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.name


class Order(models.Model):
    """Модель заказа."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['order_date']),
        ]


class OrderStatus(models.Model):
    """Модель статуса заказа."""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='status')
    status = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.status
