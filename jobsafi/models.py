from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from taggit.managers import TaggableManager


# Employer model (system users who create jobs and screen candidates)
class Employer(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    company_name = models.CharField(max_length=255, default="Company")

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = "Employer"
        verbose_name_plural = "Employers"


# Job model (submitted by Employer, generates screening questions)
class Job(models.Model):
    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="jobs"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    seniority = models.CharField(max_length=50)
    tags = TaggableManager()

    def __str__(self):
        return self.title


# Screening questions for a specific Job
class ScreeningQuestion(models.Model):
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name="questions"
    )
    text = models.TextField()
    is_custom = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    rating = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Q: {self.text[:50]}..."


# Pre-approved question templates (reusable across jobs)
class TemplateQuestion(models.Model):
    tag = models.CharField(max_length=200)
    template_text = models.TextField()

    def __str__(self):
        return f"{self.tag}: {self.template_text[:50]}..."


# Candidate model (individuals being screened for a Job)
class Candidate(models.Model):
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name="candidates"
    )
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)

    def __str__(self):
        return self.name


# Candidate response session (all answers per candidate for a specific job)
class CandidateResponse(models.Model):
    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, related_name="responses"
    )
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name="responses"
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    overall_score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Response by {self.candidate.name} for {self.job.title}"

    def calculate_overall_score(self):
        """Recalculate overall score as average of all answer scores."""
        answers = self.answers.exclude(score__isnull=True)
        if not answers.exists():
            return None
        total = sum(answer.score for answer in answers)
        self.overall_score = total / answers.count()
        return self.overall_score


# Candidate answers to individual screening questions
class CandidateAnswer(models.Model):
    response = models.ForeignKey(
        CandidateResponse, on_delete=models.CASCADE, related_name="answers"
    )
    question = models.ForeignKey(
        ScreeningQuestion, on_delete=models.CASCADE, related_name="answers"
    )
    answer_text = models.TextField()
    score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.response.candidate.name} → {self.question.text[:30]}..."