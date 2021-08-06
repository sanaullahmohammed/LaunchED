from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('courses/', views.courses),
    path('instructors/', views.instructors),
    path('login/', views.login),
    path('logout/', views.logout),
    path('registerStudent/', views.registerStudent),
    path('registerInstructor/', views.registerInstructor),
    path('profile/',views.profile),
    path('profile/createCourse/',views.createCourse),
    path('profile/<int:course_id>/',views.deleteStudentCourse),
    path('profile/createCourse/<int:course_id>/',views.deleteInstructorCourse),
    path('profile/profileDelete/',views.profileDelete),
    path('profile/profileUpdate/',views.profileUpdate),
    path('profile/myCourses',views.myCourse),
    path('courses/<int:course_id>/', views.enroll),
    path('sampleCertificate/',views.sampleCertificate),
    path('termsOfUse/',views.termsOfUse),
    path('contactUs/',views.contactUs),
]