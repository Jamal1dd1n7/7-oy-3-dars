from django.urls import path
from .views import *

urlpatterns = [
    # URL with Generic views:
    # Home
    path('', HomeView.as_view(), name='home'),
    # ----------------------------------------------------------------------------------------------------------------------------------------------------

    # Course
    path('course/<int:course_id>/',CourseView.as_view(), name='course'),
    path('course/add/', AddCourseView.as_view(), name='add_course'),
    path('course/<int:course_id>/', UpdateCourseView.as_view(), name='update_course'),
    path('course/<int:course_id>/', DeleteCourseView.as_view(), name='delet_course'),
    # ----------------------------------------------------------------------------------------------------------------------------------------------------

    # Group
    path('group/<int:group_id>/', GroupView.as_view(), name='group_by_course'),
    path('group/add/', AddGroupView.as_view(), name='add_group'),
    path('course/<int:course_id>/', UpdateGroupView.as_view(), name='update_course'),
    path('course/<int:course_id>/', DeleteGroupView.as_view(), name='delete_course'),
    
    # Lesson
    path('lesson/<int:lesson_id>/', LessonDetail.as_view(), name='lesson_detail'),
    path('lesson/add/', AddLessonView.as_view(), name='add_lesson'),
    path('lesson/<int:lesson_id>/', UpdateLessonView.as_view(), name='update_lesson'),
    path('lesson/<int:lesson_id>/', DeleteLessonView.as_view(), name='delete_lesson'),

    # Message 
    path('message', SendMessage.as_view(), name='send_message'),
    # ----------------------------------------------------------------------------------------------------------------------------------------------------




    # URL with Functions:
    # Home 
    # path('', home, name='home'),
    # ----------------------------------------------------------------------------------------------------------------------------------------------------
    
    # Course
    # path('course/<int:course_id>/', course, name='course'),
    # path('course/add/', add_course, name='add_course'),
    # path('course/<int:course_id>/', update_course, name='update_course'),
    # path('course/<int:course_id>/', delete_course, name='delete_course'),
    # ----------------------------------------------------------------------------------------------------------------------------------------------------

    # Group
    # path('group/<int:group_id>/', group, name='group_by_course'),
    # path('group/add/', add_group, name='add_group'),
    # path('course/<int:course_id>/', update_course, name='update_course'),
    # path('course/<int:course_id>/', delete_course, name='delete_course'),


    # ----------------------------------------------------------------------------------------------------------------------------------------------------
   
    # Lesson
    # path('lesson/<int:lesson_id>/', lesson, name='lesson_detail'),
    # path('lesson/add/', add_lesson, name='add_lesson'),
    # path('lesson/<int:lesson_id>/', update_lesson, name='update_lesson'),
    # path('lesson/<int:lesson_id>/', delete_lesson, name='delete_lesson'),
    # ----------------------------------------------------------------------------------------------------------------------------------------------------
   
    # Comment
    path('lesson/<int:lesson_id>/comment/save/', comment_save, name='comment_save'),
    path('comment/<int:comment_id>/update/', comment_update, name='updateComment'),
    path('comment/<int:comment_id>/delete/', comment_delete, name='deleteComment'),
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 

    # Auth
    path('auth/register/', register, name='register'),
    path('auth/login/', loginPage, name='login'),
    path('auth/logout/', logoutPage, name='logout'),
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 

    # Errors
    path('404/', send_404, name='404'),

    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 

    # Message
    # path('message', send_message, name='send_message'),
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
]