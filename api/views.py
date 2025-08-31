from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from jobsafi.utils import auto_generate_questions

from jobsafi.models import (
    Employer, Job, ScreeningQuestion, TemplateQuestion,
    Candidate, CandidateAnswer, CandidateResponse
)
from .serializers import (
    EmployerSerializer, JobSerializer, ScreeningQuestionSerializer,
    TemplateQuestionSerializer, CandidateSerializer,
    JobDetailSerializer, CandidateResponseSerializer, ScreeningQuestionSerializer
)


# ---------------- EMPLOYER ----------------
class EmployerViewSet(viewsets.ModelViewSet):
    """
    Employers can register (no auth required),
    but all other actions require authentication.
    """
    serializer_class = EmployerSerializer

    def get_permissions(self):
        if self.action == "create":  
            return [AllowAny()]  # Anyone can register
        return [IsAuthenticated()]  # Others must be logged in

    def get_queryset(self):
        return Employer.objects.all()


# ---------------- JOB ----------------
class JobViewSet(viewsets.ModelViewSet):
    """
    Jobs belong to Employers.
    - Public can view jobs
    - Only job owner can create/update/delete their jobs
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return JobDetailSerializer
        return JobSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Job.objects.filter(employer=user).prefetch_related('tags')
        return Job.objects.all().prefetch_related('tags')

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.employer != self.request.user:
            raise PermissionDenied("You cannot edit another employer's job.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.employer != self.request.user:
            raise PermissionDenied("You cannot delete another employer's job.")
        instance.delete()

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def candidates(self, request, pk=None):
        """
        Get all candidates for a specific job.
        Only the job owner can access this endpoint.
        """
        job = self.get_object()
        
        # Check if the current user owns this job
        if job.employer != request.user:
            return Response(
                {"error": "You can only view candidates for your own jobs"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        candidates = job.candidates.all()
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def responses(self, request, pk=None):
        """
        Get all responses for a specific job.
        Only the job owner can access this endpoint.
        """
        job = self.get_object()
        
        # Check if the current user owns this job
        if job.employer != request.user:
            return Response(
                {"error": "You can only view responses for your own jobs"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        responses = job.responses.all()
        serializer = CandidateResponseSerializer(responses, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def generate_questions(self, request, pk=None):
        """
        Auto-generate screening questions based on job tags
        """
        job = self.get_object()
        
        # Check if the current user owns this job
        if job.employer != request.user:
            return Response(
                {"error": "You can only generate questions for your own jobs"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Generate questions
        generated_questions = auto_generate_questions(job)
        
        if not generated_questions:
            return Response(
                {"message": "No new questions generated. Either no matching templates found or questions already exist."},
                status=status.HTTP_200_OK
            )
        
        serializer = ScreeningQuestionSerializer(generated_questions, many=True)
        return Response(
            {
                "message": f"Generated {len(generated_questions)} new questions",
                "questions": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

# ---------------- SCREENING QUESTIONS ----------------
class ScreeningQuestionViewSet(viewsets.ModelViewSet):
    """
    Screening questions for jobs.
    - Public can view approved questions
    - Only job owner can manage questions
    """
    serializer_class = ScreeningQuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        job_id = self.request.query_params.get('job')
        
        if user.is_authenticated:
            # Authenticated users see questions for their jobs
            queryset = ScreeningQuestion.objects.filter(job__employer=user)
        else:
            # Public users only see approved questions
            queryset = ScreeningQuestion.objects.filter(is_approved=True)
        
        if job_id:
            queryset = queryset.filter(job_id=job_id)
            
        return queryset

    def perform_create(self, serializer):
        job = serializer.validated_data["job"]
        if job.employer != self.request.user:
            raise PermissionDenied("You cannot add questions to another employer's job.")
        serializer.save()

    def perform_update(self, serializer):
        if serializer.instance.job.employer != self.request.user:
            raise PermissionDenied("You cannot edit questions for another employer's job.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.job.employer != self.request.user:
            raise PermissionDenied("You cannot delete questions for another employer's job.")
        instance.delete()


# ---------------- TEMPLATE QUESTIONS ----------------
class TemplateQuestionViewSet(viewsets.ModelViewSet):
    """
    Reusable template questions (system-wide).
    Only authenticated users can manage.
    """
    queryset = TemplateQuestion.objects.all()
    serializer_class = TemplateQuestionSerializer
    permission_classes = [IsAuthenticated]


# ---------------- CANDIDATE ----------------
class CandidateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Candidates can only register.
    No listing/updating others.
    """
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [AllowAny]


# ---------------- CANDIDATE RESPONSES ----------------
class CandidateResponseViewSet(viewsets.ModelViewSet):
    """
    Candidate submits responses to a job’s screening questions in one flow:
    - Candidate info (id or object)
    - Job id
    - Answers (list of {question, answer})
    """
    queryset = CandidateResponse.objects.all()
    serializer_class = CandidateResponseSerializer
    permission_classes = [AllowAny]
    authentication_classes = []


    def create(self, request, job_id=None):
        data = request.data.copy()
        
        # If job_id comes from URL (job-specific endpoint), use it
        if job_id is not None:
            data['job'] = job_id
        else:
            # For the generic endpoint, expect job in payload
            job_id = data.get('job')
        
        candidate_data = data.get("candidate")
        answers = data.get("answers", [])
        
        # --- Validate required fields ---
        if not candidate_data or not job_id or not answers:
            return Response(
                {"error": "candidate, job, and answers are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # --- Candidate Handling ---
        candidate = None
        if isinstance(candidate_data, int) or str(candidate_data).isdigit():
            # Candidate by ID
            try:
                candidate = Candidate.objects.get(id=candidate_data)
                # Verify this candidate is associated with the correct job
                if candidate.job_id != job_id:
                    return Response(
                        {"error": "Candidate is not associated with this job"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except Candidate.DoesNotExist:
                return Response(
                    {"error": f"Candidate with id {candidate_data} not found"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif isinstance(candidate_data, dict):
            # Candidate by object - use the job from context
            candidate_data['job'] = job_id
            candidate_serializer = CandidateSerializer(data=candidate_data)
            if candidate_serializer.is_valid():
                # Try to find existing candidate by email for this job
                try:
                    candidate = Candidate.objects.get(email=candidate_data['email'], job_id=job_id)
                    # Update name if provided and different
                    if candidate_data.get('name') and candidate.name != candidate_data['name']:
                        candidate.name = candidate_data['name']
                        candidate.save()
                except Candidate.DoesNotExist:
                    # Create new candidate
                    candidate = candidate_serializer.save()
            else:
                return Response(
                    {"error": "Invalid candidate data", "details": candidate_serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"error": "Invalid candidate format. Provide ID or candidate object."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # --- Create CandidateResponse ---
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response(
                {"error": f"Job with id {job_id} not found"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        response_obj = CandidateResponse.objects.create(
            candidate=candidate,
            job=job
        )
        
        # --- Create Answers ---
        for ans in answers:
            question_id = ans.get("question")
            answer_text = ans.get("answer_text")  # Use answer_text instead of answer
            
            if not question_id or answer_text is None:
                continue  # skip invalid entries
            
            try:
                question = ScreeningQuestion.objects.get(id=question_id, job_id=job_id)
            except ScreeningQuestion.DoesNotExist:
                continue  # skip invalid questions
            
            CandidateAnswer.objects.create(
                response=response_obj,
                question=question,
                answer_text=answer_text
            )
        
        return Response(
            {"message": "Answers submitted successfully!", "response_id": response_obj.id},
            status=status.HTTP_201_CREATED
        )
