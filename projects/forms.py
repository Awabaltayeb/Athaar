from django import forms
from .models import Project, Category

class ProjectSubmissionForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'accent-cyan-400'}),
        label='التصنيفات الأكاديمية (يمكنك اختيار أكثر من تخصص)'
    )

    class Meta:
        model = Project
        fields = [
            'title', 'categories', 'summary', 'problem_statement', 
            'proposed_solution', 'objectives', 'technologies', 
            'course_name', 'semester', 'cover_image', 'demo_url', 'repository_url'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'عنوان المشروع المبتكر...', 'class': 'form-input-glass'}),
            'summary': forms.Textarea(attrs={'rows': 3, 'placeholder': 'ملخص تنفيذي يوضح جوهر الفكرة...', 'class': 'form-input-glass'}),
            'problem_statement': forms.Textarea(attrs={'rows': 4, 'placeholder': 'ما هي الفجوة أو المشكلة الواقعية التي يعالجها المشروع؟', 'class': 'form-input-glass'}),
            'proposed_solution': forms.Textarea(attrs={'rows': 4, 'placeholder': 'كيف يقدم مشروعك حلاً عملياً وتقنياً لهذه المشكلة؟', 'class': 'form-input-glass'}),
            'objectives': forms.Textarea(attrs={'rows': 3, 'placeholder': 'أهداف المشروع القابلة للقياس ومخرجاته المتوقعة...', 'class': 'form-input-glass'}),
            'technologies': forms.TextInput(attrs={'placeholder': 'مثال: Python, Django, Flutter, Figma, IoT', 'class': 'form-input-glass'}),
            'course_name': forms.TextInput(attrs={'placeholder': 'مثال: مشروع التخرج، هندسة البرمجيات، بحوث العمليات', 'class': 'form-input-glass'}),
            'semester': forms.TextInput(attrs={'placeholder': 'مثال: ربيع 2025', 'class': 'form-input-glass'}),
            'demo_url': forms.URLInput(attrs={'placeholder': 'https://example.com/demo', 'class': 'form-input-glass'}),
            'repository_url': forms.URLInput(attrs={'placeholder': 'https://github.com/username/project', 'class': 'form-input-glass'}),
        }
        labels = {
            'title': 'عنوان المشروع',
            'summary': 'الملخص التنفيذي',
            'problem_statement': 'بيان المشكلة الواقعية',
            'proposed_solution': 'الحل المقترح',
            'objectives': 'أهداف المشروع ومخرجاته',
            'technologies': 'التقنيات والأدوات المستخدمة',
            'course_name': 'المقرر الأكاديمي',
            'semester': 'الفصل الدراسي',
            'cover_image': 'غلاف المشروع البصري (صورة)',
            'demo_url': 'رابط التجربة الحية (Demo)',
            'repository_url': 'رابط المستودع البرمجي (GitHub / GitLab)',
        }
