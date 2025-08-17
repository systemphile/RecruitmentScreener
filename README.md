### RecruiterScreener

#### Overview

Recruiter Screener is a Django + Django REST Framework project designed to help recruiters streamline candidate screening.  
The system **auto-generates screening questions** based on job descriptions and associated tags, giving recruiters an instant screener they can use in their hiring process.  

This project is developed as a capstone project.

#### Features

* **User Management**: Employers (recruiters), Candidates and Admin roles.  
* **Job Posting**: Employers create and manage job listings with tags/keywords.  
* **Auto-Generated Screening Questions**: Generated from predefined template questions mapped to job tags.  
* **Custom Screening Questions**: Employers can add their own custom questions.  
* **Evaluation Tools**: Employers can score or annotate questions to refine future screeners.  
* **API Layer**: REST API for integration with external systems (HRMS, ATS, etc.).  


#### Tech Stack

* Python 3.10+  
* Django 5.x  
* Django REST Framework (DRF)  
* Django-Taggit 6.1+  
* SQLite (Dev) / PostgreSQL (Prod)  
* Heroku / PythonAnywhere (Deployment target)  

#### Project Structure
``` markdown
recruiter_screener/ # Project folder (repo root)
│── recruiter_screener/ # Main Django project (settings, wsgi, asgi)
│── screener/ # Core app: models, business logic, admin
│ │── models.py
│ │── views.py
│ │── urls.py
│ │── tests.py
│── api/ # API app: serializers, viewsets, routers, permissions
│ │── serializers.py
│ │── views.py
│ │── urls.py
│ │── tests.py
│── requirements.txt
│── manage.py
└── README.md
```

#### Database Entities (Implemented)

* **Employer**: Custom user model extending `AbstractUser` (employers).  
* **Job**: Job listings with title, description, seniority, and tags.  
* **ScreeningQuestion**: Auto-generated or custom questions tied to a job.  
* **TemplateQuestion**: Reusable predefined question templates mapped to tags.  

* **CandidateResponse**: Candidate-submitted answers to screening questions, with employers able to assign scores and feedback manually.  

#### API Endpoints (Planned)

| Endpoint             | Method | Description                       |
|----------------------|--------|-----------------------------------|
| /api/users/          | POST   | Create employer (recruiter) user  |
| /api/users/login/    | POST   | User login/authentication         |
| /api/posts/          | GET    | List job posts                    |
| /api/posts/          | POST   | Create job post                   |
| /api/posts/{id}/     | PUT    | Update job post                   |
| /api/posts/{id}/     | DELETE | Delete job post                   |
| /api/questions/      | GET    | List screening questions          |
| /api/questions/      | POST   | Add new question (custom)         |
| /api/questions/auto/ | POST   | Auto-generate screening questions |
| /api/candidate-responses/	| POST	| Candidate submits an answer
| /api/candidate-responses/	| GET	| Employer views submitted answers
| /api/candidate-responses/{id}/rate	| PUT	| Employer rates/annotates candidate answer

#### Setup Instructions

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

5. Start development server:

    ```bash
    python manage.py runserver
    ```

#### Development Roadmap

- [x] Define project idea and features  
- [x] Create ERD and endpoint plan  
- [x] Set up Django + DRF project skeleton  
- [x] Implement models & migrations  
- [ ] Implement serializers & views  
- [ ] Add authentication & authorization  
- [ ] Implement CRUD endpoints  
- [ ] Implement auto-generation of screening questions  
- [ ] Deploy to Heroku/PythonAnywhere  
- [ ] Final testing & documentation  

#### Author

Elly Okoth — Backend Developer (Capstone Project)