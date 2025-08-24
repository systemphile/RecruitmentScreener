from rest_framework import viewsets
from jobsafi.models import Employer, Job, ScreeningQuestion, TemplateQuestion, Candidate, CandidateAnswer, CandidateResponse
from .serializers import EmployerSerializer, JobSerializer, ScreeningQuestionSerializer, TemplateQuestionSerializer, CandidateSerializer, CandidateAnswerSerializer, CandidateResponseSerializer

class EmployerViewSet(viewsets.ModelViewSet):
        queryset = Employer.objects.all()
        serializer_class = EmployerSerializer

class JobViewSet(viewsets.ModelViewSet):
        queryset = Job.objects.all()
        serializer_class = JobSerializer

class ScreeningQuestionViewSet(viewsets.ModelViewSet):
        queryset = ScreeningQuestion.objects.all()
        serializer_class = ScreeningQuestionSerializer

class TemplateQuestionViewSet(viewsets.ModelViewSet):
        queryset = TemplateQuestion.objects.all()
        serializer_class = TemplateQuestionSerializer

class CandidateViewSet(viewsets.ModelViewSet):
        queryset = Candidate.objects.all()
        serializer_class = CandidateSerializer

class CandidateAnswerViewSet(viewsets.ModelViewSet):
        queryset = CandidateAnswer.objects.all()
        serializer_class = CandidateAnswerSerializer

class CandidateResponseViewSet(viewsets.ModelViewSet):
        queryset = CandidateResponse.objects.all()
        serializer_class = CandidateResponseSerializer