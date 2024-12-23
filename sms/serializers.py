from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = ['id', 'subject', 'details', 'syllabus_link', 'total_classes', 'remaining_attendance']

class GradeSerializer(serializers.ModelSerializer):
    curriculums = CurriculumSerializer(many=True, read_only=True)

    class Meta:
        model = Grade
        fields = ['id', 'grade', 'image', 'curriculums']

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested user data
    grade = serializers.StringRelatedField()  # Shows grade name instead of ID

    class Meta:
        model = Student
        fields = '__all__'

class ParentSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()  # Shows student's name instead of ID

    class Meta:
        model = Parent
        fields = '__all__'

class FeeChallanSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()  # Shows student's name instead of ID

    class Meta:
        model = FeeChallan
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested user data

    class Meta:
        model = Teacher
        fields = '__all__'

class TeacherGradeCurriculumSerializer(serializers.ModelSerializer):
    teacher = serializers.StringRelatedField()
    grade = serializers.StringRelatedField()
    curriculum = serializers.StringRelatedField()

    class Meta:
        model = TeacherGradeCurriculum
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class QuizSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    teacher = serializers.StringRelatedField()
    curriculum = serializers.StringRelatedField()

    class Meta:
        model = Quiz
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class RetailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retailer
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class SemesterActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SemesterActivity
        fields = ['id', 'activity', 'date']  # Include only the relevant fields


class SemesterSerializer(serializers.ModelSerializer):
    activities = SemesterActivitySerializer(many=True, read_only=True)

    class Meta:
        model = Semester
        fields = ['id', 'name', 'session', 'activities']

