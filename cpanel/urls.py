from django.urls import path
from . import views_en, views_ar

app_name = 'cpanel'

urlpatterns = [
    path('', views_en.main, name="main"),
    path('ar/', views_ar.mainRTL, name="mainrtl"),
    path('dashboard/', views_en.dashboard, name="dashboard"),
    path('ar/dashboard/', views_ar.dashboard, name="ar_dashboard"),
    # Cases
    path('case_add/', views_en.case_add, name="case_add"),
    path('case_edit/<id>/', views_en.case_edit, name="case_edit"),
    path('cases/', views_en.case_list, name="case_list"),
    path('ar/case_add/', views_ar.case_add, name="ar_case_add"),
    path('ar/case_edit/<id>/', views_ar.case_edit, name="ar_case_edit"),
    path('ar/cases/', views_ar.case_list, name="ar_case_list"),
    # Projects
    path('project_add/', views_en.project_add, name="project_add"),
    path('project_edit/<id>/', views_en.project_edit, name="project_edit"),
    path('projects/', views_en.project_list, name="project_list"),
    path('ar/project_add/', views_ar.project_add, name="ar_project_add"),
    path('ar/project_edit/<id>/', views_ar.project_edit, name="ar_project_edit"),
    path('ar/projects/', views_ar.project_list, name="ar_project_list"),
    # Main Category
    path('main_category_add/', views_en.main_category_add, name="main_category_add"),
    path('main_category_edit/<id>/', views_en.main_category_edit, name="main_category_edit"),
    path('main_categories/', views_en.main_category_list, name="main_category_list"),
    path('ar/main_category_add/', views_ar.main_category_add, name="ar_main_category_add"),
    path('ar/main_category_edit/<id>/', views_ar.main_category_edit, name="ar_main_category_edit"),
    path('ar/main_categories/', views_ar.main_category_list, name="ar_main_category_list"),
    # Sub Category
    path('sub_category_add/', views_en.sub_category_add, name="sub_category_add"),
    path('sub_category_edit/<id>/', views_en.sub_category_edit, name="sub_category_edit"),
    path('sub_categories/', views_en.sub_category_list, name="sub_category_list"),
    path('ar/sub_category_add/', views_ar.sub_category_add, name="ar_sub_category_add"),
    path('ar/sub_category_edit/<id>/', views_ar.sub_category_edit, name="ar_sub_category_edit"),
    path('ar/sub_categories/', views_ar.sub_category_list, name="ar_sub_category_list"),
    # Agents
    path('agent_add/', views_en.agent_add, name="agent_add"),
    path('agent_edit/<id>/', views_en.agent_edit, name="agent_edit"),
    path('agents/', views_en.agent_list, name="agent_list"),
    path('ar/agent_add/', views_ar.agent_add, name="ar_agent_add"),
    path('ar/agent_edit/<id>/', views_ar.agent_edit, name="ar_agent_edit"),
    path('ar/agents/', views_ar.agent_list, name="ar_agent_list"),
    # Donors
    path('donor_add/', views_en.donor_add, name="donor_add"),
    path('donor_edit/<id>/', views_en.donor_edit, name="donor_edit"),
    path('donors/', views_en.donor_list, name="donor_list"),
    path('ar/donor_add/', views_ar.donor_add, name="ar_donor_add"),
    path('ar/donor_edit/<id>/', views_ar.donor_edit, name="ar_donor_edit"),
    path('ar/donors/', views_ar.donor_list, name="ar_donor_list"),
    # Donations
    path('donation_add/', views_en.donation_add, name="donation_add"),
    path('donation_edit/<id>/', views_en.donation_edit, name="donation_edit"),
    path('donations/', views_en.donation_list, name="donation_list"),
    path('donation_view/<id>/', views_en.donation_view, name="donation_view"),
    path('ar/donation_add/', views_ar.donation_add, name="ar_donation_add"),
    path('ar/donation_edit/<id>/', views_ar.donation_edit, name="ar_donation_edit"),
    path('ar/donations/', views_ar.donation_list, name="ar_donation_list"),
    path('ar/donation_view/<id>/', views_ar.donation_view, name="ar_donation_view"),
    # Develope
    path('inputs/', views_en.inputs, name="inputs"),

]
