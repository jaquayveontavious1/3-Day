<h1>3-Day Builder</h1>

<h3>A productivity-focused web application that allows users to create, track, and complete 3-day sprints. Users can monitor their progress, update sprint goals, and view their sprint history.</h3>

<hr>

<h2>Table of Contents</h2>
<ul>
<li>Features</li>

<li>Technologies Used</li>

<li>Installation</li>

<li>Usage</li>

<li>Models</li>

<li>Screenshots</li>

<li>Future Improvements</li>

<li>License</li>
</ul>

<hr>
<h2>Features</h2>
<ul>
<li>User authentication (Signup, Login, Logout)</li>

<li>Create 3-day sprints with 3 main goals</li>

<li>Update goal completion status with progress reflected in real-time</li>

<li>Progress bar and status tracking for each sprint</li>

<li>Sprint history for users to view completed and failed sprints</li>

<li>Community leaderboard showing top-performing users</li>

<li>Congratulatory animation when a sprint is completed</li>

<li>Timer counting down from 72 hours per sprint</li>

<li>Pagination for dashboard view</li>
</ul>

<hr>
<h2>Technologies Used</h2>
<ul>
<li>Backend: Django, Django REST Framework</li>

<li>Frontend: HTML, CSS, JavaScript</li>

<li>Database: SQLite (default), can be switched to MySQL</li>

<li>Authentication: Django built-in auth system</li>
</ul>

<hr>


<h2>Installation</h2>
<ol>
<li>Clone the repository</li>
```
git clone 
cd 3-day-builder

<li>Create and activate a virtual environment</li>
```
python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows
```

<li>Install dependencies</li>
```
pip install -r requirements.txt

```
Apply migrations

python manage.py migrate


Create superuser (optional)

python manage.py createsuperuser


Run the server

python manage.py runserver


Visit in browser

http://127.0.0.1:8000/

Usage

Signup as a new user.

Create a sprint with 3 goals (maximum 3-day duration).

Update goals as you complete them; progress bars and status update automatically.

View dashboard for active sprints and progress of other users.

Check sprint history to see completed or failed sprints.

Community leaderboard ranks users by sprints completed.

Models
User (Django default)

username

email

password

Sprint

user: ForeignKey to User

title: CharField

start_datetime: DateTimeField

end_datetime: DateTimeField (auto 72 hours after start)

status: Active / Completed / Failed

visibility: public/private

Goal

sprint: ForeignKey to Sprint

text: CharField

is_completed: BooleanField

SprintUserStatus

user: ForeignKey to User

sprint: ForeignKey to Sprint

progress: IntegerField (0-100)

status: Not Started / In Progress / Paused / Completed

Screenshots

(Optional: Add screenshots of dashboard, update goals page, leaderboard, and sprint history)

Future Improvements

Add detailed user profiles

Integrate payment/gamification features

Real-time notifications for sprint deadlines

UX/UI improvements and responsive design

Mobile-friendly version

License

MIT License © 2026