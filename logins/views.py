from django.shortcuts import render, redirect
from . import models
from . import form
import hashlib
# Create your views here.
def hash_code(s, salt='login'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def index(request):
    if not request.session.get('is_login', None):
        return redirect('/logins/')
    return render(request, 'logins/index.html')

def logins(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == 'POST':
        login_form = form.UserForm(request.POST)
        message = '请检查填写的内容!'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.User.objects.get(name=username)
            except:
                message = '用户不存在!'
                return render(request, 'logins/logins.html', locals())
            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = '密码不正确!'
                return render(request, 'logins/logins.html', locals())
        else:
            return render(request, 'logins/logins.html', locals())

    login_form = form.UserForm()
    return render(request, 'logins/logins.html', locals())

def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == 'POST':
        register_form = form.RegisterForm(request.POST)
        message = '请检查填写的内容'
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message= '两次输入的密码不同!'
                return render(request, 'logins/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在!'
                    return render(request, 'logins/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册!'
                    return render(request, 'logins/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                return redirect('/logins/')
        else:
            return render(request, 'logins/register.html', locals())
    register_form = form.RegisterForm()
    return render(request, 'logins/register.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/logins/')
    request.session.flush()
    return redirect('/logins/')

