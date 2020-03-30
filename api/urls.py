from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'api'
urlpatterns = [
    path('token/<username>/', login_required(views.TokenView.as_view()), name='token'),
    path('users/', login_required(views.UserView.as_view()), name='users'),
    path('user/<username>/', login_required(views.UserDetailView.as_view()), name='user_detail'),
    path('login_registration/', views.LoginRegistrationView.as_view(), name='login_registration'),
    path('donors/', views.DonorView.as_view(), name='donors'),
    path('donor/<username>/', views.DonorDetailView.as_view(), name='donor'),
    path('slider_images/', views.SliderImageView.as_view(), name='slider_images'),
    path('sub_categories/', views.SubCategoryView.as_view(), name='sub_categories'),
    path('projects/', views.ProjectView.as_view(), name='projects'),
    path('urgent_projects/', views.UrgentProjectView.as_view(), name='urgent_projects'),
    path('our_sponsors/', views.SponsorView.as_view(), name='our_sponsors'),
    path('mersal_numbers/', views.MersalNumbersView.as_view(), name='mersal_numbers'),
    path('cases/', views.CaseView.as_view(), name='cases'),
    path('urgent_cases/', views.UrgentCaseView.as_view(), name='urgent_cases'),
    path('donations/', views.DonationView.as_view(), name='donations'),
    path('donations/<username>/', views.DonationDetailView.as_view(), name='donation_detail'),
    path('case_by_category/<id>/', views.CaseByCategory.as_view(), name='case_by_category'),
]
