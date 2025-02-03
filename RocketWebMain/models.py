from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class DiscordUserManager(BaseUserManager):
    def create_user(self, discord_id, username, email, password=None, **extra_fields):
        """Создаёт обычного пользователя."""
        if not discord_id:
            raise ValueError("Discord ID is required")
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(discord_id=discord_id, username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, discord_id, username, email, password=None, **extra_fields):
        """Создаёт суперпользователя."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(discord_id, username, email, password, **extra_fields)


class Status(models.Model):
    """Модель статуса пользователя."""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class DiscordUser(AbstractUser):
    """Кастомная модель пользователя."""
    # Роли сотрудников
    ROLE_CHOICES = [
        ('team_lead', 'Тимлид'),
        ('teacher', 'Педагог'),
        ('product', 'Продукт'),
        ('smm', 'SMM'),
        ('sales', 'Sales'),
        ('hr', 'HR'),
    ]

    # Поля модели
    discord_id = models.CharField(max_length=50, unique=True)
    avatar_url = models.URLField(blank=True, null=True)

    # Поле статусов (многие ко многим)
    statuses = models.ManyToManyField(Status, blank=True)

    # Поле ролей сотрудников (множество ролей)
    roles = models.JSONField(default=list, blank=True)

    # Переопределяем менеджер
    objects = DiscordUserManager()

    # Переопределяем поля аутентификации
    USERNAME_FIELD = 'discord_id'
    REQUIRED_FIELDS = ['username', 'email']

    def __str__(self):
        return f"{self.username} ({', '.join([status.name for status in self.statuses.all()])})"

    # Методы управления статусами
    def add_status(self, status_name):
        """Добавить статус пользователю."""
        status, _ = Status.objects.get_or_create(name=status_name)
        self.statuses.add(status)

    def remove_status(self, status_name):
        """Удалить статус у пользователя."""
        status = Status.objects.filter(name=status_name).first()
        if status:
            self.statuses.remove(status)

    # Методы управления ролями
    def add_role(self, role):
        """Добавить роль сотруднику."""
        if role not in dict(self.ROLE_CHOICES):
            raise ValueError("Invalid role")
        if role not in self.roles:
            self.roles.append(role)
            self.save()

    def remove_role(self, role):
        """Удалить роль у сотрудника."""
        if role in self.roles:
            self.roles.remove(role)
            self.save()
