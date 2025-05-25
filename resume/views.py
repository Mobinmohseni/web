from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import PersonalInfo, ContactMessage, Education, Experience, Skill, Project
from .forms import ResumeForm
import requests
import json


def resume_view(request, user_id=None):
    users = PersonalInfo.objects.all()
    person = None
    if user_id:
        person = get_object_or_404(PersonalInfo, id=user_id)
    elif users.exists():
        person = users.first()
    users_json = json.dumps([{'id': user.id, 'name': user.name} for user in users])
    context = {'users': users, 'person': person, 'users_json': users_json}
    return render(request, 'resume/resume.html', context)


def contact_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # ارسال به Formspree
        formspree_url = 'https://formspree.io/f/xjkwwljb'
        data = {
            'name': name,
            'email': email,
            'message': message
        }
        response = requests.post(formspree_url, data=data)

        # ذخیره در دیتابیس و پیام موفقیت اگر ارسال موفق بود
        if response.status_code == 200:
            ContactMessage.objects.create(
                name=name,
                email=email,
                message=message
            )
            messages.success(request, 'پیام شما با موفقیت ارسال شد!')
        else:
            messages.error(request, 'خطا در ارسال پیام. لطفاً دوباره تلاش کنید.')

        return HttpResponseRedirect(reverse('resume'))

    return HttpResponseRedirect(reverse('resume'))


def create_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            # ذخیره اطلاعات شخصی
            person = PersonalInfo.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                linkedin=form.cleaned_data['linkedin']
            )
            # ذخیره تحصیلات
            if form.cleaned_data['degree'] and form.cleaned_data['university']:
                Education.objects.create(
                    person=person,
                    degree=form.cleaned_data['degree'],
                    university=form.cleaned_data['university'],
                    start=form.cleaned_data['edu_start'],
                    end=form.cleaned_data['edu_end']
                )
            # ذخیره تجربه کاری
            if form.cleaned_data['title'] and form.cleaned_data['company']:
                Experience.objects.create(
                    person=person,
                    title=form.cleaned_data['title'],
                    company=form.cleaned_data['company'],
                    start=form.cleaned_data['exp_start'],
                    end=form.cleaned_data['exp_end'],
                    description=form.cleaned_data['description']
                )
            # ذخیره مهارت‌ها
            skills = form.cleaned_data['skills'].split(',')
            for skill in skills:
                skill = skill.strip()
                if skill:
                    Skill.objects.create(person=person, name=skill)
            # ذخیره پروژه
            if form.cleaned_data['project_name'] and form.cleaned_data['project_description']:
                Project.objects.create(
                    person=person,
                    name=form.cleaned_data['project_name'],
                    description=form.cleaned_data['project_description'],
                    link=form.cleaned_data['project_link']
                )
            messages.success(request, 'رزومه با موفقیت ایجاد شد!')
            return HttpResponseRedirect(reverse('resume_user', args=[person.id]))
    else:
        form = ResumeForm()
    return render(request, 'resume/create_resume.html', {'form': form})
