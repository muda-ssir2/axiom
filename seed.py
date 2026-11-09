import os
import json
from datetime import datetime, timezone, timedelta
from app import create_app
from models import db, User, StudentProfile, Company, Job, Application, SavedJob, Course, Lesson, Test, Question, TestResult, Resume, Testimonial

app = create_app()

def seed_database():
    with app.app_context():
        # Clear existing tables for fresh seed
        db.drop_all()
        db.create_all()
        print("Dropped and recreated database tables.")

        # 1. USERS
        admin = User(
            name="Platform Administrator",
            email="admin@axiompath.com",
            role="admin",
            phone="+91 99887 76655"
        )
        admin.set_password("Admin@123")
        db.session.add(admin)

        student1 = User(
            name="Rahul Sharma",
            email="rahul.sharma@axiompath.com",
            role="student",
            phone="+91 98765 43210"
        )
        student1.set_password("Student@123")
        db.session.add(student1)

        student2 = User(
            name="Ananya Verma",
            email="ananya.verma@axiompath.com",
            role="student",
            phone="+91 91234 56789"
        )
        student2.set_password("Student@123")
        db.session.add(student2)

        student3 = User(
            name="Karthik Iyer",
            email="karthik.iyer@axiompath.com",
            role="student",
            phone="+91 98450 12345"
        )
        student3.set_password("Student@123")
        db.session.add(student3)

        db.session.flush()

        # Profiles
        profile1 = StudentProfile(
            user_id=student1.id,
            headline="Aspiring Full Stack Engineer | Python & React | 300+ Problems on LeetCode",
            college="Vellore Institute of Technology (VIT)",
            degree="B.Tech in Computer Science & Engineering",
            graduation_year=2026,
            cgpa=8.85,
            bio="Final-year computer science student passionate about building performant web applications and distributed systems. Strong problem-solving foundations and winner of multiple collegiate hackathons.",
            skills="Python, JavaScript, Flask, React, SQL, PostgreSQL, Docker, Git, Data Structures",
            target_role="Full Stack Developer",
            github_url="https://github.com/rahul-sharma-dev",
            linkedin_url="https://linkedin.com/in/rahul-sharma-axiom",
            portfolio_url="https://rahulsharma.dev"
        )
        db.session.add(profile1)

        profile2 = StudentProfile(
            user_id=student2.id,
            headline="AI/ML Enthusiast & Data Engineer | Final Year CSE",
            college="Delhi Technological University (DTU)",
            degree="B.Tech in Information Technology",
            graduation_year=2026,
            cgpa=9.1,
            bio="Interested in deep learning, LLM fine-tuning, and scalable data pipelines. Actively practicing for tech placement rounds.",
            skills="Python, PyTorch, SQL, Pandas, Scikit-Learn, FastApi, Spark",
            target_role="Data Science / AI Engineer",
            github_url="https://github.com/ananya-verma",
            linkedin_url="https://linkedin.com/in/ananya-verma"
        )
        db.session.add(profile2)

        # 2. COMPANIES
        companies_data = [
            {
                "name": "Razorpay",
                "slug": "razorpay",
                "logo_initials": "RZ",
                "logo_bg_color": "#0284c7",
                "website": "https://razorpay.com",
                "location": "Bengaluru, Karnataka",
                "industry": "Fintech & Payments Infrastructure",
                "employee_count": "2,500+",
                "about": "Razorpay is India's leading full-stack financial services platform powering payments for millions of businesses across the nation."
            },
            {
                "name": "Swiggy",
                "slug": "swiggy",
                "logo_initials": "SW",
                "logo_bg_color": "#f97316",
                "website": "https://swiggy.com",
                "location": "Bengaluru, Karnataka",
                "industry": "Hyperlocal Consumer Tech & Logistics",
                "employee_count": "5,000+",
                "about": "Swiggy connects consumers with thousands of restaurants and stores through an ultra-low latency routing and logistics platform."
            },
            {
                "name": "CRED",
                "slug": "cred",
                "logo_initials": "CR",
                "logo_bg_color": "#111827",
                "website": "https://cred.club",
                "location": "Bengaluru, Karnataka",
                "industry": "Fintech & Rewards Platform",
                "employee_count": "1,000+",
                "about": "CRED is a high-trust community of creditworthy individuals, known for cutting-edge design, high-concurrency systems and engineering craftsmanship."
            },
            {
                "name": "TCS Digital",
                "slug": "tcs-digital",
                "logo_initials": "TC",
                "logo_bg_color": "#4338ca",
                "website": "https://tcs.com",
                "location": "Mumbai / Pan-India",
                "industry": "IT Services & Global Consulting",
                "employee_count": "600,000+",
                "about": "Tata Consultancy Services Digital division drives strategic digital transformations for Fortune 500 enterprises using cloud and modern data platforms."
            },
            {
                "name": "Infosys Ltd",
                "slug": "infosys",
                "logo_initials": "IN",
                "logo_bg_color": "#0284c7",
                "website": "https://infosys.com",
                "location": "Bengaluru / Pune",
                "industry": "Enterprise Digital Solutions",
                "employee_count": "300,000+",
                "about": "A global leader in next-generation digital services and consulting, empowering clients in 56 countries to navigate their digital transformation."
            },
            {
                "name": "BrowserStack",
                "slug": "browserstack",
                "logo_initials": "BS",
                "logo_bg_color": "#059669",
                "website": "https://browserstack.com",
                "location": "Mumbai / Remote",
                "industry": "Cloud Testing & Developer Tools",
                "employee_count": "1,200+",
                "about": "BrowserStack is the world's leading web and mobile app testing platform powering automated test suites for 50,000+ customers worldwide."
            },
            {
                "name": "Juspay",
                "slug": "juspay",
                "logo_initials": "JP",
                "logo_bg_color": "#7c3aed",
                "website": "https://juspay.in",
                "location": "Bengaluru, Karnataka",
                "industry": "Payments OS & Pure Functional Engineering",
                "employee_count": "800+",
                "about": "Juspay builds India's unified payment infrastructure processing hundreds of millions of UPI and card transactions daily using Haskell and PureScript."
            },
            {
                "name": "Zomato",
                "slug": "zomato",
                "logo_initials": "ZO",
                "logo_bg_color": "#e11d48",
                "website": "https://zomato.com",
                "location": "Gurugram, Haryana",
                "industry": "Food Delivery & Quick Commerce",
                "employee_count": "4,000+",
                "about": "Zomato is a technology platform connecting customers, restaurant partners and delivery partners with millions of monthly transactions."
            }
        ]

        companies = {}
        for c_data in companies_data:
            comp = Company(**c_data)
            db.session.add(comp)
            companies[c_data["slug"]] = comp

        db.session.flush()

        # 3. REALISTIC JOBS
        jobs_data = [
            {
                "title": "Associate Software Engineer - Backend",
                "company_id": companies["razorpay"].id,
                "role_category": "Backend Development",
                "job_type": "Full-Time",
                "location": "Bengaluru, KA",
                "workplace_type": "Hybrid",
                "experience_level": "Fresher (0-1 yrs)",
                "min_salary": 14.0,
                "max_salary": 18.0,
                "salary_display": "₹14.0 - ₹18.0 LPA",
                "skills_required": "Python, Golang, SQL, REST APIs, Redis, Distributed Systems",
                "openings": 6,
                "is_featured": True,
                "description": "Join Razorpay's Core Payments team to build resilient, ultra-fast transaction processing microservices. You will work on high-volume message queues, distributed database locking, and partner banking integrations handling 15,000+ transactions per second.",
                "requirements": "• B.Tech/B.E in CS/IT or equivalent (2025/2026 Batch)\n• Strong fundamentals in Data Structures, Algorithms and OS\n• Proficient in Python, Java, or Golang\n• Understanding of relational databases (PostgreSQL/MySQL) and indexes\n• Eagerness to build highly available fintech software."
            },
            {
                "title": "Frontend Software Engineer (React / Next.js)",
                "company_id": companies["swiggy"].id,
                "role_category": "Frontend Development",
                "job_type": "Full-Time",
                "location": "Bengaluru, KA",
                "workplace_type": "Onsite",
                "experience_level": "Fresher (0-1 yrs)",
                "min_salary": 12.0,
                "max_salary": 16.0,
                "salary_display": "₹12.0 - ₹16.0 LPA",
                "skills_required": "JavaScript, TypeScript, React.js, HTML5/CSS3, State Management, Web Performance",
                "openings": 4,
                "is_featured": True,
                "description": "Help millions of food lovers order in seconds. You will craft pixel-perfect, accessible, and high-performance user interfaces for web and mobile web browsers.",
                "requirements": "• Good command over modern JavaScript (ES6+), CSS Grid/Flexbox\n• Experience with React component lifecycles, Hooks, and memoization\n• Passion for sub-second page loads and mobile-first design\n• Portfolio or project links demonstrating responsive web apps."
            },
            {
                "title": "Software Development Engineer - Trainee (SDE-1)",
                "company_id": companies["cred"].id,
                "role_category": "Full Stack Development",
                "job_type": "Full-Time",
                "location": "Bengaluru, KA",
                "workplace_type": "Onsite",
                "experience_level": "Fresher (0-1 yrs)",
                "min_salary": 18.0,
                "max_salary": 24.0,
                "salary_display": "₹18.0 - ₹24.0 LPA",
                "skills_required": "Java, Spring Boot, Microservices, React, Kafka, Docker",
                "openings": 3,
                "is_featured": True,
                "description": "At CRED, engineering craftsmanship is our core philosophy. We look for candidates who write clean, elegant, modular code with strict testing coverage and architectural elegance.",
                "requirements": "• Strong algorithmic intuition and problem-solving capability\n• Knowledge of Object-Oriented Principles and Design Patterns\n• Ability to decompose complex system requirements into clean services\n• CGPA 8.0+ or equivalent competitive programming rating."
            },
            {
                "title": "Systems Engineer - TCS Digital",
                "company_id": companies["tcs-digital"].id,
                "role_category": "Software Engineering",
                "job_type": "Full-Time",
                "location": "Pan-India (Multiple Locations)",
                "workplace_type": "Hybrid",
                "experience_level": "Fresher (0-1 yrs)",
                "min_salary": 7.0,
                "max_salary": 9.0,
                "salary_display": "₹7.0 - ₹9.0 LPA",
                "skills_required": "Python, Java, Cloud Computing, SQL, SDLC",
                "openings": 25,
                "is_featured": False,
                "description": "TCS Digital offers elite opportunities to work on digital transformation projects for global banks, airlines, and healthcare providers using state-of-the-art tech stacks.",
                "requirements": "• B.E / B.Tech / M.E / M.Tech in CS/IT/ECE (2025/2026 batches)\n• Minimum 60% or 6.0 CGPA throughout academic career\n• Good analytical, logical, and verbal communication abilities\n• Hands-on project experience in web or mobile app development."
            },
            {
                "title": "Specialist Programmer / DSE",
                "company_id": companies["infosys"].id,
                "role_category": "Software Engineering",
                "job_type": "Full-Time",
                "location": "Pune / Bengaluru",
                "workplace_type": "Hybrid",
                "experience_level": "Fresher (0-1 yrs)",
                "min_salary": 8.0,
                "max_salary": 9.5,
                "salary_display": "₹8.0 - ₹9.5 LPA",
                "skills_required": "Python, Java, DSA, Dynamic Programming, System Basics",
                "openings": 15,
                "is_featured": False,
                "description": "The Specialist Programmer (SP) role is Infosys' premier coding profile, assigned to high-impact innovation labs, AI incubators, and enterprise modernization initiatives.",
                "requirements": "• Cleared HackWithInfy or InfyTQ with high percentile\n• Advanced proficiency in Dynamic Programming, Graphs and Bit Manipulation\n• Excellent problem formulation and debugging skills."
            },
            {
                "title": "Software Development Engineer in Test (SDET)",
                "company_id": companies["browserstack"].id,
                "role_category": "QA & Automation",
                "job_type": "Full-Time",
                "location": "Remote / Mumbai",
                "workplace_type": "Remote",
                "experience_level": "Fresher (0-1 yrs)",
                "min_salary": 11.0,
                "max_salary": 14.5,
                "salary_display": "₹11.0 - ₹14.5 LPA",
                "skills_required": "Python, PyTest, Selenium, Playwright, CI/CD, Linux",
                "openings": 5,
                "is_featured": True,
                "description": "Work at the core of developer infrastructure. You will design automated testing frameworks capable of running thousands of browser matrix tests concurrently.",
                "requirements": "• Strong coding skills in Python or Java\n• Good understanding of browser internals, DevTools, and DOM structure\n• Familiarity with Git, Linux command line and Docker containers."
            },
            {
                "title": "Product Analyst - Core Experience",
                "company_id": companies["zomato"].id,
                "role_category": "Product & Analytics",
                "job_type": "Full-Time",
                "location": "Gurugram, HR",
                "workplace_type": "Onsite",
                "experience_level": "Fresher (0-1 yrs)",
                "min_salary": 9.0,
                "max_salary": 13.0,
                "salary_display": "₹9.0 - ₹13.0 LPA",
                "skills_required": "Advanced SQL, Python, Tableau/PowerBI, A/B Testing, Product Metrics",
                "openings": 4,
                "is_featured": False,
                "description": "Dive into terabytes of consumer behavior data to unlock conversion funnels, predict delivery times, and analyze experiment results for Zomato Gold & Blinkit.",
                "requirements": "• Exceptional aptitude in quantitative reasoning and business analytics\n• Advanced SQL mastery (Window functions, CTEs, self-joins)\n• Experience analyzing data using Python (Pandas/NumPy)\n• Strong communication and storytelling with data."
            },
            {
                "title": "Functional Programming Engineer - FP Trainee",
                "company_id": companies["juspay"].id,
                "role_category": "Backend Development",
                "job_type": "Full-Time",
                "location": "Bengaluru, KA",
                "workplace_type": "Onsite",
                "experience_level": "Fresher (0-1 yrs)",
                "min_salary": 15.0,
                "max_salary": 20.0,
                "salary_display": "₹15.0 - ₹20.0 LPA",
                "skills_required": "Haskell, PureScript, C++, Type Systems, Distributed State Machines",
                "openings": 5,
                "is_featured": True,
                "description": "Juspay is one of the world's largest commercial adopters of Haskell and functional programming. Build zero-downtime, deterministic financial transaction engines.",
                "requirements": "• Passion for declarative, pure functional programming\n• Strong grasp of mathematical proofs, Category Theory concepts or pure typed code\n• Willingness to undergo intensive bootcamps in Haskell and PureScript."
            },
            {
                "title": "Cloud & DevOps Associate",
                "company_id": companies["razorpay"].id,
                "role_category": "Cloud & DevOps",
                "job_type": "Full-Time",
                "location": "Bengaluru, KA",
                "workplace_type": "Hybrid",
                "experience_level": "Fresher (0-1 yrs)",
                "min_salary": 10.0,
                "max_salary": 14.0,
                "salary_display": "₹10.0 - ₹14.0 LPA",
                "skills_required": "AWS, Docker, Kubernetes, Linux, Terraform, GitHub Actions",
                "openings": 3,
                "is_featured": False,
                "description": "Collaborate with platform engineers to provision secure infrastructure as code, build automated deployment pipelines, and maintain 99.99% uptime for payment gateways.",
                "requirements": "• Solid understanding of Linux networking, DNS, routing and security\n• Experience with containerization (Docker) and basic Kubernetes\n• Scripting skills in Bash or Python\n• AWS/GCP certification is a plus."
            },
            {
                "title": "Machine Learning Engineer - Intern",
                "company_id": companies["swiggy"].id,
                "role_category": "Data Science & AI",
                "job_type": "Internship",
                "location": "Bengaluru, KA",
                "workplace_type": "Hybrid",
                "experience_level": "Fresher (0-1 yrs)",
                "min_salary": 6.0,
                "max_salary": 8.0,
                "salary_display": "₹50,000 / month (PPO up to ₹16 LPA)",
                "skills_required": "Python, PyTorch, Scikit-learn, Feature Engineering, FastApi",
                "openings": 3,
                "is_featured": True,
                "description": "Work with our recommendation systems team on dynamic pricing, delivery ETA modeling, and search ranking algorithms using multi-modal embeddings.",
                "requirements": "• Pre-final or final year student in CS, Data Science, Math or Stats\n• Hands-on ML project portfolio on GitHub or Kaggle\n• Solid grasp of Linear Algebra, Probability, and Loss Optimization."
            }
        ]

        created_jobs = []
        for j_data in jobs_data:
            job = Job(**j_data)
            db.session.add(job)
            created_jobs.append(job)

        db.session.flush()

        # 4. APPLICATIONS & SAVED JOBS FOR DEMO STUDENT
        app1 = Application(
            job_id=created_jobs[0].id,
            user_id=student1.id,
            cover_note="I am extremely excited about Razorpay's high-scale fintech architecture. I have built multiple backend microservices with Python and Docker.",
            status="Interview Scheduled",
            admin_feedback="Selected for Technical Round 2 based on outstanding aptitude and DSA profile test."
        )
        app2 = Application(
            job_id=created_jobs[2].id,
            user_id=student1.id,
            cover_note="CRED's engineering blog has been my biggest source of inspiration. Ready to write production-grade code.",
            status="Under Review",
            admin_feedback="Profile submitted to hiring manager for resume screening."
        )
        db.session.add_all([app1, app2])

        save1 = SavedJob(job_id=created_jobs[1].id, user_id=student1.id)
        save2 = SavedJob(job_id=created_jobs[5].id, user_id=student1.id)
        db.session.add_all([save1, save2])

        # 5. TESTS AND QUESTIONS
        test1 = Test(
            title="Quantitative Aptitude - Placement Sprint",
            slug="quant-placement-sprint",
            category="Quantitative Aptitude",
            description="Comprehensive numerical ability test covering Time & Work, Profit & Loss, Speed-Distance, and Permutations. Essential for TCS, Infosys, and product-firm online rounds.",
            duration_mins=20,
            total_marks=10,
            passing_marks=6,
            difficulty="Medium"
        )
        test2 = Test(
            title="Logical Reasoning & Analytical Puzzle Test",
            slug="logical-reasoning-assessment",
            category="Logical Reasoning",
            description="Assess your deductive reasoning, syllogisms, blood relations, and seating arrangement puzzles commonly encountered in campus recruitment drives.",
            duration_mins=15,
            total_marks=8,
            passing_marks=5,
            difficulty="Medium"
        )
        test3 = Test(
            title="Technical CS Fundamentals & SQL Mock",
            slug="cs-fundamentals-sql-mock",
            category="Technical Coding",
            description="Core Computer Science essentials: DBMS transactions, ACID properties, Operating System scheduling, Computer Networks, and Python internals.",
            duration_mins=25,
            total_marks=12,
            passing_marks=7,
            difficulty="Hard"
        )
        test4 = Test(
            title="Verbal Ability & Professional English",
            slug="verbal-ability-assessment",
            category="Verbal Ability",
            description="Sentence correction, para-jumbles, vocabulary in context, and error spotting for corporate campus screening.",
            duration_mins=15,
            total_marks=4,
            passing_marks=2,
            difficulty="Easy"
        )

        db.session.add_all([test1, test2, test3, test4])
        db.session.flush()

        # Questions for Test 1 (Quantitative)
        q_quant = [
            {
                "test_id": test1.id,
                "question_text": "A can complete a piece of work in 12 days and B in 18 days. If they work together for 4 days, what fraction of the work remains unfinished?",
                "option_a": "1/3",
                "option_b": "4/9",
                "option_c": "5/9",
                "option_d": "2/3",
                "correct_option": "B",
                "explanation": "A's 1 day work = 1/12, B's 1 day work = 1/18. Together in 1 day = 1/12 + 1/18 = 5/36. In 4 days, work done = 4 * (5/36) = 20/36 = 5/9. Work remaining = 1 - 5/9 = 4/9.",
                "category": "Quantitative",
                "marks": 2
            },
            {
                "test_id": test1.id,
                "question_text": "A shopkeeper sells an article at a discount of 20% on the marked price and still makes a profit of 25%. If the cost price is ₹480, what was the marked price?",
                "option_a": "₹600",
                "option_b": "₹720",
                "option_c": "₹750",
                "option_d": "₹800",
                "correct_option": "C",
                "explanation": "Cost Price = ₹480. Profit = 25%, so Selling Price = 480 * 1.25 = ₹600. Discount = 20%, so Selling Price = 80% of Marked Price. 0.8 * MP = 600 => MP = 600 / 0.8 = ₹750.",
                "category": "Quantitative",
                "marks": 2
            },
            {
                "test_id": test1.id,
                "question_text": "A train 180 meters long is running at a speed of 72 km/h. How many seconds will it take to cross an electric pole?",
                "option_a": "7.5 seconds",
                "option_b": "9 seconds",
                "option_c": "10 seconds",
                "option_d": "12 seconds",
                "correct_option": "B",
                "explanation": "Speed = 72 * (5/18) = 20 m/s. Distance to cross pole = length of train = 180 m. Time = Distance / Speed = 180 / 20 = 9 seconds.",
                "category": "Quantitative",
                "marks": 2
            },
            {
                "test_id": test1.id,
                "question_text": "In how many different ways can the letters of the word 'LEADER' be arranged?",
                "option_a": "720",
                "option_b": "360",
                "option_c": "120",
                "option_d": "480",
                "correct_option": "B",
                "explanation": "The word 'LEADER' has 6 letters, where 'E' appears 2 times. Total permutations = 6! / 2! = 720 / 2 = 360.",
                "category": "Quantitative",
                "marks": 2
            },
            {
                "test_id": test1.id,
                "question_text": "The sum of ages of 5 children born at the intervals of 3 years each is 50 years. What is the age of the youngest child?",
                "option_a": "4 years",
                "option_b": "5 years",
                "option_c": "6 years",
                "option_d": "7 years",
                "correct_option": "A",
                "explanation": "Let ages be x, x+3, x+6, x+9, x+12. Sum = 5x + 30 = 50 => 5x = 20 => x = 4 years.",
                "category": "Quantitative",
                "marks": 2
            }
        ]

        # Questions for Test 2 (Logical Reasoning)
        q_logical = [
            {
                "test_id": test2.id,
                "question_text": "Pointing to a photograph, Rohit said, 'She is the daughter of my grandfather's only son.' How is the person in the photograph related to Rohit?",
                "option_a": "Mother",
                "option_b": "Sister",
                "option_c": "Aunt",
                "option_d": "Cousin",
                "correct_option": "B",
                "explanation": "Grandfather's only son is Rohit's father. Daughter of Rohit's father is Rohit's sister.",
                "category": "Logical",
                "marks": 2
            },
            {
                "test_id": test2.id,
                "question_text": "Find the missing number in the sequence: 4, 9, 25, 49, 121, ?",
                "option_a": "144",
                "option_b": "169",
                "option_c": "196",
                "option_d": "225",
                "correct_option": "B",
                "explanation": "These are squares of consecutive prime numbers: 2²=4, 3²=9, 5²=25, 7²=49, 11²=121. The next prime number is 13, and 13² = 169.",
                "category": "Logical",
                "marks": 2
            },
            {
                "test_id": test2.id,
                "question_text": "Statements: (1) All mangoes are fruits. (2) Some fruits are sweet. Conclusion I: Some mangoes are sweet. Conclusion II: All sweet things are fruits.",
                "option_a": "Only Conclusion I follows",
                "option_b": "Only Conclusion II follows",
                "option_c": "Neither I nor II follows",
                "option_d": "Both I and II follow",
                "correct_option": "C",
                "explanation": "From the given premises, sweet fruits might not overlap with mangoes, so I doesn't necessarily follow. And not all sweet things need to be fruits, so II doesn't follow. Neither follows.",
                "category": "Logical",
                "marks": 2
            },
            {
                "test_id": test2.id,
                "question_text": "In a certain code, 'PYTHON' is written as 'QZWILM'. How is 'CODING' written in that code?",
                "option_a": "DPEJOH",
                "option_b": "DPCHMH",
                "option_c": "DNCHOH",
                "option_d": "DQEJMI",
                "correct_option": "A",
                "explanation": "Each letter is shifted by +1 in the alphabet (P->Q, Y->Z, T->U/W etc.). C(+1)->D, O(+1)->P, D(+1)->E, I(+1)->J, N(+1)->O, G(+1)->H => DPEJOH.",
                "category": "Logical",
                "marks": 2
            }
        ]

        # Questions for Test 3 (CS Fundamentals & SQL)
        q_cs = [
            {
                "test_id": test3.id,
                "question_text": "In relational database management, what does the 'I' in the ACID transaction model guarantee?",
                "option_a": "Integrity of indexes across partitioned shards",
                "option_b": "Isolation of concurrent transactions from one another",
                "option_c": "Immutability of past audit log records",
                "option_d": "Instantaneous disk serialization without write cache",
                "correct_option": "B",
                "explanation": "Isolation ensures that concurrent execution of transactions leaves the database in the same state as if they were executed sequentially.",
                "category": "DBMS",
                "marks": 3
            },
            {
                "test_id": test3.id,
                "question_text": "Which SQL clause is used to filter records that have been aggregated by a GROUP BY statement?",
                "option_a": "WHERE",
                "option_b": "HAVING",
                "option_c": "FILTER",
                "option_d": "QUALIFY",
                "correct_option": "B",
                "explanation": "WHERE filters rows before aggregation occurs; HAVING filters grouped summary rows after the aggregation is computed.",
                "category": "SQL",
                "marks": 3
            },
            {
                "test_id": test3.id,
                "question_text": "What is the worst-case time complexity of searching for an element in a Balanced Binary Search Tree (such as AVL or Red-Black Tree)?",
                "option_a": "O(1)",
                "option_b": "O(log N)",
                "option_c": "O(N)",
                "option_d": "O(N log N)",
                "correct_option": "B",
                "explanation": "Because the tree remains height-balanced with max height proportional to log₂(N), worst-case search, insertion, and deletion are guaranteed O(log N).",
                "category": "DSA",
                "marks": 3
            },
            {
                "test_id": test3.id,
                "question_text": "Which condition is NOT one of the Coffman conditions required for a deadlock to occur in an Operating System?",
                "option_a": "Mutual Exclusion",
                "option_b": "Hold and Wait",
                "option_c": "Preemption by Priority Scheduler",
                "option_d": "Circular Wait",
                "correct_option": "C",
                "explanation": "The four Coffman conditions are: Mutual Exclusion, Hold and Wait, No Preemption, and Circular Wait. If preemption is allowed, deadlock is broken.",
                "category": "OS",
                "marks": 3
            }
        ]

        # Questions for Test 4 (Verbal)
        q_verbal = [
            {
                "test_id": test4.id,
                "question_text": "Choose the word most nearly opposite in meaning (Antonym) to: 'EPHEMERAL'",
                "option_a": "Transient",
                "option_b": "Perpetual",
                "option_c": "Fleeting",
                "option_d": "Evanescent",
                "correct_option": "B",
                "explanation": "'Ephemeral' means lasting for a very short time. The antonym is 'Perpetual', which means lasting forever or indefinitely.",
                "category": "Verbal",
                "marks": 2
            },
            {
                "test_id": test4.id,
                "question_text": "Identify the grammatically correct sentence:",
                "option_a": "Neither the manager nor the engineers was present at the scrum.",
                "option_b": "Neither the manager nor the engineers were present at the scrum.",
                "option_c": "Neither the manager or the engineers was present at the scrum.",
                "option_d": "Neither of the engineers were available today.",
                "correct_option": "B",
                "explanation": "When subject components are joined by 'neither... nor', the verb agrees in number with the nearer subject ('engineers' is plural => 'were').",
                "category": "Verbal",
                "marks": 2
            }
        ]

        all_questions = q_quant + q_logical + q_cs + q_verbal
        for q in all_questions:
            db.session.add(Question(**q))

        db.session.flush()

        # Seed initial test result for student1 to show populated dashboard charts
        test_result1 = TestResult(
            user_id=student1.id,
            test_id=test1.id,
            score=8.0,
            total_questions=5,
            correct_answers=4,
            wrong_answers=1,
            unanswered=0,
            percentage=80.0,
            time_taken_seconds=540,
            answers_json=json.dumps({"1": "B", "2": "C", "3": "B", "4": "B", "5": "C"}),
            passed=True,
            taken_at=datetime.now(timezone.utc) - timedelta(days=2)
        )
        test_result2 = TestResult(
            user_id=student1.id,
            test_id=test3.id,
            score=9.0,
            total_questions=4,
            correct_answers=3,
            wrong_answers=1,
            unanswered=0,
            percentage=75.0,
            time_taken_seconds=780,
            answers_json=json.dumps({"10": "B", "11": "B", "12": "B", "13": "A"}),
            passed=True,
            taken_at=datetime.now(timezone.utc) - timedelta(days=1)
        )
        db.session.add_all([test_result1, test_result2])

        # 6. COURSES & LESSONS
        courses_data = [
            {
                "title": "Placement DSA Sprint in Python & Java",
                "slug": "placement-dsa-sprint",
                "description": "Master high-frequency placement coding patterns: sliding window, two pointers, binary search variations, trees, graphs and dynamic programming with step-by-step visualizations.",
                "category": "Technical",
                "level": "Intermediate",
                "icon": "fa-code",
                "badge_color": "#06b6d4",
                "duration_hours": 32,
                "enrolled_count": 3480,
                "rating": 4.9,
                "is_popular": True
            },
            {
                "title": "Quantitative & Logical Aptitude Masterclass",
                "slug": "quant-logical-aptitude-masterclass",
                "description": "Speed tricks, shortcut formulas, Vedic math techniques, and time management strategies to clear round 1 aptitude tests of Tier-1 product and consulting companies.",
                "category": "Aptitude",
                "level": "All Levels",
                "icon": "fa-calculator",
                "badge_color": "#f59e0b",
                "duration_hours": 20,
                "enrolled_count": 4210,
                "rating": 4.8,
                "is_popular": True
            },
            {
                "title": "Modern Full-Stack Web Architecture",
                "slug": "modern-full-stack-web-architecture",
                "description": "Build production-grade applications from scratch with Python Flask, PostgreSQL, REST APIs, JWT authentication, and responsive modern frontend design.",
                "category": "Technical",
                "level": "Beginner to Advanced",
                "icon": "fa-layer-group",
                "badge_color": "#10b981",
                "duration_hours": 28,
                "enrolled_count": 2890,
                "rating": 4.9,
                "is_popular": True
            },
            {
                "title": "Ace The Technical & HR Interview Loop",
                "slug": "ace-technical-hr-interview-loop",
                "description": "Deconstruct the STAR methodology, behavioral questions, culture fit evaluations, salary negotiation strategies, and how to discuss complex architecture confidently.",
                "category": "Communication",
                "level": "All Levels",
                "icon": "fa-user-tie",
                "badge_color": "#8b5cf6",
                "duration_hours": 14,
                "enrolled_count": 2150,
                "rating": 4.7,
                "is_popular": False
            }
        ]

        for c_info in courses_data:
            course = Course(**c_info)
            db.session.add(course)
            db.session.flush()

            # Add lessons for each course
            lesson1 = Lesson(
                course_id=course.id,
                title="Course Overview & Roadmap to Day 1 Readiness",
                order_num=1,
                duration_mins=18,
                content="Welcome to this placement roadmap. In this module, we dissect the hiring expectations of top product companies and service companies. You will establish your baseline problem-solving speed and setup your daily preparation cadence.",
                key_takeaways="• Analyze company hiring rounds and cutoff percentiles.\n• Setup continuous practice tracking.\n• Build an interview-ready Git repository."
            )
            lesson2 = Lesson(
                course_id=course.id,
                title="Core Principles, Mental Models & Cheat Sheets",
                order_num=2,
                duration_mins=28,
                content="We break down fundamental patterns rather than memorizing individual solutions. We focus on identifying problem constraints and mapping them to the most efficient data structure or technique.",
                code_example="# Example: Fast & Slow Pointer Cycle Detection\ndef hasCycle(head):\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n        if slow == fast:\n            return True\n    return False",
                key_takeaways="• Recognize constraints: N <= 10^5 implies O(N log N) or O(N).\n• Two-pointer symmetry on sorted vs unsorted inputs.\n• Space vs time trade-offs in recursive call stacks."
            )
            lesson3 = Lesson(
                course_id=course.id,
                title="Mock Problem Walkthrough & Edge Case Handling",
                order_num=3,
                duration_mins=35,
                content="In this live walk-through, we tackle complex placement problems under strict time constraints. Watch how to articulate thought processes aloud to the interviewer and structure clean code.",
                key_takeaways="• Always clarify inputs and edge cases before coding.\n• Dry run your logic with a small test case.\n• Calculate time and space complexity upfront."
            )
            db.session.add_all([lesson1, lesson2, lesson3])

        # 7. RESUME FOR STUDENT 1
        resume1 = Resume(
            user_id=student1.id,
            title="Software Engineer - Core Resume",
            template_name="modern_cyber",
            full_name="Rahul Sharma",
            email="rahul.sharma@axiompath.com",
            phone="+91 98765 43210",
            location="Bengaluru, India",
            github="https://github.com/rahul-sharma-dev",
            linkedin="https://linkedin.com/in/rahul-sharma-axiom",
            portfolio="https://rahulsharma.dev",
            summary="Passionate and results-driven software engineering graduate with hands-on expertise in Python, full-stack web development, and relational databases. Strong foundation in Data Structures, Algorithms, and Object-Oriented Design with 300+ solved algorithmic problems. Eager to contribute to scalable cloud architectures.",
            education_json=json.dumps([
                {
                    "degree": "B.Tech in Computer Science & Engineering",
                    "institution": "Vellore Institute of Technology (VIT)",
                    "year": "2022 - 2026",
                    "score": "8.85 CGPA"
                },
                {
                    "degree": "Senior Secondary (Class XII CBSE)",
                    "institution": "Delhi Public School, R.K. Puram",
                    "year": "2020 - 2022",
                    "score": "95.4%"
                }
            ]),
            experience_json=json.dumps([
                {
                    "role": "Software Engineering Intern",
                    "company": "TechNova Solutions",
                    "duration": "May 2025 - July 2025",
                    "description": "Architected RESTful endpoints in Python/Flask serving 50,000 daily API calls. Reduced slow database query latencies by 32% using composite B-tree indexes and Redis caching."
                }
            ]),
            projects_json=json.dumps([
                {
                    "title": "AXIOMPATH Recruitment Prep Engine",
                    "tech": "Python, Flask, SQLite, Bootstrap 5, Chart.js",
                    "description": "Developed an end-to-end career readiness portal featuring timed adaptive aptitude assessments, live resume generation, and job tracking workflows."
                },
                {
                    "title": "High-Throughput Distributed Rate Limiter",
                    "tech": "Golang, Redis, Token Bucket, Docker",
                    "description": "Engineered a distributed API rate limiting service enforcing sliding window algorithms across multi-region server clusters."
                }
            ]),
            skills_json=json.dumps([
                "Python", "JavaScript", "SQL", "Flask", "React", "Data Structures & Algorithms", "Git", "Docker", "RESTful APIs", "PostgreSQL"
            ]),
            certifications_json=json.dumps([
                "AWS Certified Cloud Practitioner (2025)",
                "HackerRank 5-Star Gold Badge in Problem Solving & Python",
                "DeepLearning.AI Machine Learning Specialization"
            ]),
            achievements_json=json.dumps([
                "Secured Global Rank 142 in Codeforces Div 3 Round #840",
                "First Place Winner - VIT HackSprint 2024 among 120 collegiate teams",
                "Maintained 8.8+ CGPA across all 6 semesters"
            ])
        )
        db.session.add(resume1)

        # 8. TESTIMONIALS
        testimonials_data = [
            {
                "student_name": "Priya Nambiar",
                "role": "Backend Engineer",
                "company_placed": "Razorpay",
                "package_lpa": "18.5 LPA",
                "quote": "AXIOMPATH completely transformed my placement journey. The company-specific mock tests and technical interview cheat sheets matched exactly what was asked in the Razorpay machine coding round!",
                "college": "NIT Surathkal",
                "graduation_year": 2025,
                "avatar_initials": "PN",
                "is_featured": True
            },
            {
                "student_name": "Aditya Verma",
                "role": "Software Development Engineer",
                "company_placed": "Swiggy",
                "package_lpa": "16.0 LPA",
                "quote": "The aptitude timed simulator built my speed and accuracy under pressure. I went from being rejected in first rounds to securing two Dream offers in campus placements.",
                "college": "BMS College of Engineering, Bengaluru",
                "graduation_year": 2025,
                "avatar_initials": "AV",
                "is_featured": True
            },
            {
                "student_name": "Meera Krishnan",
                "role": "Full Stack Engineer",
                "company_placed": "CRED",
                "package_lpa": "22.0 LPA",
                "quote": "The Resume Builder created a clean, ATS-compliant resume that immediately started getting shortlists. The system design and Python deep-dives were world class.",
                "college": "PES University",
                "graduation_year": 2025,
                "avatar_initials": "MK",
                "is_featured": True
            },
            {
                "student_name": "Rohan Deshmukh",
                "role": "Systems Engineer (Digital)",
                "company_placed": "TCS Digital",
                "package_lpa": "9.0 LPA",
                "quote": "I cleared TCS Digital in the very first attempt thanks to the curated aptitude and coding questions on AXIOMPATH. Highly recommended for every engineering graduate!",
                "college": "COEP Technological University, Pune",
                "graduation_year": 2025,
                "avatar_initials": "RD",
                "is_featured": True
            }
        ]

        for t_info in testimonials_data:
            db.session.add(Testimonial(**t_info))

        db.session.commit()
        print("Database successfully seeded with realistic enterprise data!")
        print(f"Admin Account: admin@axiompath.com / Admin@123")
        print(f"Student Account: rahul.sharma@axiompath.com / Student@123")

if __name__ == "__main__":
    seed_database()
