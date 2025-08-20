from rest_framework import serializers
from screener.models import Employer, Job, ScreeningQuestion, TemplateQuestion, Candidate, CandidateAnswer, CandidateResponse

class EmployerSerializer(serializers.ModelSerializer):
    model = Employer
    fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    model = Job
    fields = '__all__'

class ScreeningQuestionSerializer(serializers.ModelSerializer):
    model = ScreeningQuestion
    fields = '__all__'

class TemplateQuestionSerializer(serializers.ModelSerializer):
    model = TemplateQuestion
    fields = '__all__'

class CandidateSerializer(serializers.ModelSerializer):
    model = Candidate
    fields = '__all__'

class CandidateResponseSerializer(serializers.ModelSerializer):
    model = CandidateAnswer
    fields = '__all__'

class CandidateAnswerSerializer(serializers.ModelSerializer):
    model = CandidateResponse
    fields = '__all__'