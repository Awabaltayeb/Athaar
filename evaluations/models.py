from django.db import models
from django.conf import settings
from projects.models import Project

class EvaluationCriteria(models.Model):
    criterion_name = models.CharField(max_length=150, verbose_name='اسم المعيار')
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text='الوزن النسبي (مثلاً: 20 لـ 20%)', verbose_name='الوزن')
    description = models.TextField(blank=True, null=True, verbose_name='وصف المعيار وطريقة قياسه')

    class Meta:
        verbose_name = 'معيار تقييم'
        verbose_name_plural = 'معايير التقييم'

    def __str__(self):
        return f"{self.criterion_name} ({self.weight}%)"


class Evaluation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='evaluations', verbose_name='المشروع')
    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='my_evaluations', verbose_name='المشرف المُقيِّم')
    total_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name='المعدل الكلي النهائي')
    overall_feedback = models.TextField(verbose_name='التقرير والملاحظات العامة')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ التقييم')

    class Meta:
        verbose_name = 'تقييم أكاديمي'
        verbose_name_plural = 'التقييمات الأكاديمية'

    def __str__(self):
        return f"تقييم {self.project.title} - {self.total_score}%"


class EvaluationScore(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='scores', verbose_name='التقييم')
    criterion = models.ForeignKey(EvaluationCriteria, on_delete=models.CASCADE, verbose_name='المعيار')
    score = models.DecimalField(max_digits=5, decimal_places=2, help_text='الدرجة الممنوحة من 100', verbose_name='الدرجة')
    feedback = models.TextField(blank=True, null=True, verbose_name='ملاحظات خاصة بهذا المعيار')

    class Meta:
        verbose_name = 'درجة المعيار'
        verbose_name_plural = 'درجات المعايير'
        unique_together = ('evaluation', 'criterion')


class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments', verbose_name='المشروع')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='الكاتب')
    comment_text = models.TextField(verbose_name='نص التعليق')
    is_internal = models.BooleanField(
        default=False, 
        help_text='إذا تم التحديد، يكون التعليق خاصاً بين المشرف وأصحاب المشروع فقط أثناء المراجعة',
        verbose_name='ملاحظة مراجعة داخلية'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإضافة')

    class Meta:
        verbose_name = 'تعليق / ملاحظة'
        verbose_name_plural = 'التعليقات والملاحظات'
        ordering = ['created_at']

    def __str__(self):
        return f"تعليق بواسطة {self.author.username} على {self.project.title}"
