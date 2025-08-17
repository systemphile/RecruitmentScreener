from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employer, Job, ScreeningQuestion, TemplateQuestion

# Register your models here.
class EmployerAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone',)
    search_fields = ('username', 'email',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone',)}),
    )

admin.site.register(Employer, UserAdmin)

class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer',)
    search_fields = ('title', 'description',)
    list_filter = ('tags',)   # allow filtering by tags

admin.site.register(Job, JobAdmin)

class ScreeningQuestionAdmin(admin.ModelAdmin):
    list_display = ('job', 'text', 'rating', 'is_custom', 'is_approved',)
    search_fields = ('job', 'rating',)

admin.site.register(ScreeningQuestion, ScreeningQuestionAdmin)

class TemplateQuestionAdmin(admin.ModelAdmin):
    list_display = ('tag', 'template_text',)
    search_fields = ('tag',)

admin.site.register(TemplateQuestion, TemplateQuestionAdmin)