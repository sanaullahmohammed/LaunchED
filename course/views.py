from django.http import request
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from .models import Course, Instructor, Certifier, Student, StudentCourse, User

USER = get_user_model()

def dateConvert(date):
    toConvert = date.split('/')
    return( toConvert[2]+'-'+toConvert[0]+'-'+toConvert[1])

# Create your views here.
def home(request):
    return render(request,"home.html")

def courses(request):
    course = Course.objects.all() 
    COURSE = {
        "courses":course 
    }
    return render(request, 'courses.html',COURSE)

def instructors(request):
    instructor = Instructor.objects.all()
    course = Course.objects.all()
    INSTRUCTOR = {
        "instructors":instructor,
        "courses":course
    }
    return render(request, 'instructors.html',INSTRUCTOR)

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

@login_required
def logout(request):
    auth.logout(request)
    messages.success(request,"You have successfully logged off!")
    return redirect("/")

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
            DOB = dateConvert(DOB)
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
        f_name = request.POST.get('fname')
        l_name = request.POST.get('lname')
        username = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        DOB = request.POST.get('DOB')
        qual = request.POST.get('qualification')
        sex = request.POST.get('sex')
        if password1 == password2:
            DOB = dateConvert(DOB)
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

@login_required
def profile(request):
    if request.user.is_student():
        student = Student.objects.get(email = request.user.username)
        courses = Course.objects.all()
        enrolled_courses = StudentCourse.objects.filter(student__email__startswith=request.user.username)
        context = {
            "Students": student,
            "Courses": courses,
            "enrolled": enrolled_courses,
        }
        return render(request,"profile.html",context)
    if request.user.is_instructor():
        instructor = Instructor.objects.get(email = request.user.username)
        courses = instructor.course_set.all()
        context = {
            "Instructors":instructor,
            "courses" : courses
        }
        return render(request,"profile.html", context)

@login_required
def deleteStudentCourse(request, course_id):
    course = StudentCourse.objects.get(pk=course_id)
    course.delete()
    return redirect('/profile')

@login_required
def profileDelete(request):
    if request.user.is_student():
        student=Student.objects.get(email = request.user.username)
        UsEr = User.objects.get(username = request.user.username)
        student.delete()
        UsEr.delete()
    if request.user.is_instructor():
        instructor=Instructor.objects.get(email = request.user.username)
        UsEr = User.objects.get(username = request.user.username)
        instructor.delete()
        UsEr.delete()
    messages.success(request,"Account successfully deleted, We're really sorry to see you leave us :'(  ")
    return redirect('/')

@login_required
def profileUpdate(request):
    if request.method == "POST":
        if request.user.is_student():
            curr_user=Student.objects.filter(email = request.user.username)
        if request.user.is_instructor():
            curr_user=Instructor.objects.filter(email = request.user.username)
        f_name = request.POST.get('fname')
        l_name = request.POST.get('lname')
        DOB = request.POST.get('DOB')
        qual = request.POST.get('qualification')
        if request.user.is_instructor():
            About = request.POST.get('About')
        if (len(DOB) == 0):
            messages.success(request,"DOB field cannot be empty!")
            return redirect('profileUpdate')
        else:
            DOB = dateConvert(DOB)
            form = curr_user.update(fname=f_name,lname=l_name,qualification=qual,DOB=DOB)
            if request.user.is_instructor():
                curr_user.update(description = About)
            form_user = USER.objects.filter(username = request.user.username)
            form_user.update(first_name=f_name, last_name=l_name)
            messages.success(request,"Successfully changed profile details")
            return redirect('/')
    else:
        return render(request,'profileUpdate.html')

@login_required
def createCourse(request):
    certifier = Certifier.objects.all()
    instructor = Instructor.objects.get(email = request.user.username)
    courses = instructor.course_set.all()
    context = {
            "certifier" : certifier,
            "Instructors":instructor,
            "courses" : courses
        }
    if request.method == "POST":
        course_name = request.POST.get('Cname')
        certifier = request.POST.get('Ccertifier')
        course_description = request.POST.get('Cdesc')
        if(len(course_name) == 0 and len(course_description) == 0):
            messages.success(request,"Invalid form, Please fill everyblock!")
            return redirect('createCourse')
        else:
            certifier_name = Certifier.objects.get(id=certifier)
            inst_name = Instructor.objects.get(email=request.user.username)
            form = Course.objects.create(name=course_name,description=course_description,certifier=certifier_name,instructor=inst_name)
            form.save()
        return redirect('/profile')

    return render(request,"createCourse.html",context)

@login_required
def deleteInstructorCourse(request, course_id):
    course = Course.objects.get(pk=course_id)
    course.delete()
    return redirect('/profile')

@login_required
def myCourse(request):
    student = Student.objects.get(email = request.user.username)
    courses = Course.objects.all()
    enrolled_courses = StudentCourse.objects.filter(student__email__startswith=request.user.username)
    context = {
            "Students": student,
            "Courses": courses,
            "enrolled": enrolled_courses,
        }
    if request.method == "POST":
        course_name = request.POST.get('Cname')
        c_id = Course.objects.get(id=course_name)
        s_name= Student.objects.get(email=request.user.username)
    return render(request,"myCourses.html",context)

@login_required
def enroll(request, course_id):
    course_id = Course.objects.get(id=course_id)
    student_id = Student.objects.get(email = request.user.username)
    if student_id.studentcourse_set.filter(course__id__contains=course_id.id).exists() == True:
        messages.success(request,"You are already enrolled in this course! select another one!")
        return redirect('/courses')
    else:
        form = StudentCourse.objects.create(course=course_id,student=student_id)
        form.save()
        return redirect('/profile')

def sampleCertificate(request):
    return render(request, "sampleCertificate.html")

def termsOfUse(request):
    return render(request, "termsOfUse.html")

def contactUs(request):
    return render(request, "contactUs.html")




