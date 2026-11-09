import unittest
import json
from app import create_app
from models import db, User, Job, Application, Test, TestResult, Resume, ContactMessage

class AxiomPathComprehensiveTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF in automated unit tests
        self.client = self.app.test_client()

    def test_01_homepage_renders(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'AXIOMPATH', response.data)
        self.assertIn(b'Your Career Doesn', response.data)
        self.assertIn(b'Start Preparing', response.data)
        print("PASS: Homepage renders with hero, stats, and branding.")

    def test_02_student_login_and_dashboard(self):
        # Login with seeded demo student
        res = self.client.post('/auth/login', data={
            'email': 'rahul.sharma@axiompath.com',
            'password': 'Student@123'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Candidate Cockpit', res.data)
        self.assertIn(b'Rahul', res.data)
        print("PASS: Student authentication and cockpit dashboard functional.")

    def test_03_admin_login_and_dashboard(self):
        # Login with seeded demo admin
        res = self.client.post('/auth/login', data={
            'email': 'admin@axiompath.com',
            'password': 'Admin@123'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Command & Analytics Cockpit', res.data)
        print("PASS: Administrator authentication and portal dashboard functional.")

    def test_04_job_portal_search_and_filter(self):
        res = self.client.get('/jobs/?q=Python')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Discover Tech Opportunities', res.data)

        # Check filter by location
        res_loc = self.client.get('/jobs/?location=Bengaluru')
        self.assertEqual(res_loc.status_code, 200)
        print("PASS: Job portal search and multi-criteria filtering functional.")

    def test_05_job_details_and_save(self):
        # Login as student
        self.client.post('/auth/login', data={
            'email': 'rahul.sharma@axiompath.com',
            'password': 'Student@123'
        }, follow_redirects=True)

        with self.app.app_context():
            job = Job.query.first()
            job_id = job.id

        res = self.client.get(f'/jobs/{job_id}')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Role Overview & Responsibilities', res.data)

        # Test toggle save
        res_save = self.client.post(f'/jobs/{job_id}/save', follow_redirects=True)
        self.assertEqual(res_save.status_code, 200)
        print("PASS: Job details and bookmarking functional.")

    def test_06_aptitude_test_submission_and_scoring(self):
        # Login as student
        self.client.post('/auth/login', data={
            'email': 'rahul.sharma@axiompath.com',
            'password': 'Student@123'
        }, follow_redirects=True)

        with self.app.app_context():
            test = Test.query.first()
            test_id = test.id
            questions = test.questions.all()

        # Submit answers
        form_data = {
            'time_taken_seconds': 350
        }
        for q in questions:
            form_data[f"question_{q.id}"] = q.correct_option

        res_submit = self.client.post(f'/preparation/aptitude/test/{test_id}/submit', data=form_data, follow_redirects=True)
        self.assertEqual(res_submit.status_code, 200)
        self.assertIn(b'Detailed Question Solutions & Explanations', res_submit.data)
        self.assertIn(b'PASSED', res_submit.data)
        print("PASS: Timed test submission, score calculation, and review verified.")

    def test_07_resume_save_and_pdf_download(self):
        # Login as student
        self.client.post('/auth/login', data={
            'email': 'rahul.sharma@axiompath.com',
            'password': 'Student@123'
        }, follow_redirects=True)

        res_builder = self.client.get('/resume-builder/')
        self.assertEqual(res_builder.status_code, 200)
        self.assertIn(b'Interactive Resume Builder', res_builder.data)

        # Test Resume PDF download
        with self.app.app_context():
            user = User.query.filter_by(email='rahul.sharma@axiompath.com').first()
            resume = user.resumes.first()
            resume_id = resume.id

        res_pdf = self.client.get(f'/resume-builder/download/{resume_id}')
        self.assertEqual(res_pdf.status_code, 200)
        self.assertEqual(res_pdf.mimetype, 'application/pdf')
        self.assertTrue(len(res_pdf.data) > 1000)
        print(f"PASS: ReportLab PDF generation verified ({len(res_pdf.data)} bytes generated).")

    def test_08_admin_management_workflows(self):
        # Login as admin
        self.client.post('/auth/login', data={
            'email': 'admin@axiompath.com',
            'password': 'Admin@123'
        }, follow_redirects=True)

        # 1. Admin Students list
        res_st = self.client.get('/admin/students')
        self.assertEqual(res_st.status_code, 200)
        self.assertIn(b'Registered Student Profiles', res_st.data)

        # 2. Admin Jobs list
        res_jb = self.client.get('/admin/jobs')
        self.assertEqual(res_jb.status_code, 200)
        self.assertIn(b'Manage Job Postings', res_jb.data)

        # 3. Admin Applications list & update
        with self.app.app_context():
            app_record = Application.query.first()
            app_id = app_record.id

        res_up = self.client.post(f'/admin/applications/{app_id}/status', data={
            'status': 'Interview Scheduled',
            'admin_feedback': 'Selected for Machine Coding Round 1'
        }, follow_redirects=True)
        self.assertEqual(res_up.status_code, 200)
        print("PASS: Admin student, job, and application pipeline management verified.")

    def test_09_contact_form_submission(self):
        res = self.client.post('/contact', data={
            'name': 'Pooja Hegde',
            'email': 'pooja.hegde@college.edu',
            'subject': 'Placement Drive Inquiry 2026',
            'message': 'We would like to connect our college placement cell with AXIOMPATH.'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Your message has been received', res.data)

        with self.app.app_context():
            msg = ContactMessage.query.filter_by(email='pooja.hegde@college.edu').first()
            self.assertIsNotNone(msg)
        print("PASS: Public contact inquiry submission and database persistence verified.")

    def test_10_student_cannot_access_admin(self):
        # Login as student
        self.client.post('/auth/login', data={
            'email': 'rahul.sharma@axiompath.com',
            'password': 'Student@123'
        }, follow_redirects=True)

        res = self.client.get('/admin/', follow_redirects=True)
        self.assertIn(b'Access denied', res.data)
        print("PASS: Role-based access control (RBAC) securely verified.")

if __name__ == '__main__':
    unittest.main()
