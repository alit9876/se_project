from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import *

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'grades', GradeViewSet)
router.register(r'curriculums', CurriculumViewSet)
router.register(r'contents', ContentViewSet)
router.register(r'students', StudentViewSet)
router.register(r'parents', ParentViewSet)
router.register(r'fee-challans', FeeChallanViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'teacher-grade-curriculums', TeacherGradeCurriculumViewSet)
router.register(r'attendances', AttendanceViewSet)
router.register(r'quizzes', QuizViewSet)
router.register(r'events', EventViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'retailers', RetailerViewSet)
router.register(r'jobs', JobViewSet)
router.register(r'semesters', SemesterViewSet)
router.register(r'semester-activities', SemesterActivityViewSet)

# list of urls 
urlpatterns = [
    path('api/', include(router.urls)),
    path('semesters/', SemesterListView.as_view(), name='semester-list'),
    path('api/contact/', ContactAPIView.as_view(), name='contact_api'),
    path('', home_view, name="home"),
    path('About/', about_view, name="about"),
    path('Academics/', academic_view, name="academics"),
    path('Contact Us/', contact_view, name="contact_us"),
    path('Student/', student_view, name="student"),
    path('Student/Offered Subject', offered_subject_view, name="offeredSubjects"),
    path('Student/Clubs & Activities', co_curricular_view, name="Cocurricular"),
    path('Online Uniform Retailer/', retailer_view, name="retailer"),
    path('News & Events/', event_view, name="event"),
    path('Admission/', admission_view, name="admission"),
    path('Careers/', careers_view, name="careers"),
    path('Alumni/', alumni_view, name="alumni"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('Admission/Academic Calendar/', academic_calendar_view, name="academic_calendar"),
    path('Admission/Campuses/', campuses_view, name="Campuses"),
    path('Admission/Curriculum/', curriculum_view, name="curriculum"),
    path('Admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('student-dashboard/', student_dashboard, name='student_dashboard'),
    path('Student-dashboard/Attendance/', attendance_display_view, name='student_dashboard_attendance'),
    path('Student-dashboard/Grades/', display_grades_view, name='student_dashboard_grades'),
    path('Student-dashboard/FeePayment/', onlinefee_view, name='student_dashboard_fee'),
    path('pay-challan/<int:challan_id>/', pay_challan, name='pay_challan'),
    path('Teacher-dashboard/', teacherDashboard_view, name='teacher_dashboard'),
    path('Teacher-dashboard/Attendance/', attendance_view, name='attendance'),
    path('Teacher-dashboard/Grading/', grading_view, name='grading'),
    path('Teacher-dashboard/Curriculum/', manage_curriculum_view, name='managecurriclum'),
    path('search/suggestions/', search_suggestions_view, name='search_suggestions'),
    path('search/', search_view, name='search'),
    #
    path('curriculum/<int:curriculum_id>/', attendance_more_info_view, name='curriculum_details'),
    path('Admin-dashboard/Teacher/', manage_teacher_view, name='manage_teacher'),
    path('Admin-dashboard/Teacher/Add Teacher/', add_teacher_manage, name='add_manage_teacher'),
    path('Admin-dashboard/Student/', student_manage_view, name='student_manage'),
    path('Admin-dashboard/FeePayment/', generate_challans_view, name='fee_view'),
    path('edit-challan/', edit_challan, name='update-challan'),
    path('Admin-dashboard/Student/Add Student/', add_student_manage, name='add_student_manage'),
    path('edit-teacher/', edit_teacher_saves, name='edit_teacher'),
    path('student-teacher/', edit_student_save, name='edit_student'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
