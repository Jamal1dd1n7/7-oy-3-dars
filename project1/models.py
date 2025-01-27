from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy
# ------------------------------------------------------------------------------------------------------------------------
from PIL import Image

# Myuser 

class MyUser(AbstractUser):
    phone = models.CharField(max_length=13, null=True, blank=True)
    photo = models.ImageField(upload_to='users/photo', null=True, blank=True)

    class Meta:
        verbose_name = "Foydalanuvchi "
        verbose_name_plural = "Foydalanuvchilar"
        ordering = ['id'] 

# Course model:
class Course(models.Model):
    # Title model: Kurs nomini kiritish uchun model. Maksimal 255 ta simvol kiritish mumkin;
    title = models.CharField(max_length=255)
    # Description model: Kurs haqida ma`lumot kiritish uchun model. Maksimal 255 ta simvol kiritish mumkin;
    description = models.TextField(max_length=1000)
        
    def __str__(self):
        return self.title
    
    def get_absolut_url(self):
        return reverse_lazy('course', kwargs={'course_id':self.pk})
# ------------------------------------------------------------------------------------------------------------------------

# Group model:
class Group(models.Model):
    # Title model: Guruh nomini kiritish uchun model. Maksimal uzunligi 255 ta simvol;
    title = models.CharField(max_length=255)
    # Teacher model: O`qituvchi ismini kiritish uchun model. Maksimal uzunligi 255 ta simvol. Bo`sh qoldirish mumkin;
    teacher = models.CharField(max_length=255, null=True, blank=True)
    # Course type model: Kurs turini ko`rsatish uchun model. Maksimal uzunligi 255 ta simvol. Bo`sh qoldirish mumkin;
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='groups')
    # Student count model: Guruhdagi o`quvchilar sonini kiritish uchun model (Integer ma`lumot kiritladi, default=0); 
    student_count = models.IntegerField(default=0)
    # Created at model: Guruh yaratilgan vaqtni saqlash uchun model. Bo`sh qoldirish mumkin;
    created_at = models.DateTimeField(auto_now_add=True)
    # Update at model: Guruh oxirgi marta yangilangan vaqtni saqlash uchun model. Bo`sh qoldirish mumkin;
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_absolut_url(self):
        return reverse_lazy('group_by_course', kwargs={'group_id':self.pk})
    
    class Meta:
        verbose_name = "Guruh"
        verbose_name_plural = "Guruhlar"
        ordering = ['-id']
# ------------------------------------------------------------------------------------------------------------------------

# Lesson model:
class Lesson(models.Model):
    # Title model: Dars mavzusini kiritish uchun model. Maksimal 255 ta simvol kiritish mumkin ;
    title = models.CharField(max_length=255)
    # Teacher model: O`qituvchi ismini kiritish uchun model. Maksimal 255 ta simvol kiritish mumkin . Bo`sh qoldirish mumkin;
    teacher = models.CharField(max_length=255, null=True, blank=True)
    # Content model: Dars mavzusi haqida ma`lumot kiritish uchun model. Simvol yozishda cheklov yo`q;
    content = models.TextField()
    # Duration model: Dars davomiyligini kiritish uchun model. Bo`sh qoldirish mumkin;
    duration = models.DurationField(blank=True, null=True)
    # Created_at model: Dars yaratilgan vaqtni avtomatik tarzda saqlash uchun model; 
    created_at = models.DateField(auto_now_add=True)
    # Course model: Ushbu dars tegishli bo‘lgan kurs bilan bog‘lash uchun ForeignKey. Kurs o`chirilganda, dars ham o`chiriladi;
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='lessons')

    def __str__(self):
        return self.title
    
    def get_absolut_url(self):
        return reverse_lazy('lesson_detail', kwargs={'lesson_id':self.pk})
    
    class Meta:
        verbose_name = "Dars"
        verbose_name_plural = "Darslar"
        ordering = ['-id']
# ------------------------------------------------------------------------------------------------------------------------

# Student model:
class Student(models.Model):
    # Name model: O`quvchi ismini kiritish uchun model. Maksimal 255 ta simvol kiritish mumkin;
    name = models.CharField(max_length=255)
    # Email model: Talabani emailini kiritish uchun model. Maksimal 255 ta simvol kiritish mumkin;
    email = models.CharField(max_length=255)
    # Enrolled at model: O`quvchi bu guruhga qachon ro`yxatdan o`tganini kiritish uchun model;
    enrolled_at = models.DateField(blank=True, null=True, auto_now_add=True)
    # Group model: Group modeliga bog`lanadi. Agar bu o`quvchiga ulangan guruh o`chirilsa, o`quvchi haqida ma`lumot o`chirilib yuboriladi;
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "O`quvchi"
        verbose_name_plural = "O`quvchilar"
        ordering = ['-id']
# ------------------------------------------------------------------------------------------------------------------------
    
# Comment model:  
class Comment(models.Model):
    # Text model: Dars uchun o`quvchi tomonidan qo`yilishi uchun izoh matnini kiritish uchun model;
    text = models.TextField(max_length=1000)
    # Author: Izoh qoldirgan o`qituvchi yoki o`quvchini avtomatik tarzda kirituvchi uchun model;
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    # Lesson model: Izoh qaysi darsga qoldirilganligini avtomatik tarzda kirituvchi model;
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    # Created model: Izoh qachon qoldirilganligini avtomatik tarzda kirituvchi model;
    created = models.DateTimeField(auto_now_add=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Izoh "
        verbose_name_plural = "Izohlar"
        ordering = ['-id']
# ------------------------------------------------------------------------------------------------------------------------

# Message model
class Message(models.Model):
    # Subject model: 
    subject = models.CharField(max_length=255, blank=True, null=True)
    # Message model: 
    message = models.TextField(max_length=1000)
    # To_user: Xabar kimgaligi
    to_user = models.CharField(max_length=255)
    # From model: Xabar egasi
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)


# ------------------------------------------------------------------------------------------------------------------------






























