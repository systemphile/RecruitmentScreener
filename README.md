### JobSafi - Recruitment Screener

#### Overview

JobSafi is Recruiter Screener app, a Django + Django REST Framework project designed to help recruiters streamline candidate screening.  
The system **auto-generates screening questions** based on job descriptions and associated tags, giving recruiters an instant screener they can use in their hiring process.  

This project is developed as a capstone project.

#### Features

* **User Management**: Employers (recruiters), and Admin roles.  
* **Job Posting**: Employers create and manage job listings with tags/keywords.  
* **Auto-Generated Screening Questions**: Generated from predefined template questions mapped to job tags.  
* **Custom Screening Questions**: Employers can add their own custom questions.  
* **Evaluation Tools**: Employers can score and annotate candidate responses.  
* **REST API**: Complete API layer for integration with external systems (HRMS, ATS, etc.) 
* **Candidate Portal**: Clean interface for candidates to submit applications


#### Tech Stack

* Python 3.10+  
* Django 5.x  
* Django REST Framework (DRF)  
* Django-Taggit 6.1+  
* SQLite (Development) / PostgreSQL ready  
* WhiteNoise for static file serving
* PythonAnywhere (Deployment platform)

#### Project Structure
``` markdown
recruiter_screener/
├── recruiter_screener/     # Main Django project (settings, wsgi, asgi)
├── jobsafi/     # Core app: models, business logic, admin
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│   └── tests.py
├── api/     # API app: serializers, viewsets, routers permissions
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── requirements.txt
├── manage.py
└── README.md
```

#### Database Entities

* **Employer**: Custom user model extending AbstractUser (employers)
* **Job: Job listings with title, description, seniority, and tags
* **ScreeningQuestion**: Auto-generated or custom questions tied to a job
* **TemplateQuestion**: Reusable predefined question templates mapped to tags
* **Candidate**: Individuals being screened for a job
* **CandidateResponse**: Candidate-submitted answers to screening questions
* **CandidateAnswer**: Individual answers with employer scoring


#### API Endpoints

| Endpoint             | Method | Description                       |
|----------------------|--------|-----------------------------------|
| /api/employers/          | POST   | Create employer (recruiter) user  |
| /api/auth/login/    | POST   | User login/authentication         |
| /api/jobs/          | GET, POST    | List and create job posts                    |
| /api/jobs/{id}/          | GET, PUT, DELETE   | Job post details and management                   |
| /api/jobs/{id}/generate_questions/     | POST    | Auto-generate screening questions                   |
| /api/jobs/{id}/responses/     | GET | List candidate responses for job                   |
| /api/questions/      | GET, POST    | List and manage screening questions          |
| /api/questions/{id}/      | PATCH   | Update question rating and approval         |
| /api/responses/ | POST   | Candidate submits response |
| /api/responses/{id}/answers/{id}/score/	| PATCH	| Employer rates candidate answer  |
| /api/templates/	| GET, POST	| Manage template questions  |

#### Setup Instructions

##### Local Development

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/RecruitmentScreener.git
    cd RecruitmentScreener
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run migrations:

    ```bash
    python manage.py migrate
    ```

5. Create superuser:

    ```bash
    python manage.py createsuperuser
    ```

6. Start development server:

    ```bash
    python manage.py runserver
    ```


#### Production Deployment

The application is configured for deployment on PythonAnywhere:
1. Set DEBUG = False in production
2. Configure proper SECRET_KEY using environment variables
3. Use WhiteNoise for static file serving
4. Set ALLOWED_HOSTS to your domain
5. Ensure proper database configuration (SQLite for free tier, PostgreSQL for paid)

#### Usage

##### For Employers

1. Register an employer account
2. Create job postings with relevant tags
3. Auto-generate screening questions based on job tags
4. Review and approve generated questions
5. Monitor candidate responses
6. Score and evaluate candidate answers

##### For Candidates

1. Browse available job postings
2. View job details and screening questions
3. Submit application with answers to screening questions
4. Receive confirmation of application submission

##### Auto-Generation Feature

The system automatically generates screening questions by matching job tags with predefined template questions. Employers can:

* Generate questions for new jobs with relevant tags
* Review and approve generated questions
* Build a library of approved questions over time
* Use both auto-generated and custom questions

##### Contributing

The system automatically generates screening questions by matching job tags with predefined template questions. Employers can:

1. Fork the repository
2. Create a feature branch: git checkout -b feature/new-feature
3. Commit changes: git commit -am 'Add new feature'
4. Push to branch: git push origin feature/new-feature
5. Submit a pull request

#### Development Roadmap

- [x] Define project idea and features  
- [x] Create ERD and endpoint plan  
- [x] Set up Django + DRF project skeleton  
- [x] Implement models & migrations  
- [x] Implement serializers & views  
- [x] Add authentication & authorization  
- [x] Implement CRUD endpoints  
- [x] Implement auto-generation of screening questions  
- [x] Deploy to PythonAnywhere  
- [x] Final testing & documentation  

#### Author

Elly Okoth — Backend Developer (Capstone Project)
