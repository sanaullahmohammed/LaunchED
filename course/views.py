from django.http.response import HttpResponse


# Create your views here.
def home(request):
    return HttpResponse("Home Page!")

def courses(request):
    return HttpResponse("Courses Page!")

def instructors(request):
    return HttpResponse("Instructors Page!")

def login(request):
    return HttpResponse("Login Page")

def logout(request):
    return HttpResponse("Logout Page")

def registerStudent(request):
    return HttpResponse("Register Student")

def registerInstructor(request):
    return HttpResponse("Register Instructor")

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




