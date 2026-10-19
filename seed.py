import os
import django

# تهيئة بيئة دجانغو
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User
from projects.models import Category, Project, ProjectMember
from evaluations.models import EvaluationCriteria, Evaluation, EvaluationScore

def run_seed():
    print("⏳ جاري حقن بيانات منصة أثَر التجريبية...")

    # 1. إنشاء التصنيفات الأكاديمية
    cat_software, _ = Category.objects.get_or_create(
        slug='software', 
        defaults={'name': 'برمجيات وتطبيقات', 'description': 'مشاريع الويب، تطبيقات الهاتف، والأنظمة المدمجة'}
    )
    cat_ai, _ = Category.objects.get_or_create(
        slug='ai-research', 
        defaults={'name': 'أبحاث وذكاء اصطناعي', 'description': 'التعلم الآلي، معالجة اللغات، والأوراق العلمية'}
    )
    cat_design, _ = Category.objects.get_or_create(
        slug='design', 
        defaults={'name': 'تصميم وواجهات', 'description': 'تجربة المستخدم، الهويات البصرية، والتصميم التفاعلي'}
    )
    cat_media, _ = Category.objects.get_or_create(
        slug='multimedia', 
        defaults={'name': 'وسائط متعددة', 'description': 'المؤثرات البصرية، الفيديو، والإنتاج الرقمي'}
    )

    # 2. إنشاء المستخدمين (طلاب ومشرف)
    supervisor, _ = User.objects.get_or_create(
        username='dr_khalid',
        defaults={
            'first_name': 'د. خالد',
            'last_name': 'الطيب',
            'email': 'khalid@athar.edu',
            'role': 'supervisor',
            'department': 'علوم الحاسوب ونظم المعلومات'
        }
    )
    if _:
        supervisor.set_password('Pass123456')
        supervisor.save()

    student1, _ = User.objects.get_or_create(
        username='mohammed_ali',
        defaults={
            'first_name': 'محمد',
            'last_name': 'علي عثمان',
            'email': 'm.ali@student.edu',
            'role': 'student',
            'academic_id': 'CS-2021-042',
            'department': 'هندسة البرمجيات'
        }
    )
    if _:
        student1.set_password('Pass123456')
        student1.save()

    student2, _ = User.objects.get_or_create(
        username='sara_hassan',
        defaults={
            'first_name': 'سارة',
            'last_name': 'حسن أحمد',
            'email': 'sara.h@student.edu',
            'role': 'student',
            'academic_id': 'GD-2022-118',
            'department': 'تصميم الوسائط المتعددة'
        }
    )
    if _:
        student2.set_password('Pass123456')
        student2.save()

    # 3. إنشاء معايير التقييم الخمسة (وفق وثيقة التخطيط)
    c1, _ = EvaluationCriteria.objects.get_or_create(criterion_name='وضوح المشكلة والأهداف', defaults={'weight': 20.00})
    c2, _ = EvaluationCriteria.objects.get_or_create(criterion_name='التنفيذ وجودة الإنتاج', defaults={'weight': 30.00})
    c3, _ = EvaluationCriteria.objects.get_or_create(criterion_name='الإبداع وجودة الحل', defaults={'weight': 20.00})
    c4, _ = EvaluationCriteria.objects.get_or_create(criterion_name='التوثيق والعرض الأكاديمي', defaults={'weight': 15.00})
    c5, _ = EvaluationCriteria.objects.get_or_create(criterion_name='النتائج وتحقيق المستهدفات', defaults={'weight': 15.00})

    # 4. المشروع الأول: منظومة نبض الطبية (برمجيات + ذكاء اصطناعي)
    p1, created1 = Project.objects.get_or_create(
        title='منظومة نبض: مراقبة المؤشرات الحيوية الطبية عبر إنترنت الأشياء والذكاء الاصطناعي',
        defaults={
            'summary': 'نظام متكامل يربط أجهزة قياس العلامات الحيوية للمرضى بمنصة سحابية تحلل البيانات في الوقت الفعلي للتنبؤ بالنوبات القلبية المبكرة.',
            'problem_statement': 'تأخر التدخل الطبي في حالات التدهور المفاجئ لمرضى العناية المنزلية لعدم وجود ربط مباشر مستمر مع غرف الطوارئ.',
            'proposed_solution': 'بناء سوار ذكي منخفض التكلفة يرسل نبضات القلب ونسبة الأكسجين إلى خادم دجانغو، مع نموذج تنبؤي يصدر إنذارات استباقية للكوادر الطبية.',
            'objectives': '1. خفض زمن الاستجابة للحالات الحرجة بنسبة 40%.\n2. توفير منصة أرشيفية آمنة لسجلات المرضى الحيوية.\n3. دعم التشغيل على شبكات الاتصال المتقطعة.',
            'technologies': 'Python, Django, Flutter, TensorFlow Lite, ESP32, MQTT',
            'course_name': 'مشروع تخرج - السنة الرابعة',
            'semester': 'ربيع 2025',
            'demo_url': 'https://nabd-health.example.com',
            'repository_url': 'https://github.com/athar-showcase/nabd-iot',
            'status': 'Approved',
            'created_by': student1
        }
    )
    if created1:
        p1.categories.add(cat_software, cat_ai)
        ProjectMember.objects.create(project=p1, member_name='محمد علي عثمان', contribution_role='تطوير البنية الخلفية وإنترنت الأشياء', is_team_leader=True)
        ProjectMember.objects.create(project=p1, member_name='أحمد التاج بابكر', contribution_role='تطوير تطبيق الهاتف (Flutter)')
        ProjectMember.objects.create(project=p1, member_name='رؤى صديق عبدالرحمن', contribution_role='تدريب وتحسين نموذج الذكاء الاصطناعي')

        # إضافة التقييم الأكاديمي للمشروع الأول
        eval1 = Evaluation.objects.create(
            project=p1,
            evaluator=supervisor,
            total_score=94.50,
            overall_feedback='مشروع استثنائي يعالج فجوة حقيقية في القطاع الصحي المحلي. التكامل بين عتاد الـ IoT والبرمجيات نُفذ بدقة ممتازة، والتوثيق الأكاديمي مكتمل الأركان.'
        )
        EvaluationScore.objects.create(evaluation=eval1, criterion=c1, score=95.00)
        EvaluationScore.objects.create(evaluation=eval1, criterion=c2, score=96.00)
        EvaluationScore.objects.create(evaluation=eval1, criterion=c3, score=92.00)
        EvaluationScore.objects.create(evaluation=eval1, criterion=c4, score=95.00)
        EvaluationScore.objects.create(evaluation=eval1, criterion=c5, score=94.00)

    # 5. المشروع الثاني: تجربة وهوية منصة رافد التعليمية (تصميم ووسائط)
    p2, created2 = Project.objects.get_or_create(
        title='منصة رافد: إعادة تصور تجربة التعلم الرقمي التفاعلي للجامعات السودانية',
        defaults={
            'summary': 'دراسة وتصميم واجهات وتجربة مستخدم (UI/UX) لمنصة تعليمية متكيفة تراعي سرعات الإنترنت المتواضعة وتعتمد نظام الموديولات الخفيفة.',
            'problem_statement': 'تعقيد منصات التعليم الإلكتروني الحالية واعتمادها على اتصالات مستقرة، مما يسبب عزوف الطلاب عن متابعة المقررات أوقات الأزمات.',
            'proposed_solution': 'نظام تصميم تفاعلي قائم على واجهات بسيطة غنية بالمعلومات وتدعم القراءة بدون إنترنت مع هوية بصرية مريحة للعين.',
            'objectives': '1. إنجاز نظام تصميم كامل (Design System) مخصص باللغة العربية.\n2. تصميم وتجربة 45 شاشة تفاعلية لكافة رحلات المستخدم.\n3. اختبار قابلية الاستخدام على عينة من 50 طالباً.',
            'technologies': 'Figma, Adobe Illustrator, Design Systems, Usability Testing',
            'course_name': 'تصميم تفاعلي متقدم',
            'semester': 'خريف 2024',
            'demo_url': 'https://figma.com/@athar/rafid-prototype',
            'repository_url': 'https://github.com/athar-showcase/rafid-design-system',
            'status': 'Approved',
            'created_by': student2
        }
    )
    if created2:
        p2.categories.add(cat_design, cat_media)
        ProjectMember.objects.create(project=p2, member_name='سارة حسن أحمد', contribution_role='باحثة تجربة مستخدم ومصممة واجهات', is_team_leader=True)
        ProjectMember.objects.create(project=p2, member_name='مروة كمال الدين', contribution_role='تصميم الهوية البصرية والرسوم التوضيحية')

        eval2 = Evaluation.objects.create(
            project=p2,
            evaluator=supervisor,
            total_score=89.00,
            overall_feedback='منهجية بحثية رصينة وفهم عميق لاحتياجات بيئة الطلاب المحلية. تميز واضح في اختيار الخطوط وتناسق درجات الألوان.'
        )
        EvaluationScore.objects.create(evaluation=eval2, criterion=c1, score=90.00)
        EvaluationScore.objects.create(evaluation=eval2, criterion=c2, score=88.00)
        EvaluationScore.objects.create(evaluation=eval2, criterion=c3, score=92.00)
        EvaluationScore.objects.create(evaluation=eval2, criterion=c4, score=90.00)
        EvaluationScore.objects.create(evaluation=eval2, criterion=c5, score=85.00)

    print("✅ تم حقن البيانات بنجاح تام! افتح الموقع لترى المعرض ينبض بالحياة.")

if __name__ == '__main__':
    run_seed()
