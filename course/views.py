from django.http.response import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Home page!")

def courses(request):
    return HttpResponse("Courses Page!")

def instructors(request):
    return HttpResponse("Instructors Page!")