from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Project, Category

def project_gallery(request):
    """عرض معرض المشاريع مع دعم البحث والتصفية بحسب التصنيف وحالة الاعتماد"""
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()

    # للزوار العاديين: نعرض المشاريع المعتمدة فقط
    projects = Project.objects.filter(status='Approved')

    # للمستخدمين المسجلين: المشرف يرى كل المشاريع، والطالب يرى المعتمدة ومشاريع نفسه
    if request.user.is_authenticated:
        if request.user.is_supervisor or request.user.is_admin_user:
            projects = Project.objects.all()
        else:
            projects = Project.objects.filter(Q(status='Approved') | Q(created_by=request.user))

    # التصفية حسب التصنيف المختار
    if category_slug:
        projects = projects.filter(categories__slug=category_slug)

    # التصفية حسب كلمة البحث (بالعنوان، الملخص، التقنيات، أو اسم صاحب المشروع)
    if query:
        projects = projects.filter(
            Q(title__icontains=query) |
            Q(summary__icontains=query) |
            Q(technologies__icontains=query) |
            Q(created_by__first_name__icontains=query) |
            Q(created_by__last_name__icontains=query)
        ).distinct()

    categories = Category.objects.all()

    context = {
        'projects': projects,
        'categories': categories,
        'selected_category': category_slug,
        'search_query': query,
    }
    return render(request, 'projects/gallery.html', context)
