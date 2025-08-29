from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied

from jobsafi.models import (
    Employer, Job, ScreeningQuestion, TemplateQuestion,
    Candidate, CandidateAnswer, CandidateResponse
)
from .serializers import (
    EmployerSerializer, JobSerializer, ScreeningQuestionSerializer,
    TemplateQuestionSerializer, CandidateSerializer,
    CandidateAnswerSerializer, CandidateResponseSerializer
)


class EmployerViewSet(viewsets.ModelViewSet):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer

    def get_permissions(self):
        if self.action == "create":  # anyone can register as an employer
            return [AllowAny()]
        return [IsAuthenticated()]  # other actions require login
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Employer deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Employers only see their own jobs.
        Anonymous users can read all jobs (public listing).
        """
        user = self.request.user
        if user.is_authenticated:
            return Job.objects.filter(employer=user)
        return Job.objects.all()  # allow public to see jobs

    def perform_create(self, serializer):
        """
        Assign the logged-in employer automatically.
        """
        serializer.save(employer=self.request.user)

    def perform_update(self, serializer):
        """
        Prevent editing jobs that don’t belong to the logged-in employer.
        """
        if serializer.instance.employer != self.request.user:
            raise PermissionDenied("You cannot edit another employer's job.")
        serializer.save()

    def perform_destroy(self, instance):
        """
        Prevent deleting jobs that don’t belong to the logged-in employer.
        """
        if instance.employer != self.request.user:
            raise PermissionDenied("You cannot delete another employer's job.")
        instance.delete()

class ScreeningQuestionViewSet(viewsets.ModelViewSet):
    serializer_class = ScreeningQuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Employers only see questions for their own jobs.
        Anonymous users cannot see questions.
        """
        user = self.request.user
        if user.is_authenticated:
            return ScreeningQuestion.objects.filter(job__employer=user)
        return ScreeningQuestion.objects.none()

    def perform_create(self, serializer):
        """
        Ensure that only the employer who owns the job can add questions.
        """
        job = serializer.validated_data["job"]
        if job.employer != self.request.user:
            raise PermissionDenied("You cannot add questions to another employer's job.")
        serializer.save()

    def perform_update(self, serializer):
        """
        Restrict updates to questions tied to the employer's own jobs.
        """
        if serializer.instance.job.employer != self.request.user:
            raise PermissionDenied("You cannot edit questions for another employer's job.")
        serializer.save()

    def perform_destroy(self, instance):
        """
        Restrict deletion to employer's own job questions.
        """
        if instance.job.employer != self.request.user:
            raise PermissionDenied("You cannot delete questions for another employer's job.")
        instance.delete()

class TemplateQuestionViewSet(viewsets.ModelViewSet):
    queryset = TemplateQuestion.objects.all()
    serializer_class = TemplateQuestionSerializer
    permission_classes = [IsAuthenticated]


# Candidates: only Creates (registration), no listing/updating others
class CandidateViewSet(mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [AllowAny]


# Candidate answers: only Creates (submit answers), no list/update/delete
class CandidateAnswerViewSet(viewsets.ModelViewSet):
    serializer_class = CandidateAnswerSerializer
    permission_classes = [AllowAny]  # candidates submit without login

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Employers see answers for their own jobs only
            return CandidateAnswer.objects.filter(
                question__job__employer=user
            )
        # Anonymous candidates shouldn’t list answers
        return CandidateAnswer.objects.none()

    def perform_create(self, serializer):
        """
        Allow anonymous candidates to submit answers,
        but ensure the question belongs to an active job.
        """
        question = serializer.validated_data["question"]
        job = question.job

        if not job:
            raise PermissionDenied("Invalid job for this answer.")

        serializer.save()

    def perform_update(self, serializer):
        """
        Prevent updates — candidates shouldn’t edit answers after submission.
        Employers also can’t modify answers.
        """
        raise PermissionDenied("Updating answers is not allowed.")

    def perform_destroy(self, instance):
        """
        Prevent deletions entirely.
        """
        raise PermissionDenied("Deleting answers is not allowed.")
    
class CandidateResponseViewSet(viewsets.ModelViewSet):
    serializer_class = CandidateResponseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Limit employers to only see responses for jobs they own.
        """
        user = self.request.user
        return CandidateResponse.objects.filter(
            candidate__job__employer=user
        )

    def perform_create(self, serializer):
        """
        Ensure responses can only be created for jobs owned by the logged-in employer.
        """
        user = self.request.user
        candidate = serializer.validated_data["candidate"]
        if candidate.job.employer != user:
            raise PermissionDenied("You cannot submit responses for this job.")
        serializer.save()