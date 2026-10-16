from django.contrib import admin
from .models import EvaluationCriteria, Evaluation, EvaluationScore, Comment

class EvaluationScoreInline(admin.TabularInline):
    model = EvaluationScore
    extra = 0

@admin.register(EvaluationCriteria)
class EvaluationCriteriaAdmin(admin.ModelAdmin):
    list_display = ('criterion_name', 'weight')
    search_fields = ('criterion_name',)

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('project', 'evaluator', 'total_score', 'created_at')
    list_filter = ('created_at', 'evaluator')
    search_fields = ('project__title', 'evaluator__username')
    inlines = [EvaluationScoreInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('project', 'author', 'is_internal', 'created_at')
    list_filter = ('is_internal', 'created_at')
    search_fields = ('project__title', 'author__username', 'comment_text')
