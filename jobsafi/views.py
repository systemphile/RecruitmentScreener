from django.shortcuts import render, get_object_or_404
from .models import Job

def home(request):
    jobs = Job.objects.all().order_by('seniority')
    context = {"jobs": jobs}
    return render(request, "jobsafi/home.html", context)

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    questions = job.questions.all()  # via related_name
    context = {
        "job": job,
        "questions": questions,
    }
    return render(request, "jobsafi/job_detail.html", context)