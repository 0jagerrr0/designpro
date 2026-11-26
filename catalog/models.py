from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название категории'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class DesignRequest(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('accepted', 'Принято в работу'),
        ('completed', 'Выполнено'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='design_requests',
        verbose_name='Пользователь'
    )

    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )

    description = models.TextField(
        verbose_name='Описание'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='requests',
        verbose_name='Категория'
    )

    room_image = models.ImageField(
        upload_to='requests/',
        verbose_name='Фото помещения или план'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус'
    )

    admin_comment = models.TextField(
        blank=True,
        verbose_name='Комментарий администратора'
    )

    design_image = models.ImageField(
        upload_to='designs/',
        blank=True,
        null=True,
        verbose_name='Готовый дизайн'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']
