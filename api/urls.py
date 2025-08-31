from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmployerViewSet, JobViewSet, ScreeningQuestionViewSet,
    TemplateQuestionViewSet, CandidateViewSet, 
    CandidateResponseViewSet, CandidateAnswerViewSet
)

router = DefaultRouter()
router.register(r'employers', EmployerViewSet, basename='employers')
router.register(r'jobs', JobViewSet, basename='jobs')
router.register(r'questions', ScreeningQuestionViewSet, basename='questions')
router.register(r'templates', TemplateQuestionViewSet, basename='templates')
router.register(r'candidates', CandidateViewSet, basename='candidates')
router.register(r'responses', CandidateResponseViewSet, basename='responses')

# Manual nested routing for answers
urlpatterns = [
    path("", include(router.urls)),
    path('jobs/<int:job_id>/responses/', CandidateResponseViewSet.as_view({'post': 'create'}), name='job-responses'),
    
    # Manual nested routes for answers
    path('responses/<int:response_pk>/answers/', CandidateAnswerViewSet.as_view({'get': 'list', 'post': 'create'}), name='response-answers'),
    path('responses/<int:response_pk>/answers/<int:pk>/', CandidateAnswerViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='response-answer-detail'),
    path('responses/<int:response_pk>/answers/<int:pk>/score/', CandidateAnswerViewSet.as_view({'patch': 'score'}), name='response-answer-score'),
]