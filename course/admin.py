from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Course)
admin.site.register(Instructor)
admin.site.register(Certifier)
admin.site.register(Student)
admin.site.register(StudentCourse)
admin.site.register(User)