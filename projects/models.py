from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='اسم التصنيف')
    slug = models.SlugField(max_length=120, unique=True, allow_unicode=True, verbose_name='المعرّف اللطيف (Slug)')
    description = models.TextField(blank=True, null=True, verbose_name='الوصف')

    class Meta:
        verbose_name = 'تصنيف'
        verbose_name_plural = 'التصنيفات'

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = (
        ('Draft', 'مسودة'),
        ('Under Review', 'قيد المراجعة'),
        ('Needs Changes', 'يحتاج إلى تعديلات'),
        ('Approved', 'معتمد للنشر'),
    )

    title = models.CharField(max_length=220, verbose_name='عنوان المشروع')
    summary = models.TextField(verbose_name='ملخص تنفيذي')
    problem_statement = models.TextField(blank=True, null=True, verbose_name='المشكلة التي يعالجها المشروع')
    proposed_solution = models.TextField(blank=True, null=True, verbose_name='الحل المقترح')
    objectives = models.TextField(blank=True, null=True, verbose_name='أهداف المشروع')
    technologies = models.CharField(max_length=255, blank=True, null=True, verbose_name='التقنيات والأدوات المستخدمة')
    
    course_name = models.CharField(max_length=120, blank=True, null=True, verbose_name='اسم المقرر الأكاديمي')
    semester = models.CharField(max_length=60, blank=True, null=True, verbose_name='الفصل الدراسي')
    
    cover_image = models.ImageField(upload_to='project_covers/', default='project_covers/default.jpg', verbose_name='غلاف المشروع')
    demo_url = models.URLField(blank=True, null=True, verbose_name='رابط النسخة الحية / المعاينة')
    repository_url = models.URLField(blank=True, null=True, verbose_name='رابط المستودع البرمجي (GitHub / GitLab)')
    
    categories = models.ManyToManyField(Category, related_name='projects', verbose_name='التصنيفات')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft', verbose_name='حالة المشروع')
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_projects', verbose_name='صاحب المشروع')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخر تحديث')

    class Meta:
        verbose_name = 'مشروع'
        verbose_name_plural = 'المشاريع'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members', verbose_name='المشروع')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='project_memberships', verbose_name='حساب العضو (إن وجد)')
    member_name = models.CharField(max_length=120, verbose_name='اسم العضو')
    contribution_role = models.CharField(max_length=100, default='عضو فريق', verbose_name='الدور في المشروع')
    is_team_leader = models.BooleanField(default=False, verbose_name='قائد الفريق')

    class Meta:
        verbose_name = 'عضو فريق'
        verbose_name_plural = 'أعضاء الفريق'

    def __str__(self):
        return f"{self.member_name} - {self.project.title}"


class ProjectMedia(models.Model):
    MEDIA_TYPES = (
        ('image', 'صورة إضافية'),
        ('document', 'ملف توثيق / PDF'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='media_files', verbose_name='المشروع')
    media_type = models.CharField(max_length=15, choices=MEDIA_TYPES, verbose_name='نوع الملف')
    file = models.FileField(upload_to='project_files/', verbose_name='الملف المرفق')
    caption = models.CharField(max_length=200, blank=True, null=True, verbose_name='وصف الملف')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'ملف وسائط'
        verbose_name_plural = 'ملفات الوسائط'
