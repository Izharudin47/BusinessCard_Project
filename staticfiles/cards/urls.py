from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("u/<slug:profile_url>/", views.profile_view, name="profile"),
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),

    # Business card routes
    path("add-business-card/", views.add_business_card, name="add_business_card"),
    path("cards/", views.businesscard_list, name="businesscard_list"),
    path("cards/<str:profile_url>/", views.businesscard_profile, name="businesscard_profile"),
    path("delete-business-card/<int:card_id>/", views.delete_business_card, name="delete_business_card"),

]
