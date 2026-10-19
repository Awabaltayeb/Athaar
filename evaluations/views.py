from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from decimal import Decimal
from projects.models import Project
from .models import EvaluationCriteria, Evaluation, EvaluationScore, Comment

@login_required
def supervisor_dashboard(request):
    """لوحة تحكم المشرف: استعراض المشاريع التي تنتظر التحكيم والمشاريع المحكّمة"""
    if not (request.user.is_supervisor or request.user.is_admin_user):
        messages.error(request, 'عذراً، هذه اللوحة مخصصة لأعضاء هيئة التدريس والمشرفين فقط.')
        return redirect('projects:gallery')

    pending_projects = Project.objects.filter(status='Under Review').order_by('-updated_at')
    approved_projects = Project.objects.filter(status='Approved').order_by('-updated_at')
    needs_changes_projects = Project.objects.filter(status='Needs Changes').order_by('-updated_at')

    context = {
        'pending_projects': pending_projects,
        'approved_projects': approved_projects,
        'needs_changes_projects': needs_changes_projects,
        'pending_count': pending_projects.count(),
        'approved_count': approved_projects.count(),
    }
    return render(request, 'evaluations/supervisor_dashboard.html', context)


@login_required
def evaluate_project(request, project_id):
    """استمارة تحكيم وتقييم المشروع بالمعايير الأكاديمية المعتمدة"""
    if not (request.user.is_supervisor or request.user.is_admin_user):
        messages.error(request, 'غير مخول لك تقييم المشاريع.')
        return redirect('projects:gallery')

    project = get_object_or_404(Project, pk=project_id)
    criteria = EvaluationCriteria.objects.all().order_by('id')

    if not criteria.exists():
        # إنشاء معايير افتراضية في حال كانت فارغة
        EvaluationCriteria.objects.create(criterion_name='وضوح المشكلة والأهداف', weight=20.00)
        EvaluationCriteria.objects.create(criterion_name='التنفيذ وجودة الإنتاج', weight=30.00)
        EvaluationCriteria.objects.create(criterion_name='الإبداع وجودة الحل', weight=20.00)
        EvaluationCriteria.objects.create(criterion_name='التوثيق والعرض الأكاديمي', weight=15.00)
        EvaluationCriteria.objects.create(criterion_name='النتائج وتحقيق المستهدفات', weight=15.00)
        criteria = EvaluationCriteria.objects.all().order_by('id')

    if request.method == 'POST':
        action = request.POST.get('action')

        # 1. حالة طلب تعديلات من الطالب
        if action == 'request_changes':
            supervisor_notes = request.POST.get('notes', '').strip()
            if not supervisor_notes:
                messages.error(request, 'يرجى كتابة ملاحظات توضيحية للطالب عند طلب التعديل.')
                return redirect('evaluations:evaluate_project', project_id=project.id)

            project.status = 'Needs Changes'
            project.save()

            Comment.objects.create(
                project=project,
                author=request.user,
                comment_text=f"طلب تعديلات من المشرف: {supervisor_notes}",
                is_internal=True
            )
            messages.warning(request, f'تمت إعادة مشروع "{project.title}" للطالب لاستكمال التعديلات المطلوبة.')
            return redirect('evaluations:dashboard')

        # 2. حالة الاعتماد والتقييم بالدرجات
        elif action == 'approve_and_publish':
            overall_feedback = request.POST.get('overall_feedback', '').strip()
            
            with transaction.atomic():
                total_weighted_score = Decimal('0.00')
                total_weight = Decimal('0.00')

                # إنشاء أو جلب سجل التقييم
                evaluation, _ = Evaluation.objects.get_or_create(
                    project=project,
                    evaluator=request.user,
                    defaults={'overall_feedback': overall_feedback}
                )
                evaluation.overall_feedback = overall_feedback

                # رصد درجات كل معيار وحساب المتوسط الموزون
                for crit in criteria:
                    score_val = request.POST.get(f'criterion_{crit.id}', '0').strip()
                    try:
                        score_dec = Decimal(score_val)
                    except:
                        score_dec = Decimal('0.00')
                    
                    # قصر الدرجة بين 0 و 100
                    score_dec = max(Decimal('0.00'), min(Decimal('100.00'), score_dec))

                    EvaluationScore.objects.update_or_create(
                        evaluation=evaluation,
                        criterion=crit,
                        defaults={'score': score_dec}
                    )

                    total_weighted_score += (score_dec * (crit.weight / Decimal('100.00')))
                    total_weight += crit.weight

                # ضبط المعدل النهائي
                if total_weight > 0:
                    evaluation.total_score = round(total_weighted_score, 2)
                else:
                    evaluation.total_score = Decimal('0.00')
                
                evaluation.save()

                # اعتماد ونشر المشروع رسمياً
                project.status = 'Approved'
                project.save()

            messages.success(request, f'تم تحكيم واعتماد مشروع "{project.title}" ونشره في المعرض العام بمعدل {evaluation.total_score}%!')
            return redirect('evaluations:dashboard')

    context = {
        'project': project,
        'criteria': criteria,
    }
    return render(request, 'evaluations/evaluate_project.html', context)
