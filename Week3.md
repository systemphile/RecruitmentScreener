#### Reflection – RecruiterScreener Capstone Project  

### 1. Accomplishments  
- **Defined the project scope**: Clarified the goal of building a recruiter screener that generates screening questions based on job descriptions.  
- **Created the ERD**: Designed the database structure for Employers, Jobs, Screening Questions, and Template Questions.  
- **Set up the project skeleton**: Installed Django and DRF, created the project and app folders.  
- **Implemented models**: Defined `Employer`, `Job`, `ScreeningQuestion`, and `TemplateQuestion` models.  
- **Updated README.md**: Documented the project overview, features, tech stack, setup instructions, and roadmap.  

### 2. Challenges  
- **Scope creep**: Initially, extra models (like Applications and Candidate Management) were introduced, which could have shifted the project away from the main goal. I resolved this by re-aligning with the original scope: employers posting jobs and generating screening questions only.  
- **Deciding on scoring**: I debated whether to include auto-scoring for candidates’ answers. After reflection, I decided to implement **manual-only scoring** (employers rate answers) to stay within scope and simplify complexity.  
- **Balancing abstraction and implementation**: It was tricky deciding how much detail to include in early models. I handled this by focusing only on what was immediately required (core ERD + models) and leaving space for iterative improvement.  

### 3. Plan for Upcoming Week
- **Implement serializers & views** for the models.  
- **Set up authentication and permissions** so employers can log in and manage only their jobs.  
- **Start building CRUD endpoints** for jobs and questions.  
- **Prepare test cases** to ensure endpoints are reliable.  
- **Keep README.md updated** with each new milestone.