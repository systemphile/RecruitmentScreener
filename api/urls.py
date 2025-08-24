from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import EmployerViewSet, JobViewSet, ScreeningQuestionViewSet, TemplateQuestionViewSet, CandidateViewSet, CandidateAnswerViewSet, CandidateResponseViewSet

router = DefaultRouter()
router.register(r'employers', EmployerViewSet, basename='employers')
router.register(r'jobs', JobViewSet, basename='jobs')
router.register(r'questions', ScreeningQuestionViewSet, basename='questions')
router.register(r'templates', TemplateQuestionViewSet, basename='templates')
router.register(r'candidates', CandidateViewSet, basename='candidates')
router.register(r'answers', CandidateAnswerViewSet, basename='answers')
router.register(r'responses', CandidateResponseViewSet, basename='responses')


urlpatterns = [
    path("", include(router.urls)),
]