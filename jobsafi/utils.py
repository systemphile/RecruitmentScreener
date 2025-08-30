from .models import Job, ScreeningQuestion, TemplateQuestion

def auto_generate_questions(job):
    """
    Auto-generate screening questions based on job tags and template questions
    """
    generated_questions = []
    
    # Get all tags for this job
    for tag in job.tags.all():
        # Find template questions for this tag
        templates = TemplateQuestion.objects.filter(tag=tag.name.lower())
        
        for template in templates:
            # Check if similar question already exists for this job
            existing_question = ScreeningQuestion.objects.filter(
                job=job,
                text__icontains=template.template_text[:50]  # Partial match
            ).first()
            
            if not existing_question:
                question = ScreeningQuestion.objects.create(
                    job=job,
                    text=template.template_text,
                    is_custom=False,
                    is_approved=False  # Employer can review and approve
                )
                generated_questions.append(question)
    
    return generated_questions