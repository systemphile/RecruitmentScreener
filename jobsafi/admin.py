from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from taggit.models import Tag
from taggit.admin import TagAdmin
from .models import Employer, Job, ScreeningQuestion, TemplateQuestion, CandidateAnswer, Candidate, CandidateResponse

# Clean up admin by removing default Tag registration
admin.site.unregister(Tag)

class EmployerAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'company_name')
    search_fields = ('username', 'email', 'company_name')
    fieldsets = UserAdmin.fieldsets + (
        ('Company Information', {'fields': ('phone', 'company_name')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Company Information', {'fields': ('phone', 'company_name')}),
    )

admin.site.register(Employer, EmployerAdmin)

class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'seniority', 'display_tags')
    search_fields = ('title', 'description', 'employer__username')
    list_filter = ('tags', 'seniority', 'employer')
    
    def display_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    display_tags.short_description = 'Tags'

admin.site.register(Job, JobAdmin)

class ScreeningQuestionAdmin(admin.ModelAdmin):
    list_display = ('job', 'short_text', 'rating', 'is_custom', 'is_approved')
    search_fields = ('job__title', 'text')
    list_filter = ('is_custom', 'is_approved', 'job__employer')
    
    def short_text(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    short_text.short_description = 'Question'

admin.site.register(ScreeningQuestion, ScreeningQuestionAdmin)

class TemplateQuestionAdmin(admin.ModelAdmin):
    list_display = ('tag', 'short_template_text')
    search_fields = ('tag', 'template_text')
    list_filter = ('tag',)
    
    def short_template_text(self, obj):
        return obj.template_text[:50] + '...' if len(obj.template_text) > 50 else obj.template_text
    short_template_text.short_description = 'Template Text'

admin.site.register(TemplateQuestion, TemplateQuestionAdmin)

class CandidateAnswerAdmin(admin.ModelAdmin):
    list_display = ('response', 'short_question', 'short_answer', 'score')
    search_fields = ('response__candidate__name', 'question__text')
    list_filter = ('score', 'question__job')
    
    def short_question(self, obj):
        return obj.question.text[:30] + '...' if len(obj.question.text) > 30 else obj.question.text
    short_question.short_description = 'Question'
    
    def short_answer(self, obj):
        return obj.answer_text[:30] + '...' if len(obj.answer_text) > 30 else obj.answer_text
    short_answer.short_description = 'Answer'

admin.site.register(CandidateAnswer, CandidateAnswerAdmin)

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'job', 'resume')
    search_fields = ('name', 'email', 'job__title')
    list_filter = ('job', 'job__employer')

admin.site.register(Candidate, CandidateAdmin)

class CandidateResponseAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'job', 'submitted_at', 'overall_score')
    search_fields = ('candidate__name', 'job__title')
    list_filter = ('job', 'submitted_at')
    readonly_fields = ('submitted_at',)

admin.site.register(CandidateResponse, CandidateResponseAdmin)