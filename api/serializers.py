from rest_framework import serializers
from taggit.serializers import TagListSerializerField

from jobsafi.models import (
    Employer,
    Job,
    ScreeningQuestion,
    TemplateQuestion,
    Candidate,
    CandidateAnswer,
    CandidateResponse,
)


class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        employer = Employer(**validated_data)
        if password:
            employer.set_password(password)
        employer.save()
        return employer


# Basic Job Serializer (for listings)
class JobSerializer(serializers.ModelSerializer):
    tags = TagListSerializerField(required=False)  # Add required=False
    
    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'seniority', 'employer', 'tags']
        
    def create(self, validated_data):
        # Extract tags from validated_data
        tags = validated_data.pop('tags', [])
        
        # Create the job instance
        job = Job.objects.create(**validated_data)
        
        # Add tags to the job
        if tags:
            job.tags.set(tags)
        
        return job
    
    def update(self, instance, validated_data):
        # Extract tags from validated_data
        tags = validated_data.pop('tags', None)
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update tags if provided
        if tags is not None:
            instance.tags.set(tags)
        
        return instance

class ScreeningQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreeningQuestion
        fields = "__all__"

# Detailed Job Serializer (includes questions)
class JobDetailSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField() 
    tags = TagListSerializerField()
    
    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'seniority', 'employer', 'questions', 'tags']
    
    def get_questions(self, obj):
        """Return questions based on user authentication and ownership"""
        request = self.context.get('request')
        
        if request and request.user.is_authenticated and obj.employer == request.user:
            # Job owner sees all questions
            questions = obj.questions.all()
        else:
            # Public users only see approved questions
            questions = obj.questions.filter(is_approved=True)
        
        return ScreeningQuestionSerializer(questions, many=True).data



class TemplateQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateQuestion
        fields = "__all__"


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = "__all__"


class CandidateAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateAnswer
        fields = ["id", "response", "question", "answer_text", "score"]
        read_only_fields = ["id", "response", "question", "answer_text"]

    def create(self, validated_data):
        # Auto-set response from URL parameter
        response_id = self.context.get('response_id')
        if response_id:
            validated_data['response_id'] = response_id
        return super().create(validated_data)


class CandidateResponseSerializer(serializers.ModelSerializer):
    candidate = CandidateSerializer()  # allow nested create
    answers = CandidateAnswerSerializer(many=True, required=False)

    class Meta:
        model = CandidateResponse
        fields = ['id', 'candidate', 'job', 'submitted_at', 'overall_score', 'answers']

    def create(self, validated_data):
        candidate_data = validated_data.pop("candidate")
        answers_data = validated_data.pop("answers", [])

        # Find or create candidate just by email (and name if new)
        candidate, _ = Candidate.objects.get_or_create(
            email=candidate_data["email"],
            defaults={"name": candidate_data.get("name", "")},
        )

        # Create CandidateResponse linking candidate to job
        response = CandidateResponse.objects.create(candidate=candidate, **validated_data)

        # Create CandidateAnswers
        for ans in answers_data:
            CandidateAnswer.objects.create(response=response, **ans)

        # Recalculate score
        response.overall_score = response.calculate_overall_score()
        response.save()

        return response