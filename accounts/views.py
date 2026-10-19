from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import StudentRegistrationForm, LoginForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('projects:gallery')

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'مرحباً بك مجدداً، {user.get_full_name() or user.username}!')
            next_url = request.GET.get('next', 'projects:gallery')
            return redirect(next_url)
        else:
            form.add_error(None, 'اسم المستخدم أو كلمة المرور غير صحيحة.')

    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('projects:gallery')

    form = StudentRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.role = 'student' # الحسابات المسجلة ذاتياً هي حسابات طلاب
        user.save()
        login(request, user)
        messages.success(request, 'تم إنشاء حسابك الأكاديمي بنجاح في منصة أثَر!')
        return redirect('projects:gallery')

    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'تم تسجيل خروجك بنجاح.')
    return redirect('projects:gallery')
