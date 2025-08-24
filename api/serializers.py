from rest_framework import serializers
from jobsafi.models import Employer, Job, ScreeningQuestion, TemplateQuestion, Candidate, CandidateAnswer, CandidateResponse

class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class ScreeningQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreeningQuestion
        fields = '__all__'

class TemplateQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateQuestion
        fields = '__all__'

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'

class CandidateAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateAnswer
        fields = '__all__'

class CandidateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateResponse
        fields = '__all__'