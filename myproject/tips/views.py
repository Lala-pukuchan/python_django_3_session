from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from .models import Tip
from .forms import TipForm

def homepage(request):
    # 1) Get existing tips list (ordered by newest first)
    tips = Tip.objects.order_by('-created_at')

    # 2) Process new post if POST method
    if request.method == 'POST':
        # Only accept posts from logged-in users
        if request.user.is_authenticated:
            form = TipForm(request.POST)
            if form.is_valid():
                tip = form.save(commit=False)
                tip.author = request.user  # Set authenticated user as author
                tip.save()
            # Redirect to homepage regardless of success or failure
            return redirect('homepage')
        else:
            # Unauthorized users cannot post
            return redirect('homepage')

    # 3) Display list and form if GET method
    else:
        if request.user.is_authenticated:
            form = TipForm()
        else:
            form = None

    context = {
        'tips': tips,
        'form': form,
    }
    return render(request, 'tips/homepage.html', context)

def register_view(request):
    # Redirect to home if already logged in
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Create User
            user = User.objects.create_user(username=username, password=password)
            # Login immediately after creation
            auth_login(request, user)
            messages.success(request, f'User {username} has been created and logged in.')
            return redirect('homepage')
        else:
            # Re-render the page with validation errors
            return render(request, 'tips/register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'tips/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # If authentication is successful, form.user contains the User object
            user = form.user
            # Process login
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('homepage')
        else:
            return render(request, 'tips/login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'tips/login.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    return redirect('homepage')

@login_required
def tip_upvote(request, tip_id):
    tip = get_object_or_404(Tip, id=tip_id)
    user = request.user

    # Remove from downvoters if already downvoted
    if tip.downvoters.filter(id=user.id).exists():
        tip.downvoters.remove(user)

    # Toggle upvote: remove if exists, add if not
    if tip.upvoters.filter(id=user.id).exists():
        tip.upvoters.remove(user)
        messages.info(request, "Upvote canceled.")
    else:
        tip.upvoters.add(user)
        messages.success(request, "You upvoted the tip.")

    return redirect('homepage')


@login_required
def tip_downvote(request, tip_id):
    tip = get_object_or_404(Tip, id=tip_id)
    user = request.user

    # Check permission to downvote
    if tip.author != user and not user.has_perm('tips.can_downvote_tip'):
        messages.error(request, "You do not have permission to downvote this tip.")
        return redirect('homepage')

    # Remove from upvoters if already upvoted
    if tip.upvoters.filter(id=user.id).exists():
        tip.upvoters.remove(user)

    # Toggle downvote: remove if exists, add if not
    if tip.downvoters.filter(id=user.id).exists():
        tip.downvoters.remove(user)
        messages.info(request, "Downvote canceled.")
    else:
        tip.downvoters.add(user)
        messages.warning(request, "You downvoted the tip.")

    return redirect('homepage')

@login_required
def tip_delete(request, tip_id):
    tip = get_object_or_404(Tip, id=tip_id)
    # if user is the author or has permission to delete tips
    if (tip.author == request.user) or (request.user.has_perm('tips.delete_tip')):
        tip.delete()
        messages.success(request, "Tip has been deleted.")
    else:
        messages.error(request, "You do not have permission to delete this tip.")

    return redirect('homepage')
