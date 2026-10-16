from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'طالب'),
        ('supervisor', 'مشرف / دكتور'),
        ('admin', 'مدير النظام'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student',
        verbose_name='نوع الحساب'
    )
    academic_id = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        verbose_name='الرقم الجامعي / الوظيفي'
    )
    department = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name='القسم / الكلية'
    )
    avatar = models.ImageField(
        upload_to='avatars/', 
        blank=True, 
        null=True, 
        verbose_name='الصورة الشخصية'
    )

    @property
    def is_student(self):
        return self.role == 'student'

    @property
    def is_supervisor(self):
        return self.role == 'supervisor'

    @property
    def is_admin_user(self):
        return self.role == 'admin' or self.is_superuser

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
