from django.contrib.auth.models import AbstractUser
from django.db import models

from datetime import datetime


class User(AbstractUser):
    ...


class Item(models.Model):
    STATUS_CHOICES = (
        ('open', 'open'),
        ('in progress', 'in progress'),
        ('done', 'done'),
        ('to do', 'to do'),
        ('in review', 'in review'),
        ('cancelled', 'cancelled'),
        ('blocked', 'blocked'),
    )
    CATEGORY_CHOICES = (
        ('bug', 'bug'),
        ('epic', 'epic'),
        ('improvement', 'improvement'),
        ('new feature', 'new feature'),
        ('story', 'story'),
        ('task', 'task'),
    )

    title = models.CharField(max_length=200)
    text = models.TextField()
    status = models.CharField(
        max_length=11,
        choices=STATUS_CHOICES,
        default='open'
    )
    category = models.CharField(
        max_length=11,
        choices=CATEGORY_CHOICES,
        default='development'
    )
    due_date = models.DateTimeField(blank=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_items')
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_items',
        default=creator,)

    def __str__(self):
        return self.title