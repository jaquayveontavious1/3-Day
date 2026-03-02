# 🚀 3-Day Builder

### A productivity-focused web application that allows users to create, track, and complete 3-day sprints. Users can monitor their progress, update sprint goals, and view their sprint history.

---

## 📚 Table of Contents

- Features  
- Technologies Used  
- Installation  
- Usage  
- Models  
- Screenshots  
- Future Improvements  
- License  

---

## ✨ Features

- User authentication (Signup, Login, Logout)
- Create 3-day sprints with 3 main goals
- Update goal completion status with progress reflected in real-time
- Progress bar and status tracking for each sprint
- Sprint history for users to view completed and failed sprints
- Community leaderboard showing top-performing users
- Congratulatory animation when a sprint is completed
- Timer counting down from 72 hours per sprint
- Pagination for dashboard view

---

## 🛠 Technologies Used

- **Backend:** Django, Django REST Framework  
- **Frontend:** HTML, CSS, JavaScript  
- **Database:** SQLite (default), can be switched to MySQL  
- **Authentication:** Django built-in authentication system  

---

## 📦 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/3-day-builder.git
cd 3-day-builder
```

### 2️⃣ Create and activate a virtual environment

```bash
python -m venv venv
```

#### ▶ Linux / macOS

```bash
source venv/bin/activate
```

#### ▶ Windows

```bash
venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Apply migrations

```bash
python manage.py migrate
```

### 5️⃣ Create superuser (optional)

```bash
python manage.py createsuperuser
```

### 6️⃣ Run the server

```bash
python manage.py runserver
```

### 7️⃣ Visit in browser

```
http://127.0.0.1:8000/
```

---

## 📖 Usage

1. Sign up as a new user.  
2. Create a sprint with 3 goals (maximum 3-day duration).  
3. Update goals as you complete them; progress bars and status update automatically.  
4. View dashboard for active sprints and progress of other users.  
5. Check sprint history to see completed or failed sprints.  
6. Community leaderboard ranks users by sprints completed.  

---

## 📊 Models

### 👤 User
Uses Django’s default `User` model:

```text
username
email
password
```

### 🏃 Sprint

```text
user: ForeignKey → User
title: CharField
start_datetime: DateTimeField
end_datetime: DateTimeField (auto 72 hours after start)
status: Active / Completed / Failed
visibility: Public / Private
```

### 🎯 Goal

```text
sprint: ForeignKey → Sprint
text: CharField
is_completed: BooleanField
```

### 📈 SprintUserStatus

```text
user: ForeignKey → User
sprint: ForeignKey → Sprint
progress: IntegerField (0–100)
status: Not Started / In Progress / Paused / Completed
```

---

## 🚀 Future Improvements

- Add detailed user profiles  
- Integrate payment / gamification features  
- Real-time notifications for sprint deadlines  
- UX/UI improvements and responsive design  
- Mobile-friendly version  

---

## 📜 License

MIT License © 2026
