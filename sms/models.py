from django.db import models
from django.utils import timezone

from django.db import models

class User(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ]
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    contact_no = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.username


class Grade(models.Model):
    grade = models.CharField(max_length=50, default='2024')
    image = models.ImageField(upload_to='curriculum_images/')

    def __str__(self):
        return self.grade
    
class Curriculum(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='curriculums')
    subject = models.CharField(max_length=100, null=True)
    details = models.TextField()
    syllabus_link = models.URLField(max_length=200, blank=True)
    total_classes = models.IntegerField(default=12)
    remaining_attendance = models.IntegerField(default=12)

    def __str__(self):
        return f"{self.grade.grade} - {self.subject}"

class Content(models.Model):
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name='contents')
    week = models.PositiveIntegerField()
    description = models.TextField()

    def __str__(self):
        return f"Week {self.week}: {self.description[:50]}..."    
        
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField()
    gender = models.CharField(max_length=1)  # 'M' or 'F'
    address = models.CharField(max_length=100)
    admission_date = models.DateField()
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, related_name='students')
    

class Parent(models.Model):
    RELATION_CHOICES = [
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('guardian', 'Guardian'),
    ]

    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        related_name='parents'
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    relation = models.CharField(max_length=10, choices=RELATION_CHOICES)
    contact_no = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.relation.capitalize()} of {self.student.first_name} {self.student.last_name}"


class FeeChallan(models.Model):
    CHALLAN_MONTH_CHOICES = [
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    ]
    challan_title = models.CharField(max_length=100)
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='fee_challans'
    )
    month = models.CharField(max_length=20, choices=CHALLAN_MONTH_CHOICES)
    due_date = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Challan {self.challan_id} for {self.student.first_name} {self.student.last_name}"


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField()
    gender = models.CharField(max_length=1)  # 'M' or 'F'
    address = models.CharField(max_length=100)
    hire_date = models.DateField()
    Subject=models.CharField(max_length=50, default='Computer Science')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# to mark which teacher teaches which subject of which grade
class TeacherGradeCurriculum(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_grade_curriculums')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='grade_teacher_curriculums')
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name='curriculum_teacher_grades')

    class Meta:
        unique_together = ('teacher', 'grade', 'curriculum')

    def __str__(self):
        return f"{self.teacher.first_name} teaches {self.curriculum.subject} to Grade {self.grade.grade}"


class Attendance(models.Model):
    teacher_grade_curriculum = models.ForeignKey( TeacherGradeCurriculum, on_delete=models.CASCADE, related_name='attendances' )
    date = models.DateField(auto_now_add=True) 
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    is_present = models.BooleanField(default=True)

    def __str__(self):
        return f"Attendance for {self.student} on {self.date}"


class Quiz(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quizzes')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='quizzes')
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name='quizzes')
    total_marks = models.PositiveIntegerField()
    obtained_marks = models.PositiveIntegerField()
    grade = models.CharField(max_length=2)  # E.g., A+, A, B, etc.
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.curriculum.subject} ({self.grade})"



class Event(models.Model):
    title = models.CharField(max_length=200, default='No title.')
    date = models.DateField(null=True)  # Allow null values
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    location = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField()
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email} - {self.phone} - {self.submitted_at}"
    

class Retailer(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name} {self.region} {self.city} {self.address} {self.phone}'    
    

class Job(models.Model):
    title = models.CharField(max_length=255)
    total_positions = models.IntegerField()
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    education_qualification = models.CharField(max_length=255)
    required_experience = models.CharField(max_length=255)
    preferred_gender = models.CharField(max_length=50)
    travelling = models.CharField(max_length=50)
    apply_by = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.title    
    
# table for semester calendar 
class Semester(models.Model):
    name = models.CharField(max_length=100) 
    session = models.CharField(max_length=100,default='2024') 

    def __str__(self):
        return f"{self.name} ({self.session})"


class SemesterActivity(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="activities")
    activity = models.CharField(max_length=255) 
    date = models.CharField(max_length=255) 

    def __str__(self):
        return f"{self.activity} - {self.date}"    
    
    