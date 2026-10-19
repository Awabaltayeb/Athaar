from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Category, ProjectMember
from .forms import ProjectSubmissionForm

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


@login_required
def student_dashboard(request):
    """لوحة الطالب: متابعة مشاريعه الشخصية وحالات المراجعة"""
    my_projects = Project.objects.filter(created_by=request.user).order_by('-created_at')
    
    total_count = my_projects.count()
    approved_count = my_projects.filter(status='Approved').count()
    review_count = my_projects.filter(status='Under Review').count()
    draft_count = my_projects.filter(status='Draft').count()

    context = {
        'my_projects': my_projects,
        'total_count': total_count,
        'approved_count': approved_count,
        'review_count': review_count,
        'draft_count': draft_count,
    }
    return render(request, 'projects/student_dashboard.html', context)


@login_required
def project_create(request):
    """استمارة إنشاء وإيداع مشروع جديد للطالب"""
    if request.method == 'POST':
        form = ProjectSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            
            # تحديد الحالة بناءً على الزر المضغوط
            if 'submit_review' in request.POST:
                project.status = 'Under Review'
                msg = 'تم إرسال مشروعك بنجاح للمراجعة والتحكيم الأكاديمي!'
            else:
                project.status = 'Draft'
                msg = 'تم حفظ المشروع كمسودة خاصة بك.'

            project.save()
            form.save_m2m() # حفظ التصنيفات المتعددة

            # إضافة صاحب المشروع تلقائياً كقائد فريق
            ProjectMember.objects.create(
                project=project,
                user=request.user,
                member_name=request.user.get_full_name() or request.user.username,
                contribution_role='مؤسس وقائد المشروع',
                is_team_leader=True
            )

            messages.success(request, msg)
            return redirect('projects:dashboard')
    else:
        form = ProjectSubmissionForm()

    return render(request, 'projects/project_create.html', {'form': form})
