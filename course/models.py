from django.db import models
import datetime
from django.utils import timezone
from django.db.models.deletion import CASCADE
from django.contrib.auth.decorators import *
from django.contrib.auth.models import AbstractUser, User
#from django.db.models import Q
#from datetime import time

# Create your models here.
SEX_CHOICE = [
    ('MALE', 'Male'),
    ('FEMALE', 'Female'),
    ('OTHER', 'Other'),
]

YEAR_IN_SCHOOL = [
    ('FR', 'Freshman'),
    ('SO', 'Sophomore'),
    ('JR', 'Junior'),
    ('SR', 'Senior'),
    ('GR', 'Graduate'),
]

INSTRUCTOR_QUALIFICATIONS = [
    ('TA', 'Teaching Assistant'),
    ('RA', 'Research Assistant'),
    ('AP', 'Assistant Professor'),
    ('SP', 'Senior Professor'),
    ('GR', 'Graduate'),
]

class User(AbstractUser):
    def is_student(self):
        if Student.objects.filter(email=self.email).exists():
            return True
        return False
    def is_instructor(self):
        if Instructor.objects.filter(email=self.email).exists():
            return True
        return False
    def enrolled_course_number(self):
        return StudentCourse.objects.filter(student__email__startswith=self.username).count()
    def course_number(self):
        return Course.objects.all().count()
    def inst_course(self):
        instructor = Instructor.objects.get(email=self.username)
        return instructor.course_set.all().count()

class Certifier(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return ('Name: '+ self.name + '  ,  ' + 'Certifier id: ' + str(self.id))

class Instructor(models.Model):
    sex = models.CharField(max_length=50, choices=SEX_CHOICE, null=False)
    fname = models.CharField(max_length=100,null=False)
    lname = models.CharField(max_length=100,blank=True)
    DOB = models.DateField(default='1900-01-01')
    qualification = models.CharField(max_length=2, choices=INSTRUCTOR_QUALIFICATIONS, default='GR', null=False)
    description = models.CharField(max_length=500)
    date_joined = models.DateField(default=datetime.date.today)
    email = models.EmailField(max_length=50,null=False)

    class Meta:
        unique_together = ('email', 'fname','lname')
        
    def age(self):
        dob = self.DOB
        tod = datetime.date.today()
        my_age = (tod.year - dob.year) - int((tod.month, tod.day) < (dob.month, dob.day))
        return my_age

    def __str__(self):
        return self.fname + ' ' + self.lname

class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    publish_date = models.DateTimeField(default=timezone.now)
    certifier = models.ForeignKey(Certifier, on_delete=CASCADE)
    instructor = models.ForeignKey(Instructor,on_delete=CASCADE)
        
    class Meta:
        unique_together = ('name', 'instructor',)
    
    def __str__(self):
        return ("Course Name: "+self.name+" , "+"Course Instructor: "+self.instructor.fname+" "+self.instructor.lname)

class Student(models.Model):
    fname = models.CharField(max_length=100,null=False)
    lname = models.CharField(max_length=100,blank=True)
    email = models.EmailField(max_length=50,null=False)
    DOB = models.DateField(default='1980-01-01')
    datejoined = models.DateField(default=datetime.date.today)
    qualification = models.CharField(max_length=2, choices=YEAR_IN_SCHOOL, default=None, null=False)
    sex = models.CharField(max_length=50, choices=SEX_CHOICE, default=None, null=False)
    
    class Meta:
        unique_together = ('email', 'fname','lname')
    
    def age(self):
        dob = self.DOB
        tod = datetime.date.today()
        my_age = (tod.year - dob.year) - int((tod.month, tod.day) < (dob.month, dob.day))
        return my_age

    def __str__(self):
        return ("Student Name: "+ self.fname + ' ' + self.lname + ' , ' + "Student EmailID: "+ self.email)

class StudentCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=CASCADE)
    student = models.ForeignKey(Student, on_delete=CASCADE)
    join_date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('course', 'student',)

    def __str__(self):
        return ("Course Name: "+ self.course.name + ' , ' + "Student Name: " + self.student.fname + ' ' + self.student.lname)


