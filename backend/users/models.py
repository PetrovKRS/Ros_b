from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator

class ManagerTeamManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class ManagerTeam(AbstractBaseUser):
    """ Модель менеджера. """
    email = models.EmailField(
        unique=True,
        verbose_name='E-mail'
    )
    first_name = models.CharField(max_length=50, verbose_name='Имя')  # Добавляем поле first_name
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')  # Добавляем поле last_name
    password = models.CharField(
        max_length=100,
        verbose_name='Пароль',
        validators=(RegexValidator(
            regex=r'^.{4,}$',
            message='Пароль должен быть не менее 4-х символов'
        ),)
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = ManagerTeamManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Добавляем обязательные поля

    class Meta:
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджеры'

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        """
        Проверка разрешений для пользователя.
        :param perm: Разрешение (строка в формате 'app_label.permission_code')
        :param obj: Объект, на который проверяется разрешение (необязательный)
        :return: True, если пользователь имеет разрешение, иначе False.
        """
        # Проверяем, является ли пользователь суперпользователем
        if self.is_superuser:
            return True
        
        # Логика проверки разрешений
        # Например, можно использовать атрибуты или группы пользователя для проверки
        # В качестве примера можно сделать следующее:
        # return perm in self.get_user_permissions()  # Если у вас есть метод, который возвращает разрешения
        return False  # Измените логику по мере необходимости

    def has_module_perms(self, app_label):
        """
        Проверка доступа к модулю (приложению).
        :param app_label: Имя приложения (строка)
        :return: True, если пользователь имеет доступ к модулю, иначе False.
        """
        # Проверяем, является ли пользователь суперпользователем или администратором
        return self.is_superuser
