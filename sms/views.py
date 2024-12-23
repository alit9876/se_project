from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from .form import ContactForm, SignInForm
from .models import *
from itertools import groupby
from django.db import IntegrityError
from django.contrib import messages
from django.http import JsonResponse
import datetime
import requests
from django.conf import settings
from .api_views import *


# website main pagw

def home_view(request):
    request.session.flush()
    return render(request, 'sms_app/website/home.html')

def about_view(request):
    return render(request, 'sms_app/website/about.html')

def academic_view(request):
    return render(request, 'sms_app/website/academics.html')

def student_view(request):
    return render(request, 'sms_app/website/student.html')

def retailer_view(request):
    api_url = "http://127.0.0.1:8000/api/retailers/"
    response = requests.get(api_url)
    if response.status_code == 200:
        retailers = response.json() 
    else:
        retailers = []  # Fallback if API request fails
    return render(request, 'sms_app/website/retailer.html', {'retailers': retailers})


def event_view(request):
    api_url = "http://127.0.0.1:8000/api/events/"
    response = requests.get(api_url)
    if response.status_code == 200:
        events = response.json()  
    else:
        events = []  
    return render(request, 'sms_app/website/events.html', {'events': events})

def admission_view(request):
    return render(request, 'sms_app/website/admission.html')

def alumni_view(request):     # does not proivde me any link now
    return render(request, 'sms_app/website/alumni.html')

def academic_calendar_view(request):
    api_url = "http://127.0.0.1:8000/api/semesters/"
    response = requests.get(api_url).json()
    return render(request, 'sms_app/website/academic_calendar.html', {'semesters': response})

def campuses_view(request):
    return render(request, 'sms_app/website/Campuses.html')

def co_curricular_view(request):  
    return render(request, 'sms_app/website/co_curricular.html')

def curriculum_view(request):
    api_url = "http://127.0.0.1:8000/api/grades/"
    response = requests.get(api_url).json()
    return render(request, 'sms_app/website/curriculum.html', {'grouped_data': response} )

def offered_subject_view(request):
    grade_data = {}
    api_url = "http://127.0.0.1:8000/api/teacher-grade-curriculums/"
    response = requests.get(api_url).json()

    # Process API response
    for item in response:
        grade = item.get('grade')
        curriculum = item.get('curriculum').split(' - ')[-1]  # Extract subject from curriculum
        teacher = item.get('teacher')

        if grade not in grade_data:
            grade_data[grade] = []
        grade_data[grade].append({'subject': curriculum, 'teacher': teacher})

    context = {'grade_data': grade_data}
    return render(request, 'sms_app/website/offered_subjects.html', context)

def careers_view(request):
    api_url = "http://127.0.0.1:8000/api/jobs/"
    response = requests.get(api_url)
    if response.status_code == 200:
        jobs = response.json()  
    else:
        jobs = []  
    return render(request, 'sms_app/website/careers.html', {'jobs': jobs,})

def login_view(request):    
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(username=username)
                if user.password == password: 
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    request.session['role'] = user.role
                    if user.role == 'admin':
                        return redirect("admin_dashboard")
                    elif user.role == 'student':
                        return redirect('student_dashboard') 
                    elif user.role == 'teacher':
                         return redirect('teacher_dashboard')    
                else:
                    form.add_error('password', 'Invalid password')
            except User.DoesNotExist:
                form.add_error('username', 'Username does not exist')
    else:
        form = SignInForm()
    return render(request, 'sms_app/website/signup_signin.html', {'form': form})

def logout_view(request):
    request.session.flush()  # Clears the session
    return redirect('login')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'],
                'phone': form.cleaned_data.get('phone', ''),  # Optional field
                'message': form.cleaned_data['message']
            }
            api_url = 'http://127.0.0.1:8000/api/contact/'
            response = requests.post(api_url, json=data)
            if response.status_code == 201:  # Successfully created
                messages.success(request, "Your response has been recorded successfully!")
            else:
                messages.error(request, f"API Error: {response.json()}")    
            return redirect('contact_us')
    else:
        form = ContactForm()
    
    return render(request, 'sms_app/website/contact.html', {'form': form})

# views for teacher dashboard
def teacherDashboard_view(request):
    user =  User.objects.get(id=request.session['user_id']) 
    teacher = Teacher.objects.get(user=user)
    return render(request, 'sms_app/TeacherDashboard/teacherDashboard.html', {'teacher': teacher })

def attendance_view(request):
    user_id = request.session.get('user_id')
    teacher = get_object_or_404(Teacher, user__id=user_id)
    teacher_grade_curriculums = TeacherGradeCurriculum.objects.filter(teacher=teacher)
    grades = Grade.objects.filter(id__in=teacher_grade_curriculums.values_list('grade_id', flat=True))
    curriculums = Curriculum.objects.filter(id__in=teacher_grade_curriculums.values_list('curriculum_id', flat=True))
    selected_grade_id = request.GET.get('grade')
    selected_curriculum_id = request.GET.get('curriculum')
    students = Student.objects.filter(grade_id=selected_grade_id) if selected_grade_id else []

    if request.method == "POST":
        curriculum_id = request.POST.get('teacher_grade_curriculum_id')
        teacher_grade_curriculum = get_object_or_404(TeacherGradeCurriculum, curriculum_id=curriculum_id)
        curriculum = teacher_grade_curriculum.curriculum

        if curriculum.remaining_attendance <= 0:
            messages.error(request, f"Attendance for the subject '{curriculum.subject}' in Grade {curriculum.grade.grade} has already been completed.")
            return redirect('attendance_view')

        for key, value in request.POST.items():
            if key.startswith('attendance'):
                student_id = key.replace('attendance', '')
                student = get_object_or_404(Student, id=student_id)
                is_present = value == 'present'

                Attendance.objects.create(
                    teacher_grade_curriculum=teacher_grade_curriculum,
                    student=student,
                    is_present=is_present
                )
        curriculum.remaining_attendance -= 1
        curriculum.save()
        messages.success(request, "Attendance has been recorded successfully!")
        return redirect('teacher_dashboard')

    context = {
        'grades': grades,
        'curriculums': curriculums,
        'students': students,
        'selected_grade_id': selected_grade_id,
        'selected_curriculum_id': selected_curriculum_id,
    }
    return render(request, 'sms_app/TeacherDashboard/attendance.html', context)


def grading_view(request):
    user_id = request.session.get('user_id')
    teacher = get_object_or_404(Teacher, user__id=user_id)

    teacher_grade_curriculums = TeacherGradeCurriculum.objects.filter(teacher=teacher)
    grades = Grade.objects.filter(id__in=teacher_grade_curriculums.values_list('grade_id', flat=True))
    curriculums = Curriculum.objects.filter(id__in=teacher_grade_curriculums.values_list('curriculum_id', flat=True))
    selected_grade_id = request.GET.get('grade')
    selected_curriculum_id = request.GET.get('curriculum')
    students = Student.objects.filter(grade_id=selected_grade_id) if selected_grade_id else []

    if request.method == "POST":
        curriculum_id = request.POST.get('curriculum')
        if not curriculum_id:
            print(request, "Please select a valid curriculum.")
            return redirect(request.path_info)

        try:
            for student_id in request.POST.getlist('student_ids'):
                total_marks = request.POST.get(f'total_marks_{student_id}')
                obtained_marks = request.POST.get(f'obtained_marks_{student_id}')
                grade = request.POST.get(f'grade_{student_id}')

                if not all([total_marks, obtained_marks, grade]):
                    print(request, f"Missing data for student {student_id}.")
                    return redirect(request.path_info)
                Quiz.objects.create(
                    student_id=int(student_id),
                    teacher=teacher,
                    curriculum_id=int(curriculum_id),
                    total_marks=int(total_marks),
                    obtained_marks=int(obtained_marks),
                    grade=grade,
                )
            messages.success(request, "Grades have been uploaded successfully!")
            return redirect('teacher_dashboard')
        except (IntegrityError, ValueError) as e:
            print(request, f"Error saving grades: {e}")
            return redirect(request.path_info)
    context = {
        'grades': grades,
        'curriculums': curriculums,
        'students': students,
        'selected_grade_id': selected_grade_id,
        'selected_curriculum_id': selected_curriculum_id,
    }
    return render(request, 'sms_app/TeacherDashboard/grading.html', context)


def manage_curriculum_view(request):
    user_id = request.session.get('user_id')
    teacher = get_object_or_404(Teacher, user__id=user_id)
    teacher_curriculums = TeacherGradeCurriculum.objects.filter(teacher=teacher)

    grade_curriculum_students = {}
    for tc in teacher_curriculums:
        students = Student.objects.filter(grade=tc.grade)
        grade_curriculum_students[tc] = students

    context = {
        'teacher': teacher,
        'grade_curriculum_students': grade_curriculum_students,
    }
    return render(request, 'sms_app/TeacherDashboard/managecurriculum.html', context)



# student dashboard

def student_dashboard(request):
    user_id = request.session.get('user_id')

    user = User.objects.get(id=user_id)
    student = None
    parents = None

    if user.role == 'student':
        student = Student.objects.select_related('grade').filter(user=user).first()
        parents = Parent.objects.filter(student=student)
    context = {
        'user': user,
        'student': student,
        'parents': parents[0],
    }
    return render(request, 'sms_app/studentDashboard/studentDashboard.html', context)

def attendance_display_view(request):
    user_id = request.session.get('user_id')
    student = get_object_or_404(Student, user_id=user_id)
    student_grade = student.grade
    curriculums_for_grade = Curriculum.objects.filter(grade=student_grade)
    attendance_data = []

    for curriculum in curriculums_for_grade:
        print(f"first curriculum : {curriculum}")
        attendance_record = Attendance.objects.filter(student=student,teacher_grade_curriculum__curriculum=curriculum).first()
        teacher = TeacherGradeCurriculum.objects.filter(curriculum=curriculum).first()
        if attendance_record:
            total_classes = curriculum.total_classes - curriculum.remaining_attendance
            attended_classes = Attendance.objects.filter(student=student,teacher_grade_curriculum__curriculum=curriculum,is_present=True).count()
            attendance_percentage = round((attended_classes / total_classes) * 100, 2) if total_classes > 0 else 0
            attendance_data.append({
                'teacher_name': f"{teacher.teacher.first_name} {teacher.teacher.last_name}" if teacher else 'No teacher assigned yet',
                'curriculum_subject': curriculum.subject,
                'attendance_percentage': attendance_percentage,
                'remaining_classes': curriculum.remaining_attendance,
                'attendance_exists': True,
                'curriculum_id': curriculum.id,  
            })
        else:
            attendance_data.append({
                'teacher_name': f"{teacher.teacher.first_name} {teacher.teacher.last_name}" if teacher else 'No teacher assigned yet',
                'curriculum_subject': curriculum.subject,
                'attendance_percentage': 0,
                'remaining_classes': curriculum.remaining_attendance,
                'attendance_exists': False,
                'curriculum_id': curriculum.id,
            })
    context = {
        'student': student,
        'attendance_data': attendance_data,
    }
    return render(request, 'sms_app/studentDashboard/attendance_display.html', context)

def attendance_more_info_view(request, curriculum_id):
    user_id = request.session.get('user_id')
    
    student = get_object_or_404(Student, user_id=user_id)
    # Fetch curriculum details
    curriculum = get_object_or_404(Curriculum, id=curriculum_id)
    
    # Determine the teacher and their information
    teacher_grade_curriculum = TeacherGradeCurriculum.objects.filter(curriculum=curriculum).first()
    teacher_name = f"{teacher_grade_curriculum.teacher.first_name} {teacher_grade_curriculum.teacher.last_name}" if teacher_grade_curriculum else "No teacher assigned"
    teacher_email = teacher_grade_curriculum.teacher.user.username if teacher_grade_curriculum else "N/A"

    # Fetch and group content by week
    contents = Content.objects.filter(curriculum=curriculum).order_by('week')
    content_by_week = {}
    for content in contents:
        content_by_week.setdefault(content.week, []).append(content.description)

    # Render the template with context
    context = {
        'student': student,
        'subject_name': curriculum.subject,
        'teacher_name': teacher_name,
        'teacher_email': teacher_email,
        'content_by_week': content_by_week,
    }
    return render(request, 'sms_app/studentDashboard/courseinfo.html', context)


def display_grades_view(request):
    user_id = request.session.get('user_id')
    student = get_object_or_404(Student, user_id=user_id)
    quizzes = []
    quizzes = Quiz.objects.filter(student__user__id=user_id)
    for quiz in quizzes:
        quiz.percentage = (quiz.obtained_marks / quiz.total_marks) * 100
        quiz.status = 'Pass' if quiz.percentage >= 50 else 'Fail'

    context = {
        'quizzes': quizzes,
        'student': student
    }
    return render(request, 'sms_app/studentDashboard/displayGrades.html', context)


def onlinefee_view(request):
    user_id = request.session.get('user_id')
    student = get_object_or_404(Student, user_id=user_id)
    challans = FeeChallan.objects.filter(student__user_id=user_id)
    
    context = {
        'student' : student,
        'challans' : challans
    }
    return render(request, 'sms_app/studentDashboard/Feepayment.html', context)

def pay_challan(request, challan_id):
    user_id = request.session.get('user_id')
    student = get_object_or_404(Student, user_id=user_id)
    challan = get_object_or_404(FeeChallan, id=challan_id)
    challan.is_paid = True
    challan.save()
    context = {
        'student' : student
    }
    return redirect('sms_app/studentDashboard/Feepayment.html', context)

# search bar of main page....

def search_suggestions_view(request):
    pages = {
        "home": "",
        "about": "About/",
        "academics": "Academics/",
        "contact us": "Contact Us/",
        "student": "Student/",
        "offered subjects": "Student/Offered Subject",
        "clubs and activities": "Student/Clubs & Activities",
        "uniform retailer": "Online Uniform Retailer/",
        "news and events": "News & Events/",
        "admission": "Admission/",
        "careers": "Careers/",
        "alumni": "Alumni/",
        "login": "login/",
        "logout": "logout/",
        "academic calendar": "Admission/Academic Calendar/",
        "campuses": "Admission/Campuses/",
        "curriculum": "Admission/Curriculum/",
    }

    query = request.GET.get('q', '').lower()
    matching_pages = {name: url for name, url in pages.items() if query in name.lower()}
    return JsonResponse({"results": list(matching_pages.items())})

def search_view(request):
    pages = {
        "home": "",
        "about": "About/",
        "academics": "Academics/",
        "contact us": "Contact Us/",
        "student": "Student/",
        "offered subjects": "Student/Offered Subject",
        "clubs and activities": "Student/Clubs & Activities",
        "uniform retailer": "Online Uniform Retailer/",
        "news and events": "News & Events/",
        "admission": "Admission/",
        "careers": "Careers/",
        "alumni": "Alumni/",
        "login": "login/",
        "logout": "logout/",
        "academic calendar": "Admission/Academic Calendar/",
        "campuses": "Admission/Campuses/",
        "curriculum": "Admission/Curriculum/",
    }

    query = request.GET.get('q', '').lower()
    if query in pages:
        return redirect(pages[query])
    else:
        return redirect('home')



# view for admin dashboard

def admin_dashboard(request):
    return render(request, 'sms_app/adminDashboard/AdminDashboard.html')

def manage_teacher_view(request):
    teacher_grade_curriculums = TeacherGradeCurriculum.objects.select_related('teacher', 'grade', 'curriculum').all()    
    
    context = {
        'teacher_grade_curriculums': teacher_grade_curriculums
    }
    return render(request, 'sms_app/adminDashboard/teacher_manage.html', context)
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def edit_teacher_saves(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        contact_no = request.POST.get('contact_no')
        password = request.POST.get('password')

        # Fetch the teacher record
        teacher = get_object_or_404(Teacher, id=teacher_id)

        # Update teacher details
        teacher.first_name = first_name
        teacher.last_name = last_name
        teacher.contact_no = contact_no
        if password:  # Update password only if provided
            user = teacher.user
            user.password = (password)
            user.save()

        teacher.save()

        messages.success(request, "Teacher details updated successfully!")
        return redirect('manage_teacher')  # Replace 'teacher_list' with your list view name
    else:
        messages.error(request, "Invalid request method.")
        return redirect('manage_teacher')  # Replace with an appropriate fallback


@csrf_protect
def edit_student_save(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        contact_no = request.POST.get('contact_no')
        password = request.POST.get('username')

        # Fetch the teacher record
        teacher = get_object_or_404(Student, id=teacher_id)

        # Update teacher details
        teacher.first_name = first_name
        teacher.last_name = last_name
        teacher.contact_no = contact_no
        if password:  # Update password only if provided
            user = teacher.user
            user.password = (password)
            user.save()

        teacher.save()

        messages.success(request, "Student details updated successfully!")
        return redirect('student_manage')  # Replace 'teacher_list' with your list view name
    else:
        messages.error(request, "Invalid request method.")
        return redirect('student_manage')  # Replace with an appropriate fallback

from datetime import date
def generate_challans_view(request):
    grades = Grade.objects.all()
    months = FeeChallan.CHALLAN_MONTH_CHOICES
    fee_challans = FeeChallan.objects.select_related('student', 'student__grade').all()
    context = {
        'grades': grades,
        'months': months,
        'fee_challans': fee_challans
    }
    if request.method == "POST":
        grade_id = request.POST.get("grade")
        month = request.POST.get("month")
        amount = request.POST.get("amount")
        
        try:
            grade = Grade.objects.get(id=grade_id)
            students = grade.students.all()

            for student in students:
                # Create the FeeChallan
                FeeChallan.objects.create(
                    challan_title=f"Challan for {student.first_name} {student.last_name}",
                    student=student,
                    month=month,
                    total=amount,
                    due_date=date.today(),  # Replace with the actual due date logic
                )
            context['success'] = "Challans have been successfully generated."
        except Grade.DoesNotExist:
            context['error'] = "Selected grade does not exist."
        except Exception as e:
            context['error'] = f"An error occurred: {str(e)}"

        return redirect('fee_view')
    return render(request, 'sms_app/adminDashboard/feepayment.html', context)

def edit_challan(request):
    challan_id = request.POST.get('challan_id')
    challan = get_object_or_404(FeeChallan, id=challan_id)
    if request.method == 'POST':
        # Process the form submission
        amount = request.POST.get('amount')
        is_paid = request.POST.get('is_paid')
        challan.total = amount
        challan.is_paid = is_paid == "True"  # Convert to boolean
        challan.save()
        return redirect('fee_view')  # Redirect to the list page (or any desired page
    return redirect('fee_view')

def student_manage_view(request):
    students = Student.objects.select_related('user', 'grade').all()
    return render(request, 'sms_app/adminDashboard/student_manage.html', {'students': students})

from django.utils.timezone import now

def add_student_manage(request):
    if request.method == "POST":
        default_password = 'abc'
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        contact_no = request.POST['contact_no']
        gender = request.POST['gender']
        dob = request.POST['dob']
        grade_id = request.POST['grade']
        father_first_name = request.POST['father_first_name']
        father_last_name = request.POST['father_last_name']
        father_contact_no = request.POST['father_contact_no']

        # Create User instance
        user = User.objects.create(
            username=email,
            password=default_password,  # Replace with proper hashing
            role="student",
            contact_no=contact_no
        )
        # Get Grade
        grade = Grade.objects.get(id=grade_id)
        # Create Student instance
        student = Student.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            dob=dob,
            gender=gender,
            grade=grade,
            admission_date=now()  # Set the current date
        )
        # Create Parent instance
        Parent.objects.create(
            student=student,
            first_name=father_first_name,
            last_name=father_last_name,
            relation="father",
            contact_no=father_contact_no
        )
        return redirect('student_manage')  # Replace with your success URL
    else:
        grades = Grade.objects.all()
        return render(request, 'sms_app/adminDashboard/Admission_page.html', {'grades': grades})


from django.http import JsonResponse
import json
def update_student(request, student_id):
   if request.method == "POST":
      data = json.loads(request.body)
      student = Student.objects.get(id=student_id)
      student.first_name, student.last_name = data["name"].split(' ', 1)
      student.grade.grade = data["studentClass"]
      student.user.username = data["email"]
      student.save()
      return JsonResponse({"success": True})
   return JsonResponse({"success": False})


from django.db import transaction

def add_teacher_manage(request):
    grades = Grade.objects.all()
    selected_grade_id = request.POST.get('grade')
    curriculums = []

    # Fetch curriculums of the selected grade that are not assigned to any teacher
    if selected_grade_id:
        curriculums = Curriculum.objects.filter(
            grade_id=selected_grade_id
        ).exclude(
            id__in=TeacherGradeCurriculum.objects.filter(grade_id=selected_grade_id).values_list('curriculum_id', flat=True)
        )

    if request.method == "POST" and "curriculum" in request.POST:
        try:
            # Validate required fields
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '').strip()
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            dob = request.POST.get('dob', '').strip()
            gender = request.POST.get('gender', '').strip()
            address = request.POST.get('address', '').strip()
            hire_date = request.POST.get('hire_date', '').strip()
            curriculum_id = request.POST.get('curriculum', '').strip()

            if not (username and password and first_name and last_name and dob and gender and address and hire_date and curriculum_id):
                raise ValueError("All fields are required.")

            # Create a new teacher with associated user
            with transaction.atomic():
                user = User.objects.create(
                    username=username,
                    password=password,
                    role='teacher',
                    contact_no=request.POST.get('contact_no', '').strip()
                )
                teacher = Teacher.objects.create(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    dob=dob,
                    gender=gender,
                    address=address,
                    hire_date=hire_date
                )
                # Assign the teacher to the selected curriculum and grade
                selected_curriculum = Curriculum.objects.get(id=curriculum_id)
                TeacherGradeCurriculum.objects.create(
                    teacher=teacher,
                    grade=selected_curriculum.grade,
                    curriculum=selected_curriculum
                )
            
            return redirect('manage_teacher')  # Replace with your success page URL

        except ValueError as e:
            error_message = str(e)
        except Curriculum.DoesNotExist:
            error_message = "Selected curriculum does not exist."
        except Exception as e:
            error_message = "An unexpected error occurred. Please try again."
    else:
        error_message = None

    return render(request, 'sms_app/adminDashboard/addTeacher.html', {
        'grades': grades,
        'curriculums': curriculums,
        'selected_grade_id': selected_grade_id,
        'error_message': error_message,
    })
