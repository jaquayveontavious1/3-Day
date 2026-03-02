from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse
from .models import SprintUserStatus,SprintHistory
from django.views.decorators.csrf import csrf_exempt
from .models import Sprint,Goal
from django.utils import timezone
import json
from django.contrib.auth import logout
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        login(request, user)
        return redirect('dashboard')

    return render(request, 'signup.html')


@login_required
def dashboard_view(request):
    sprints = Sprint.objects.filter(status='ACTIVE', visibility='public').select_related('user')
    sprint_data = []

    for sprint in sprints:
        # Fetch progress and status for sprint owner
        user_status = SprintUserStatus.objects.filter(
            user=sprint.user,
            sprint=sprint
        ).first()

        goals = sprint.goals.all()
        total = goals.count()
        completed = goals.filter(is_completed=True).count()

        sprint_data.append({
            'id': sprint.id,
            'title': sprint.title,
            'user': sprint.user,
            'progress': user_status.progress if user_status else 0,
            'status': user_status.status if user_status else "Not Started",
            'total': total,
            'completed': completed
        })

    paginator = Paginator(sprint_data, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard.html', {'page_obj': page_obj})

@login_required
def dashboard_view(request):
    sprints = Sprint.objects.filter(status='ACTIVE', visibility='public').select_related('user').order_by('-id')
    sprint_data = []

    for sprint in sprints:
        # Fetch progress and status for sprint owner
        user_status = SprintUserStatus.objects.filter(
            user=sprint.user,
            sprint=sprint
        ).first()

        goals = sprint.goals.all()
        total = goals.count()
        completed = goals.filter(is_completed=True).count()

        sprint_data.append({
            'id': sprint.id,
            'title': sprint.title,
            'user': sprint.user,
            'progress': user_status.progress if user_status else 0,
            'status': user_status.status if user_status else "Not Started",
            'total': total,
            'completed': completed
        })

    paginator = Paginator(sprint_data, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # ✅ Check if a sprint was just completed, and remove session immediately
    sprint_completed_id = request.session.pop('sprint_completed', None)

    context = {
        'page_obj': page_obj,
        'sprint_completed_id': sprint_completed_id
    }

    return render(request, 'dashboard.html', context)


@login_required
def create_sprint_view(request) :
    existing = Sprint.objects.filter(user=request.user, status="ACTIVE").first()
    if existing:
        return redirect('dashboard')
    
    if request.method == "POST":
        title = request.POST.get('title')
        goal1 = request.POST.get('goal1')
        goal2 = request.POST.get('goal2')
        goal3 = request.POST.get('goal3')

        if title and goal1 and goal2 and goal3:
            sprint = Sprint.objects.create(user=request.user,title=title,start_datetime=timezone.now())

            Goal.objects.create(sprint=sprint,text=goal1)
            Goal.objects.create(sprint=sprint, text=goal2)
            Goal.objects.create(sprint=sprint, text=goal3)

            return redirect('dashboard')
    return render(request, 'create_sprint.html')
@login_required
def update_my_sprint(request):
    sprint = Sprint.objects.filter(user=request.user, status="ACTIVE").first()
    if not sprint:
        return redirect("dashboard")

    goals = sprint.goals.all()
    user_status, _ = SprintUserStatus.objects.get_or_create(user=request.user, sprint=sprint)

    if request.method == "POST":
        for goal in goals:
            goal.is_completed = f"goal_{goal.id}" in request.POST
            goal.save()

        total_goals = goals.count()
        completed_goals = goals.filter(is_completed=True).count()
        progress = int((completed_goals * 100) / total_goals) if total_goals > 0 else 0
        user_status.progress = progress

        # Update status automatically
        if progress == 0:
            user_status.status = "Not Started"
        elif progress < 100:
            user_status.status = "In Progress"
        else:
            user_status.status = "Completed"

        # Save optional dropdown override
        posted_status = request.POST.get("status")
        if posted_status:
            user_status.status = posted_status

        user_status.save()

        # ✅ Only set session if sprint is COMPLETED
        sprint.check_and_update_status()  # This will set sprint.status to COMPLETED if 100%
        if sprint.status == "COMPLETED":
            request.session['sprint_completed'] = sprint.id

        return redirect("dashboard")

    context = {
        "sprint": sprint,
        "goals": goals,
        "user_status": user_status,
        "remaining_seconds": sprint.remaining_seconds
    }
    return render(request, "update_my_sprint.html", context)


@login_required
def sprint_history_view(request):
    # Fetch only completed or failed sprints of the logged-in user
    sprints = Sprint.objects.filter(
        user=request.user,
        status__in=['COMPLETED', 'FAILED']
    ).order_by('-end_datetime', '-created_at')

    sprint_data = []
    for sprint in sprints:
        total = sprint.goals.count()
        completed = sprint.goals.filter(is_completed=True).count()
        sprint_data.append({
            'id': sprint.id,
            'title': sprint.title,
            'total': total,
            'completed': completed,
            'status': sprint.status,
            'completed_at': sprint.end_datetime if sprint.status == 'FAILED' else sprint.created_at
        })

    paginator = Paginator(sprint_data, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'sprint_history.html', {'page_obj': page_obj})



@login_required
def leaderboard_view(request):
    # Annotate each user with the number of completed sprints
    users = User.objects.annotate(
        completed_sprints=Count(
            'sprints',
            filter=Q(sprints__status='COMPLETED')
        )
    ).filter(completed_sprints__gt=0).order_by('-completed_sprints')

    return render(request, 'leaderboard.html', {'users': users})

def logout_view(request):
    # Clear any session keys you want
    request.session.flush()
    logout(request)
    return redirect('login')

from django.contrib.auth.views import LogoutView

class CustomLogoutView(LogoutView):
    http_method_names = ['get', 'post'] 