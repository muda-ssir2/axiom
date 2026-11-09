from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_required, current_user
from models import db, Test, Question, TestResult, Course, Lesson
import json

prep_bp = Blueprint('preparation', __name__, url_prefix='/preparation')

# ----------------- APTITUDE & TESTS -----------------

@prep_bp.route('/aptitude')
def aptitude():
    tests = Test.query.filter_by(is_active=True).all()
    categories = ['Quantitative Aptitude', 'Logical Reasoning', 'Verbal Ability', 'Technical Coding', 'Full Placement Mock']
    
    user_results = {}
    if current_user.is_authenticated:
        for t in tests:
            latest = TestResult.query.filter_by(user_id=current_user.id, test_id=t.id).order_by(TestResult.taken_at.desc()).first()
            if latest:
                user_results[t.id] = latest

    return render_template(
        'aptitude.html',
        tests=tests,
        categories=categories,
        user_results=user_results
    )


@prep_bp.route('/aptitude/test/<int:test_id>')
@login_required
def take_test(test_id):
    test = Test.query.get_or_404(test_id)
    questions = test.questions.all()
    if not questions:
        flash("This test currently has no questions configured. Please select another test.", "warning")
        return redirect(url_for('preparation.aptitude'))

    return render_template('test_runner.html', test=test, questions=questions)


@prep_bp.route('/aptitude/test/<int:test_id>/submit', methods=['POST'])
@login_required
def submit_test(test_id):
    test = Test.query.get_or_404(test_id)
    questions = test.questions.all()

    user_answers = {}
    correct_count = 0
    wrong_count = 0
    unanswered_count = 0
    total_marks_earned = 0.0

    time_taken = request.form.get('time_taken_seconds', type=int) or 0

    for q in questions:
        field_name = f"question_{q.id}"
        ans = request.form.get(field_name)
        if ans:
            user_answers[str(q.id)] = ans
            if ans.upper() == q.correct_option.upper():
                correct_count += 1
                total_marks_earned += q.marks
            else:
                wrong_count += 1
                # Negative marking 0.25 of mark
                total_marks_earned -= (q.marks * 0.25)
        else:
            user_answers[str(q.id)] = ""
            unanswered_count += 1

    total_marks_earned = max(0.0, total_marks_earned)
    total_possible_marks = sum(q.marks for q in questions) or 1
    pct = round((total_marks_earned / total_possible_marks) * 100, 1)
    passed = pct >= 50.0 or total_marks_earned >= test.passing_marks

    result = TestResult(
        user_id=current_user.id,
        test_id=test.id,
        score=round(total_marks_earned, 2),
        total_questions=len(questions),
        correct_answers=correct_count,
        wrong_answers=wrong_count,
        unanswered=unanswered_count,
        percentage=pct,
        time_taken_seconds=time_taken,
        answers_json=json.dumps(user_answers),
        passed=passed
    )
    db.session.add(result)
    db.session.commit()

    flash(f"Test completed! You scored {round(total_marks_earned, 1)} / {total_possible_marks} ({pct}%).", "success")
    return redirect(url_for('preparation.test_result', result_id=result.id))


@prep_bp.route('/aptitude/result/<int:result_id>')
@login_required
def test_result(result_id):
    result = TestResult.query.get_or_404(result_id)
    if result.user_id != current_user.id and not current_user.is_admin:
        abort(403)

    user_choices = {}
    if result.answers_json:
        try:
            user_choices = json.loads(result.answers_json)
        except Exception:
            user_choices = {}

    questions = result.test.questions.all()
    return render_template(
        'test_result.html',
        result=result,
        test=result.test,
        questions=questions,
        user_choices=user_choices
    )


# ----------------- TECHNICAL PREPARATION -----------------

@prep_bp.route('/technical')
def technical():
    modules = [
        {'id': 'python', 'title': 'Python for Placements', 'icon': 'fa-python', 'badge': 'Core Stack', 'topics': ['Data Structures', 'OOPs in Python', 'Decorators & Generators', 'Collections & Algorithms', 'Common Tricky Output Questions']},
        {'id': 'dsa', 'title': 'Data Structures & Algorithms', 'icon': 'fa-code-branch', 'badge': 'High Priority', 'topics': ['Arrays & Strings', 'Linked Lists & Trees', 'Binary Search & Two Pointers', 'Dynamic Programming', 'Graph BFS/DFS']},
        {'id': 'dbms', 'title': 'DBMS & SQL Mastery', 'icon': 'fa-database', 'badge': 'Database', 'topics': ['ACID Properties', 'Normalization 1NF-BCNF', 'Complex SQL Joins', 'Indexing & B-Trees', 'Transactions & Concurrency']},
        {'id': 'os', 'title': 'Operating Systems', 'icon': 'fa-microchip', 'badge': 'CS Fundamentals', 'topics': ['Process vs Thread', 'CPU Scheduling Algorithms', 'Deadlocks & Banker’s Algorithm', 'Virtual Memory & Paging', 'Semaphore & Mutex']},
        {'id': 'networks', 'title': 'Computer Networks', 'icon': 'fa-network-wired', 'badge': 'CS Fundamentals', 'topics': ['OSI & TCP/IP Stack', 'TCP 3-Way Handshake', 'DNS & HTTP/HTTPS Lifecycle', 'Subnetting & IP Addressing', 'WebSockets & Socket Programming']},
        {'id': 'java', 'title': 'Java & Object-Oriented Design', 'icon': 'fa-java', 'badge': 'Enterprise', 'topics': ['Java Memory Model & GC', 'OOP Pillars & SOLID', 'Collections Framework', 'Multithreading & Synchronization', 'Java 8 Streams & Lambdas']},
        {'id': 'cpp', 'title': 'C and Modern C++', 'icon': 'fa-terminal', 'badge': 'Systems', 'topics': ['Pointers & Dynamic Allocation', 'Memory Leaks & Smart Pointers', 'STL Containers & Iterators', 'Templates & Metaprogramming', 'Virtual Tables & Polymorphism']},
        {'id': 'aiml', 'title': 'AI & Machine Learning Foundations', 'icon': 'fa-robot', 'badge': 'Emerging Tech', 'topics': ['Supervised vs Unsupervised', 'Gradient Descent & Loss Functions', 'Neural Network Architectures', 'LLMs & Prompt Engineering', 'Model Evaluation & Precision-Recall']}
    ]
    return render_template('technical.html', modules=modules)


@prep_bp.route('/technical/<topic>')
def technical_topic(topic):
    # Dynamic topic guide
    topic_data = get_topic_content(topic)
    if not topic_data:
        flash("Selected technical track topic coming soon!", "info")
        return redirect(url_for('preparation.technical'))
    return render_template('technical_topic.html', topic=topic_data)


# ----------------- INTERVIEW PREPARATION -----------------

@prep_bp.route('/interview')
def interview():
    company_packs = [
        {'name': 'TCS Digital / Prime', 'color': '#0284c7', 'rounds': '3 Rounds: Online Test + Tech + MR/HR', 'focus': 'DSA, SQL, Cloud Concepts, Aptitude Speed', 'salary': '7.0 - 9.0 LPA'},
        {'name': 'Infosys DSE & Specialist', 'color': '#3b82f6', 'rounds': '3 Rounds: HackWithInfy / Online + Technical + Leadership', 'focus': 'Competitive Programming, Java/Python, System Architecture', 'salary': '6.5 - 9.5 LPA'},
        {'name': 'Razorpay / Fintech SDE', 'color': '#06b6d4', 'rounds': '4 Rounds: Machine Coding + Problem Solving + LLD + Culture', 'focus': 'Clean Architecture, REST APIs, Concurrency, Database Design', 'salary': '14.0 - 22.0 LPA'},
        {'name': 'Deloitte USI (Analyst / Dev)', 'color': '#10b981', 'rounds': '3 Rounds: Versant + Tech Interview + Partner Round', 'focus': 'Consulting Mindset, SQL, Web Dev, Behavioral STAR Scenarios', 'salary': '7.6 - 11.5 LPA'},
        {'name': 'Amazon SDE-1 Fresher', 'color': '#f59e0b', 'rounds': '4 Rounds: Online Assessment + 3 Technical Onsite Loops', 'focus': 'LeetCode Medium/Hard, Trees/Graphs, 14 Leadership Principles', 'salary': '18.0 - 28.0 LPA'},
        {'name': 'Accolite Digital', 'color': '#8b5cf6', 'rounds': '3 Rounds: Accolite Eduthrill + Deep Tech + HR', 'focus': 'Core Java/C++, Matrix Algorithms, Recursion, Puzzles', 'salary': '8.0 - 12.0 LPA'}
    ]

    hr_questions = [
        {
            'question': 'Tell me about yourself and your journey in technology.',
            'tip': 'Use the Past-Present-Future structure. Highlight projects, passion for problem-solving, and why this company excites you.',
            'sample_answer': 'I am a final-year Computer Science student passionate about full-stack engineering and cloud-native systems. During my college years, I built multiple production-style apps including an automated placement tracker and an API gateway. Last summer, I interned where I reduced query latencies by 35% through SQL query optimization. Now, I am excited to bring my technical foundation and rapid learning abilities to your engineering team.'
        },
        {
            'question': 'Tell me about a time you faced a difficult bug or project roadblock.',
            'tip': 'Apply the STAR Framework (Situation, Task, Action, Result). Quantify impact and share lessons learned.',
            'sample_answer': 'During a 36-hour hackathon, our team encountered severe race conditions in payment webhooks. As lead backend developer, I isolated the issue using structured logs, implemented optimistic locking in SQLite/PostgreSQL, and simulated high concurrency using Locust. We successfully delivered zero duplicate payments and placed 2nd out of 80 teams.'
        },
        {
            'question': 'Why should we hire you over other qualified candidates?',
            'tip': 'Combine solid technical skills, adaptability, high agency, and strong cultural alignment.',
            'sample_answer': 'Beyond having strong foundations in DSA and Python, I bring strong ownership and product thinking. I do not just write code that passes tests; I understand user impact, optimize for edge cases, and learn new frameworks within days.'
        },
        {
            'question': 'Where do you see yourself in 3 to 5 years?',
            'tip': 'Focus on technical depth, domain mastery, and taking up architectural or mentorship responsibilities.',
            'sample_answer': 'In 3 years, I see myself as a dependable core engineer owning key microservices and mentoring junior engineers. In 5 years, I aim to lead high-impact architectural decisions while continuously staying abreast of emerging technologies like AI/LLM integrations.'
        }
    ]

    return render_template('interview.html', company_packs=company_packs, hr_questions=hr_questions)


@prep_bp.route('/interview/mock')
@login_required
def mock_interview():
    return render_template('mock_interview.html')


# ----------------- COMMUNICATION SKILLS -----------------

@prep_bp.route('/communication')
def communication():
    gd_topics = [
        {'title': 'Will Artificial Intelligence replace Entry-Level Software Engineers?', 'category': 'Technology & Future of Work', 'key_points': ['AI increases developer velocity rather than eliminating jobs', 'Demand for problem-solvers, system designers, and prompt engineers is rising', 'Soft skills and requirements gathering become key differentiators']},
        {'title': 'Remote vs Hybrid vs On-site: The Optimal Work Culture for Tech Startups', 'category': 'Corporate Dynamics', 'key_points': ['Hybrid balances deep work focus and collaborative whiteboard sessions', 'Junior mentorship requires intentional pairing in remote settings', 'Global talent access vs team camaraderie']},
        {'title': 'Data Privacy vs Innovation in the Era of Generative AI', 'category': 'Ethics & Governance', 'key_points': ['DPDP Act in India and GDPR guidelines in Europe', 'Proprietary IP leakage in public LLM APIs', 'Open-source on-prem models as viable enterprise alternatives']},
        {'title': 'Electric Vehicles in India: Infrastructure Bottlenecks vs Green Growth', 'category': 'Socio-Economic', 'key_points': ['Fast-charging grids in Tier-2 and Tier-3 cities', 'Grid load management and renewable source integration', 'Battery recycling and domestic manufacturing incentives']}
    ]
    return render_template('communication.html', gd_topics=gd_topics)


# ----------------- COURSES -----------------

@prep_bp.route('/courses')
def courses():
    all_courses = Course.query.order_by(Course.enrolled_count.desc()).all()
    categories = ['All', 'Technical', 'Aptitude', 'System Design', 'Communication']
    selected_cat = request.args.get('category', 'All')

    if selected_cat != 'All':
        courses_list = [c for c in all_courses if c.category.lower() == selected_cat.lower()]
    else:
        courses_list = all_courses

    return render_template('courses.html', courses=courses_list, categories=categories, selected_category=selected_cat)


@prep_bp.route('/courses/<slug>')
def course_detail(slug):
    course = Course.query.filter_by(slug=slug).first_or_404()
    lessons = course.lessons.all()
    active_lesson_id = request.args.get('lesson_id', type=int)
    
    current_lesson = None
    if active_lesson_id:
        current_lesson = Lesson.query.get(active_lesson_id)
    if not current_lesson and lessons:
        current_lesson = lessons[0]

    return render_template('course_detail.html', course=course, lessons=lessons, current_lesson=current_lesson)


# Helper function for technical topic content
def get_topic_content(topic_slug):
    topics = {
        'python': {
            'title': 'Python Placement Mastery',
            'headline': 'From Core Fundamentals to Advanced Python Engineering',
            'summary': 'Master memory management, generators, decorators, complex list comprehensions, multithreading GIL considerations, and high-frequency technical interview questions.',
            'cheat_sheet': [
                {'concept': 'Mutable vs Immutable', 'detail': 'Lists, Dictionaries, Sets are mutable. Ints, Floats, Strings, Tuples, Frozensets are immutable.'},
                {'concept': 'GIL (Global Interpreter Lock)', 'detail': 'A mutex that prevents multiple native threads from executing Python bytecodes simultaneously. Use multiprocessing for CPU-bound tasks, threading/asyncio for I/O-bound tasks.'},
                {'concept': 'Generators & `yield`', 'detail': 'Produce memory-efficient streams of data one at a time without loading entire sequences into RAM.'},
                {'concept': 'Decorators', 'detail': 'Functions that modify the behavior of other functions without modifying their code. Common in auth, logging, caching.'}
            ],
            'sample_code': '''# Top Interview Problem: Custom LRU Cache in Python using OrderedDict
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        # Move key to end to show recent use
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            # Pop the first (least recently used) item
            self.cache.popitem(last=False)'''
        },
        'dsa': {
            'title': 'Data Structures & Algorithms Sprint',
            'headline': 'Crack Product-Based & Service-Based Coding Rounds',
            'summary': 'Learn patterns rather than memorizing individual LeetCode problems: Sliding Window, Two Pointers, Fast & Slow Pointers, Monotonic Stack, Backtracking, and Dynamic Programming.',
            'cheat_sheet': [
                {'concept': 'Two Pointers Pattern', 'detail': 'Applicable on sorted arrays for Pair Sum, 3Sum, Container With Most Water, Trapping Rain Water.'},
                {'concept': 'Sliding Window', 'detail': 'Ideal for Substring problems, Longest Subarray with sum K, Maximum Sum Subarray of size K.'},
                {'concept': 'Topological Sort (Kahn\'s Algorithm)', 'detail': 'DAG node ordering with In-degree count and BFS queue. Key for Course Schedule, Build Dependencies.'},
                {'concept': 'Dynamic Programming States', 'detail': 'Identify overlapping subproblems and optimal substructure. Decide memoization vs tabulation.'}
            ],
            'sample_code': '''# Two Pointers: Trapping Rain Water O(N) Time, O(1) Space
def trap(height: list[int]) -> int:
    if not height: return 0
    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    water = 0

    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            water += left_max - height[left]
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water += right_max - height[right]

    return water'''
        },
        'dbms': {
            'title': 'DBMS & SQL Placement Blueprint',
            'headline': 'ACID Properties, Normalization, Query Optimization, and Window Functions',
            'summary': 'Every placement drive asks SQL queries with JOINs, GROUP BY, HAVING, and window functions like DENSE_RANK(). Master them here.',
            'cheat_sheet': [
                {'concept': 'ACID Guarantees', 'detail': 'Atomicity (all or nothing), Consistency (valid state), Isolation (concurrent safety), Durability (persisted on disk).'},
                {'concept': 'Clustered vs Non-Clustered Index', 'detail': 'Clustered determines physical order of rows (only 1 per table, usually Primary Key). Non-clustered creates separate B-Tree pointing to data rows.'},
                {'concept': 'Window Functions', 'detail': '`ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `LEAD()`, `LAG()` calculate results across rows without collapsing them like GROUP BY.'}
            ],
            'sample_code': '''-- High Frequency SQL: Find 3rd Highest Salary by Department
WITH RankedSalaries AS (
    SELECT 
        emp_id,
        emp_name,
        dept_id,
        salary,
        DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) as salary_rank
    FROM employees
)
SELECT emp_id, emp_name, dept_id, salary
FROM RankedSalaries
WHERE salary_rank = 3;'''
        }
    }
    return topics.get(topic_slug)
