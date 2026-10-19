from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Project, Category

def project_gallery(request):
    """عرض معرض المشاريع مع دعم البحث والتصفية بحسب التصنيف وحالة الاعتماد"""
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()

    projects = Project.objects.filter(status='Approved')

    if request.user.is_authenticated:
        if request.user.is_supervisor or request.user.is_admin_user:
            projects = Project.objects.all()
        else:
            projects = Project.objects.filter(Q(status='Approved') | Q(created_by=request.user))

    if category_slug:
        projects = projects.filter(categories__slug=category_slug)

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


def project_detail(request, pk):
    """عرض تفاصيل المشروع الكاملة، أعضاء الفريق، المرفقات، والتقييمات"""
    project = get_object_or_404(Project, pk=pk)

    # التحقق من الصلاحيات: الزائر يرى فقط المعتمد، بينما الصاحب أو المشرف يرى مشروعه بأي حالة
    if project.status != 'Approved':
        if not request.user.is_authenticated:
            return render(request, 'projects/access_denied.html', status=403)
        if not (request.user == project.created_by or request.user.is_supervisor or request.user.is_admin_user):
            return render(request, 'projects/access_denied.html', status=403)

    members = project.members.all()
    media_files = project.media_files.all()
    evaluations = project.evaluations.prefetch_related('scores__criterion').all()
    comments = project.comments.select_related('author').filter(is_internal=False)

    tech_list = [t.strip() for t in project.technologies.split(',')] if project.technologies else []

    context = {
        'project': project,
        'members': members,
        'media_files': media_files,
        'evaluations': evaluations,
        'comments': comments,
        'tech_list': tech_list,
    }
    return render(request, 'projects/project_detail.html', context)
