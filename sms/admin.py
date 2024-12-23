from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'grade', 'image')
    search_fields = ('grade',)
    list_filter = ('grade',)
    ordering = ('grade',)


@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ('id', 'grade', 'subject', 'syllabus_link')
    search_fields = ('subject', 'details')
    list_filter = ('grade', 'subject')
    ordering = ('grade', 'subject')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "grade":
            kwargs["queryset"] = Grade.objects.all().order_by('grade')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'curriculum', 'week', 'short_description')
    search_fields = ('description', 'curriculum__subject', 'curriculum__grade__grade')
    list_filter = ('curriculum__grade', 'curriculum__subject', 'week')
    ordering = ('curriculum__grade', 'curriculum__subject', 'week')

    def short_description(self, obj):
        # Limit description to 50 characters for display
        return obj.description[:50] + ('...' if len(obj.description) > 50 else '')
    short_description.short_description = 'Description'

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'dob', 'gender', 'admission_date', 'grade')
    search_fields = ('user__username', 'first_name', 'last_name', 'grade__grade')
    list_filter = ('grade',)

    def save_model(self, request, obj, form, change):
        if not obj.user_id:  
            user = User.objects.create(
                username=obj.first_name.lower() + str(obj.dob.year),  
                password="password",  
                role='student',)
            obj.user = user
        super().save_model(request, obj, form, change)


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'dob', 'gender', 'hire_date')
    search_fields = ('user__username', 'first_name', 'last_name')
    list_filter = ('hire_date',)

    def save_model(self, request, obj, form, change):
        if not obj.user_id:  
            user = User.objects.create(
                username=obj.first_name.lower() + str(obj.dob.year), 
                password="password",  
                role='teacher',)
            obj.user = user
        super().save_model(request, obj, form, change)


class TeacherGradeCurriculumAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'grade', 'curriculum')
    search_fields = ('teacher__first_name', 'teacher__last_name', 'grade__grade', 'curriculum__subject')
    list_filter = ('grade', 'curriculum')

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'contact_no')
    search_fields = ('username',)

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'relation', 'student', 'contact_no')
    search_fields = ('first_name', 'last_name', 'relation', 'student__first_name', 'student__last_name')
    list_filter = ('relation',)
    autocomplete_fields = ('student',)  
    


admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)    
admin.site.register(TeacherGradeCurriculum, TeacherGradeCurriculumAdmin)
admin.site.register(Attendance)
admin.site.register(Quiz)