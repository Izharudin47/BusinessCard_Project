from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.text import slugify
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .models import UserProfile, BusinessCard
from .forms import RegisterForm, UserProfileForm, BusinessCardForm
import uuid


# Home page
def home(request):
    return render(request, "cards/home.html")


# Register new user + profile
def register(request):
    if request.method == "POST":
        user_form = RegisterForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            email = user_form.cleaned_data["email"]

            # prevent duplicate email
            if User.objects.filter(email=email).exists():
                messages.error(request, "This email is already registered. Please login instead.")
                return redirect("login")

            # create user
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data["password"])
            user.save()

            # create profile
            profile = profile_form.save(commit=False)
            profile.user = user

            # generate unique profile_url (slug)
            if not profile.profile_url:
                base_slug = slugify(user.username)
                slug = base_slug
                counter = 1
                while UserProfile.objects.filter(profile_url=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                profile.profile_url = slug

            profile.save()

            # auto login
            login(request, user)
            return redirect("profile", profile_url=profile.profile_url)
    else:
        user_form = RegisterForm()
        profile_form = UserProfileForm()

    return render(request, "cards/register.html", {
        "user_form": user_form,
        "profile_form": profile_form
    })


# Login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("profile", profile_url=user.userprofile.profile_url)
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "cards/login.html")


# Logout
def logout_view(request):
    logout(request)
    return redirect("home")


# Profile page
def profile_view(request, profile_url):
    profile = get_object_or_404(UserProfile, profile_url=profile_url)
    return render(request, "cards/profile.html", {"profile": profile})


# Admin dashboard (only staff can access)
@staff_member_required
def admin_dashboard(request):
    users = UserProfile.objects.all()
    return render(request, "cards/admin_dashboard.html", {"users": users})


# Add business card (must be logged in)
@login_required
def add_business_card(request):
    if request.method == "POST":
        form = BusinessCardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user  # track which admin added it

            # generate unique profile_url if not set
            if not card.profile_url:
                base_slug = slugify(card.full_name)  # ✅ FIXED from card.name → card.full_name
                unique_id = uuid.uuid4().hex[:6]
                slug = f"{base_slug}-{unique_id}"
                while BusinessCard.objects.filter(profile_url=slug).exists():
                    unique_id = uuid.uuid4().hex[:6]
                    slug = f"{base_slug}-{unique_id}"
                card.profile_url = slug

            card.save()
            return redirect("businesscard_list")
    else:
        form = BusinessCardForm()
    return render(request, "cards/add_business_card.html", {"form": form})


# List all business cards
@login_required
def businesscard_list(request):
    cards = BusinessCard.objects.all()
    return render(request, "cards/businesscard_list.html", {"cards": cards})


# Public profile view (unique URL for each business card)
def businesscard_profile(request, profile_url):
    card = get_object_or_404(BusinessCard, profile_url=profile_url)
    return render(request, "cards/businesscard_profile.html", {"card": card})


def delete_business_card(request, card_id):
    card = get_object_or_404(BusinessCard, id=card_id, user=request.user)
    if request.method == "POST":
        card.delete()
        return redirect('businesscard_list')