from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import auth
from .models import *
from django.shortcuts import redirect

USER = get_user_model()

# Create your views here.
def home(request):
    return render(request,"home.html")

def courses(request):
    return HttpResponse("Courses Page!")

def instructors(request):
    return HttpResponse("Instructors Page!")

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            name = str(request.user.first_name)+" "+str(request.user.last_name)
            messages.success(request,"Successfully logged in as %s!" %name)
            return redirect('/')
        else:
            messages.success(request,"Incorrect credentials, Try again!")
            return render(request,'login.html')
    else:
        return render(request, 'login.html')

def logout(request):
    return HttpResponse("Logout Page")

def registerStudent(request):
    if request.method == "POST":
        f_name = request.POST.get('fname')
        l_name = request.POST.get('lname')
        username = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        DOB = request.POST.get('DOB')
        qual = request.POST.get('qualification')
        sex = request.POST.get('sex')
        if password1 == password2:
            user_form = USER.objects.create_user(username=username,password=password1,email=username,first_name=f_name,last_name=l_name)
            form = Student.objects.create(fname=f_name,lname=l_name,email=username,qualification=qual,sex=sex,DOB=DOB)
            user_form.save()
            form.save()
            messages.success(request,"Succesfully registered as Student! you can Sign in now")
            return redirect('/')
        else:
            messages.success(request,"Error in credentials! please re-enter values")
            return redirect('registerStudent')
    else:
        return render(request,'registerStudent.html')

def registerInstructor(request):
    if request.method == "POST":
        f_name = request.POST['fname']
        l_name = request.POST.get('lname')
        username = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        DOB = request.POST.get('DOB')
        qual = request.POST.get('qualification')
        sex = request.POST.get('sex')
        if password1 == password2:
            user_form = USER.objects.create_user(username=username,password=password1,email=username,first_name=f_name,last_name=l_name)
            form = Instructor.objects.create(fname=f_name,lname=l_name,email=username,qualification=qual,sex=sex,DOB=DOB)
            user_form.save()
            form.save()
            messages.success(request,"Succesfully registered as Instructor! you can Sign in now")
            return redirect('/')
        else:
            messages.success(request,"Error in credentials! please re-enter values")
            return redirect('registerInstructor')
    else:
        return render(request, 'registerInstructor.html')

def profile(request):
    return HttpResponse("Profile")

def deleteStudentCourse(request, course_id):
    return HttpResponse("Deleted Student Course:"+str(course_id))

def profileDelete(request):
    return HttpResponse("Profile Delete")

def profileUpdate(request):
    return HttpResponse("Profile Update")

def createCourse(request):
    return HttpResponse("Create Course")

def deleteInstructorCourse(request, course_id):
    return HttpResponse("Deleted Instructor Course:"+str(course_id))

def myCourse(request):
    return HttpResponse("My Course")

def enroll(request, course_id):
    return HttpResponse("Enroll Course is "+str(course_id))

def sampleCertificate(request):
    return HttpResponse("Sample Certificate")

def termsOfUse(request):
    return HttpResponse("Terms of Use")

def contactUs(request):
    return HttpResponse("Contact Us")




