from django.shortcuts import render, get_object_or_404
from .models import PersonalInfo

def resume_view(request, user_id=None):
    users = PersonalInfo.objects.all()
    person = None
    if user_id:
        person = get_object_or_404(PersonalInfo, id=user_id)
    elif users.exists():
        person = users.first()  # اولین کاربر به صورت پیش‌فرض
    context = {'users': users, 'person': person}
    return render(request, 'resume/resume.html', context)