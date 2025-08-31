from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Job, Candidate, CandidateResponse, CandidateAnswer

def home(request):
    jobs = Job.objects.all().order_by('seniority')
    context = {"jobs": jobs}
    return render(request, "jobsafi/home.html", context)

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    questions = job.questions.filter(is_approved=True)  # Only show approved questions
    
    if request.method == 'POST':
        # Process form submission
        candidate_name = request.POST.get('candidate_name')
        candidate_email = request.POST.get('candidate_email')
        
        # Create or get candidate
        candidate, created = Candidate.objects.get_or_create(
            email=candidate_email,
            job=job,
            defaults={'name': candidate_name}
        )
        
        # Create response
        response = CandidateResponse.objects.create(
            candidate=candidate,
            job=job
        )
        
        # Create answers
        for question in questions:
            answer_text = request.POST.get(f'answer_{question.id}')
            if answer_text:
                CandidateAnswer.objects.create(
                    response=response,
                    question=question,
                    answer_text=answer_text
                )
        
        messages.success(request, 'Application submitted successfully!')
        return redirect('job_detail', pk=job.pk)
    
    context = {
        "job": job,
        "questions": questions,
    }
    return render(request, "jobsafi/job_detail.html", context)