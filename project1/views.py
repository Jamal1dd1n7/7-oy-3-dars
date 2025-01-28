# Imports:
# Messages: template ga xabar jo`natish uchun ishlatiladi
# ( message.success(request, 'Amal muvaffaqiyatli amalga oshirildi'));
from django.contrib import messages
#--------------------------------------------------------------------------------

# Login, Logout, Authenticate: ...;
from django.contrib.auth import login, logout, authenticate
#--------------------------------------------------------------------------------

# Permission required, login required: Foydalanuvchi uchun ruxsatlar borligini tekshiruvchi funksiyalar;
from django.contrib.auth.decorators import permission_required, login_required
#--------------------------------------------------------------------------------

# Mixin class: Ro`yxatdan o`tganlikka tekshiruvchi class;
from django.contrib.auth.mixins import LoginRequiredMixin
#--------------------------------------------------------------------------------

# Send mail: Xabarni kiritilgan emailga jo`natish uchun ishlatiladi;
from django.core.mail import send_mail
#--------------------------------------------------------------------------------

# Paginator: template da model cheklanganidan ortib ketsa, yangi page da chiqaradigan class;
from django.core.paginator import Paginator
#--------------------------------------------------------------------------------

# WSGIRequest: ...;
from django.core.handlers.wsgi import WSGIRequest
#--------------------------------------------------------------------------------

# Render, Redirect, Get_object_or_404, Get_list_or_404: ...; 
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
#--------------------------------------------------------------------------------

# Reverse lazy: ...;
from django.urls import reverse_lazy
#--------------------------------------------------------------------------------

# View class: ...;
from django.views import View
#--------------------------------------------------------------------------------

# Generic Views: Oldindan tayyorlangan "view"lar( ListView, DetailView);
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
#--------------------------------------------------------------------------------

# Now function: Ayni vaqtni olib beruvchi funksiya;
from django.utils.timezone import now 
#--------------------------------------------------------------------------------

# Datetime function: Bugungi sana, oy, yilni olib beruvchi funksiya;
from datetime import datetime
#--------------------------------------------------------------------------------

# User model: User uchun yozilgan model;
# from django.contrib.auth.models import User
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

# .models: models.py faylidan modellarni import qiladi;
from .models import *
#--------------------------------------------------------------------------------

# .forms: forms.py faylidan formlarni import qiladi; 
from .forms import *

# Generic Views
# Views:
# Home,
# Message(send_message)

# Home
class HomeView(ListView):
    template_name = 'project1/intex.html'
    model = Group
    context_object_name = "groups"
    extra_context = {
        "title": "Home"
    }
    
    def get_context_data(self, *, objects_list=None,**kwargs):
        context = super().get_context_data(objects_list=None, **kwargs)
        context['courses'] = Course.objects.all()
        return context
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

# Course
class CourseView(LoginRequiredMixin, ListView):
    template_name = 'project1/course.html'
    def get_queryset(self):
        groups = Group.objects.filter(course_id=self.kwargs.get('course_id'))  
        if groups.exists():   
            return groups  
        else:
            messages.error(self.request, 'Bu kursda hozirda guruhlar yo`q')
            return None  
        
    def render_to_response(self, context, **response_kwargs):
        if self.get_queryset() is None:
            return redirect(reverse_lazy('home'))  
        return super().render_to_response(context, **response_kwargs)
    
    
class AddCourseView(CreateView):
    template_name = 'project1/add_course.html'
    model = Course
    fields = '__all__'
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Kurs muvaffaqiyatli qo`shildi")
        return response
    success_url = reverse_lazy('home')

class UpdateCourseView(UpdateView):
    template_name = 'project1/add_course.html'
    model = Course
    pk_url_kwarg = 'course_id'
    fields = '__all__'
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        messages.success(self.request, "Kurs ma'lumotlari muvaffaqiyatli o'zgartirildi")
        return super().form_valid(form)

class DeleteCourseView(DeleteView):
    model = Course
    pk_url_kwarg = 'course_id'
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        messages.success(self.request, "Kurs ma'lumotlari muvaffaqiyatli o'chirildi")
        return super().form_valid(form)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

# Group
class GroupView(ListView):
    template_name = 'project1/group.html'
    def get_queryset(self):
        lessons = Lesson.objects.filter(group_id=self.kwargs.get('group_id'))  
        if lessons.exists():
            return lessons  
        else:
            messages.error(self.request, 'Bu guruhda hozirda darslar yo`q')
            return None  

    def render_to_response(self, context, **response_kwargs):
        if self.get_queryset() is None:
            return redirect(reverse_lazy('home'))  
        return super().render_to_response(context, **response_kwargs)
    

class AddGroupView(CreateView):
    template_name = 'project1/add_group.html'
    model = Group
    fields = ['title', 'teacher', 'course', 'student_count']
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Guruh muvoffaqiyatli qo`shildi')
        return response
    success_url = reverse_lazy('home')

class UpdateGroupView(UpdateView):
    template_name = 'project1/add_group.html'
    model = Group
    fields = ['title', 'teacher', 'course', 'student_count']
    pk_url_kwarg = 'group_id'
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        messages.success(self.request, "Guruh ma'lumotlari muvaffaqiyatli o'zgartirildi")
        return super().form_valid(form)

class DeleteGroupView(DeleteView):
    model = Group
    pk_url_kwarg = 'group_id'
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        messages.success(self.request, "Guruh ma'lumotlari muvaffaqiyatli o'chirildi")
        return super().form_valid(form)
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------


# Lesson
class LessonDetail(DetailView):
    template_name = 'project1/lesson.html'
    model = Lesson
    pk_url_kwarg = 'lesson_id'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(objects_list=None, **kwargs)
        context['comments'] = Comment.objects.all()
        context['comment_form'] = CommentForm()  
        return context

    def post(self, request, *args, **kwargs):
        lesson = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.lesson = lesson  
            comment.author = request.user  
            comment.save()
            messages.success(request, "Fikr muvaffaqiyatli qo'shildi!")
        else:
            messages.error(request, "Fikrni yuborishda xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")
        return redirect('lesson_detail', lesson_id=lesson.id)
class AddLessonView(CreateView):
    template_name = 'project1/add_lesson.html'
    model = Lesson
    fields = ['title', 'teacher', 'content', 'duration', 'group']
    success_url = reverse_lazy('home')

class UpdateLessonView(UpdateView):
    template_name = 'project1/add_lesson.html'
    model = Lesson
    fields = ['title', 'teacher', 'content', 'duration', 'group']
    pk_url_kwarg = 'lesson_id'
    success_url = reverse_lazy('home')

class DeleteLessonView(DeleteView):
    template_name = 'project1/lesson_confirm_delete.html'
    model = Lesson
    success_url = reverse_lazy('home')
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------


# Message
class SendMessage(LoginRequiredMixin, View):
    template_name = 'templates/message.html'
    def get(self, request):
        form = MessageForm()
        return render(request, 'message.html', {'form': form})
    
    def post(self, request):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.save()
            try:
                send_mail(
                    subject=message.subject,  
                    message=message.message,  
                    from_email="jamal1dd1n_07 <request.user.email>",  
                    recipient_list=[message.to_user],  
                    fail_silently=False,
                )
                messages.success(request, f"Xabar '{message.subject}' muvaffaqiyatli yuborildi!")
            except Exception as e:
                messages.error(request, f"Xabar yuborishda xatolik yuz berdi: {e}")
            return redirect('home')  
        else:
            messages.error(request, "Form noto'g'ri to'ldirilgan. Iltimos, qaytadan urinib ko'ring.")
            return render(request, self.template_name, {'form': form})

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# Function Views
# Views: 
# Home, 
# Course(course, add_course, update_course, delete_course), 
# Group(group, add_group), 
# Lesson(lesson, add_lesson, update_lesson, delete_lesson),
# Comment(comment_save, comment_update, comment_delete),
# Auth(register, loginPage, logoutPage),
# 404(send_404),
# Message(send_message)

# Home
def home(request: WSGIRequest):
    courses = Course.objects.all()
    groups = Group.objects.all()

    paginator = Paginator(groups, 3)
    page = request.GET.get('page', 1)

    context = {
        'courses': courses,
        'groups': paginator.get_page(page)
    }
    return render(request, 'intex.html', context)
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

# Course
def course(request: WSGIRequest, course_id):
    course = get_object_or_404(Course, pk = course_id)
    groups = Group.objects.filter(course_id= course_id)

    paginator = Paginator(groups, 3)
    page = request.GET.get('page', 1)

    context = {
        'course': course,
        'groups': paginator.get_page(page)
    }
    return render(request, 'course.html', context)

@permission_required('project1.add_course', login_url='404')
def add_course(request: WSGIRequest):
    if request.method == 'POST':
        form = CourseForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            course = form.save()
            messages.success(request, f"{course} kursi qo`shildi!!!")
            return redirect('home')
        else:
            print(form.errors)
    form = CourseForm()
    context = {
        "form": form
    }
    return render(request, 'add_course.html', context)

@permission_required('project1.update_course', login_url='404')
def update_course(request: WSGIRequest, course_id):
    course = get_object_or_404(Course, pk= course_id)
    if request.method == 'POST':
        form = CourseForm(data=request.POST, files=request.FILES, instance=course)
        if form.is_valid():
            course = form.save()
            messages.success(request, "Ma'lumot muvaffaqiyatli o'zgartirildi.")
            return redirect('home')
    forms = CourseForm(instance=course)
    context = {
        'forms': forms,
        'current_year': datetime.now().year
    }
    return render(request, 'add_course.html', context)

@permission_required('project1.delete_course', login_url='404')
def delete_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    course.delete()
    messages.success(request, "Ma'lumot muvaffaqiyatli o'chirildi.")
    return redirect('home')
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

# Group
def group(request:WSGIRequest, group_id):
    lessons = Lesson.objects.filter(id=group_id)

    paginator = Paginator(lessons, 3)
    page = request.GET.get('page', 1)

    context = {
        "lessons": paginator.get_page(page)
    }
    return render(request, 'group.html', context)

@permission_required('project1.add_group', login_url='404')
def add_group(request: WSGIRequest):
    if request.method == 'POST':
        form = GroupForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"{group} kursi qo`shildi!!!")
            return redirect('home')
        else:
            print(form.errors)
    form = GroupForm()
    context = {
        "form": form
    }
    return render(request, 'add_group.html', context)
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

# Lesson
@login_required
def lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    comments = Comment.objects.filter(lesson=lesson)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save(user=request.user, lesson=lesson) 
    else:
        form = CommentForm()

    context = {
        'lesson': lesson,
        'form': form,
        'comments': comments,
        'current_year': now().year,
    }
    return render(request, 'lesson.html', context)

@permission_required('project1.add_lesson', login_url='404')
def add_lesson(request):
    if request.method == 'POST':
        form = LessonForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            lesson = form.save()  
            messages.success(request, f"{lesson.title} muvaffaqiyatli qo'shildi!")
            return redirect('home')
        else:
            messages.error(request, "Formda xatolik bor. Iltimos, qayta urinib ko'ring.")

    else:
        form = LessonForm()

    context = {
        "form": form
    }
    return render(request, 'add_lesson.html', context)

@permission_required('project1.update_lesson', login_url='404')
def update_lesson(request: WSGIRequest, lesson_id):
    lesson = get_object_or_404(Course, pk=lesson_id)

    if request.method == 'POST':
        form = CourseForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            lesson.title = form.cleaned_data.get('title')
            lesson.teacher = form.cleaned_data.get('teacher')
            lesson.content = form.cleaned_data.get('content')
            lesson.course = form.cleaned_data.get('title')
            lesson.save()

            messages.success(request, "Ma'lumot muvaffaqiyatli o'zgartirildi.")
            if lesson.published:
                return redirect('lesson_detail', lesson_id=lesson_id)
            else:
                return redirect('home')

    forms = LessonForm(initial={
        'title': lesson.title,
        'teacher':lesson.teacher,
        'content':lesson.content,
        'group':lesson.group
    })

    context = {
        'forms': forms
    }

    return render(request, 'addLesson.html', context)

@permission_required('project1.delate_lesson', login_url='404')
def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(lesson, pk=lesson_id)
    lesson.delete()

    messages.success(request, "Ma'lumot muvaffaqiyatli o'chirildi.")
    return redirect('home')
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

# Comment
def comment_save(request: WSGIRequest, lesson_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentForm(data=request.POST)
            lesson = get_object_or_404(Lesson, pk=lesson_id)
            if form.is_valid():
                form.save(Comment, request.user, lesson)

                messages.success(request, "Izoh muvaffaqiyatli qo'shildi.")
                return redirect('lesson_detail', lesson_id=lesson_id)
    else:
        messages.error(request, "Iltimos, tizimga kirishingiz kerak.")
        return redirect('login')

def comment_update(request: WSGIRequest, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_id)
        lesson_id = comment.lesson.id
        if request.user == comment.author or request.user.is_superuser:
            if request.method == 'POST':
                form = CommentForm(data=request.POST)
                if form.is_valid():
                    form.update(comment)

                    messages.success(request, "Izoh muvaffaqiyatli o'zgartirildi.")
                    return redirect('lesson_detail', lesson_id=lesson_id)

            else:
                form = CommentForm(initial={'text': comment.text})

            context = {
                'lesson': comment.lesson,
                'form': form,
                'update': True,
                'comment': comment,
                'comments': Comment.objects.filter(lesson_id=lesson_id)
            }

            return render(request, 'lesson.html', context)

    else:
        messages.error(request, "Iltimos, tizimga kirishingiz kerak.")
        return redirect('login')

def comment_delete(request: WSGIRequest, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_id)
        if request.user == comment.author or request.user.is_superuser:
            lesson_id = comment.lesson.id
            comment.delete()
            messages.success(request, "Izoh muvaffaqiyatli o'chirildi!")
            return redirect('lesson_detail', lesson_id=lesson_id)
        
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

# Auth
def register(request: WSGIRequest):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,
                             "Tabriklaymiz! Siz muvaffaqiyatli ro'yxatdan o'tdingiz va tizimga kirish uchun tayyorsiz.")
            return redirect('login')
    else:
        form = RegisterForm()

    context = {
        'forms': form,
        'current_year': datetime.now().year
    }

    return render(request, 'auth/sign_up.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')  

    form = LoginForm(data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Tizimga muvaffaqiyatli kirdingiz!")
                return redirect('home')
            else:
                messages.error(
                    request,
                    "Kiritilgan foydalanuvchi nomi yoki parol noto`g`ri. Iltimos, qayta tekshirib ko`ring."
                )

    context = {
        'form': form,
        'current_year': now().year 
    }

    return render(request, 'auth/login.html', context)

def logoutPage(request: WSGIRequest):
    logout(request)
    messages.success(request, "Tizimdan muvaffaqiyatli chiqdingiz!")
    return redirect('home')
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

# 404
def send_404(request:WSGIRequest):
    return render(request,'404.html')
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

# Message 
def send_message(request):
    # POST so'rovni qayta ishlash
    if request.method == 'POST':
        form = MessageForm(data=request.POST)
        if form.is_valid():
            # Xabarni bazaga saqlash
            message = form.save(commit=False)  # Ma'lumotlarni validatsiyadan o'tkazish
            message.author = request.user  # Hozirgi foydalanuvchi - muallif
            message.save()

            # Email jo'natish jarayoni
            try:
                send_mail(
                    subject=message.subject,  # Xabar sarlavhasi
                    message=message.message,  # Xabar matni
                    from_email=f"Foydalanuvchi <{request.user.email}>",  # Kimdan yuborilyapti
                    recipient_list=[message.to_user],  # Kimga yuborilyapti
                    fail_silently=False,
                )
                messages.success(request, f"Xabar '{message.subject}' muvaffaqiyatli yuborildi!")
            except Exception as e:
                messages.error(request, f"Xabar yuborishda xatolik yuz berdi: {e}")

            return redirect('home')  # Muvaffaqiyatdan so'ng, foydalanuvchini bosh sahifaga yo'naltirish
    else:
        # GET so'rov uchun bo'sh formni ko'rsatish
        form = MessageForm()

    return render(request, 'message.html', {'form': form})
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------