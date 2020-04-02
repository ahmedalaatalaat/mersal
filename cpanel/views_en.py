from django.shortcuts import render, get_object_or_404, redirect
from main.utils import get_object_or_none
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from .models import *
from .from_excel import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime


# Main Pages
@login_required(login_url='login')
def dashboard(request):
    current_month = datetime.now().month
    context = {
        'title': 'Dashboard',
        'agents': Agent.objects.all().count(),
        'cases': Case.objects.all().count(),
        'projects': Project.objects.all().count(),
        'donations': Donation.objects.all().count(),
        'this_month_donation': Donation.objects.filter(date__month=current_month).count(),
        'donors': Donor.objects.all().count(),
        'new_donors_this_month': Donor.objects.filter(join_date__month=current_month).count(),
    }
    return render(request, 'cpanel/Others/dashboard.html', context)


@login_required(login_url='login')
def main(request):
    context = {
        'title': 'base',
    }
    return render(request, 'cpanel/base.html', context)


@login_required(login_url='login')
def profile(request):
    user = request.user
    if request.is_ajax():
        if request.method == 'POST':
            user = get_object_or_none(User, username=request.POST.get('username'))
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')

            if request.POST.get('password'):
                if user.check_password(request.POST.get('old_password')):
                    user.set_password(request.POST.get('password'))

        user.save()
    context = {
        'user': user,
        'title': 'Profile'
    }
    return render(request, 'cpanel/Others/profile.html', context)


# Case Views
@login_required(login_url='login')
def case_add(request):
    charitable_activities = Sub_Category.objects.all()

    # Add data
    if request.is_ajax():
        if request.method == 'POST':
            case = get_object_or_none(Case, code=request.POST.get('code'))
            if case:
                return HttpResponseBadRequest('This Case is already exists')

            is_urgent = True if request.POST.get(
                'is_urgent') == 'on' else False

            sub_category = get_object_or_404(Sub_Category, id=request.POST.get('sub_category'))

            contribution = Contribution.objects.create(
                amount=request.POST.get('amount'),
                description=request.POST.get('description'),
                is_urgent=is_urgent,
            )

            Case.objects.create(
                case_id=contribution,
                code=request.POST.get('code'),
                sub_category=sub_category,
            )

    context = {
        'title': 'Add Case',
        'charitable_activities': charitable_activities
    }
    return render(request, 'cpanel/cases/case_add.html', context)


@login_required(login_url='login')
def case_edit(request, id):
    # get data
    charitable_activities = Sub_Category.objects.all()
    case = get_object_or_404(Case, case_id=id)
    contribution = get_object_or_404(Contribution, id=id)

    # Save new data
    if request.is_ajax():
        if request.method == 'POST':
            sub_category = get_object_or_404(Sub_Category, id=request.POST.get('sub_category'))
            is_urgent = True if request.POST.get(
                'is_urgent') == 'on' else False

            contribution.amount = request.POST.get('amount')
            contribution.description = request.POST.get('description')
            contribution.is_urgent = is_urgent
            case.sub_category = sub_category

            case.save()
            contribution.save()

    context = {
        'title': 'Edit Case',
        'charitable_activities': charitable_activities,
        'case': case
    }
    return render(request, 'cpanel/cases/case_edit.html', context)


@login_required(login_url='login')
def case_list(request):
    cases = Case.objects.all()

    # Delete
    if request.is_ajax():
        if request.method == 'POST':
            get_object_or_none(Case, case_id=request.POST.get('id')).delete()
            get_object_or_none(
                Contribution, id=request.POST.get('id')).delete()

    # Search
    if request.method == 'GET':
        query = request.GET.get('search')
        if query:
            cases = cases.filter(Q(case_id__id__icontains=query) |
                                 Q(code__icontains=query) |
                                 Q(case_id__amount__icontains=query) |
                                 Q(case_id__is_urgent__icontains=query)).distinct()

    # Import from excel
    if request.method == 'POST':
        import_cases(request.FILES.get('file'))  # handel excel files

    # Pagination
    cases_pages = Paginator(cases, 20)
    cases = cases_pages.get_page(request.GET.get('page'))
    current_page = request.GET.get('page') if request.GET.get('page') else 1
    context = {
        'title': 'Cases list',
        'cases': cases,
        'pages': str(cases_pages.num_pages),
        'current_page': str(current_page)
    }
    return render(request, 'cpanel/cases/case_list.html', context)


# Project Views
@login_required(login_url='login')
def project_add(request):
    # Add data
    if request.is_ajax():
        if request.method == 'POST':
            is_urgent = True if request.POST.get(
                'is_urgent') == 'on' else False

            contribution = Contribution.objects.create(
                amount=request.POST.get('amount'),
                description=request.POST.get('description'),
                is_urgent=is_urgent,
            )

            Project.objects.create(
                project_id=contribution,
                name=request.POST.get('name'),
            )
    context = {
        'title': 'Project Add',
    }
    return render(request, 'cpanel/projects/project_add.html', context)


@login_required(login_url='login')
def project_edit(request, id):
    # get data
    project = get_object_or_404(Project, project_id=id)
    contribution = get_object_or_404(Contribution, id=id)

    # Save new data
    if request.is_ajax():
        if request.method == 'POST':
            is_urgent = True if request.POST.get(
                'is_urgent') == 'on' else False
            contribution.amount = request.POST.get('amount')
            contribution.description = request.POST.get('description')
            contribution.is_urgent = is_urgent

            contribution.save()

    context = {
        'title': 'Project Edit',
        'project': project
    }
    return render(request, 'cpanel/projects/project_edit.html', context)


@login_required(login_url='login')
def project_list(request):
    projects = Project.objects.all()

    # Delete
    if request.is_ajax():
        if request.method == 'POST':
            get_object_or_none(
                Project, project_id=request.POST.get('id')).delete()
            get_object_or_none(
                Contribution, id=request.POST.get('id')).delete()

    # Search
    if request.method == 'GET':
        query = request.GET.get('search')
        if query:
            projects = projects.filter(Q(project_id__id__icontains=query) |
                                       Q(name__icontains=query) |
                                       Q(project_id__amount__icontains=query) |
                                       Q(project_id__is_urgent__icontains=query)).distinct()

    # Import from excel
    if request.method == 'POST':
        import_projects()  # handel excel files

    # Pagination
    projects_pages = Paginator(projects, 20)
    projects = projects_pages.get_page(request.GET.get('page'))
    current_page = request.GET.get('page') if request.GET.get('page') else 1
    context = {
        'title': 'Projects List',
        'projects': projects,
        'pages': str(projects_pages.num_pages),
        'current_page': str(current_page)
    }
    return render(request, 'cpanel/projects/project_list.html', context)


# Main Category Views
@login_required(login_url='login')
def main_category_add(request):
    # Add data
    if request.is_ajax():
        if request.method == 'POST':
            main_category = Main_Category.objects.create(
                english_name=request.POST.get('english_name'),
                arabic_name=request.POST.get('arabic_name')
            )
            if request.FILES.get('image'):
                main_category.image = request.FILES.get('image')
                main_category.save()

    context = {
        'title': 'Main Category Add',
    }
    return render(request, 'cpanel/Main Category/main_category_add.html', context)


@login_required(login_url='login')
def main_category_edit(request, id):
    main_category = get_object_or_404(Main_Category, id=id)
    if request.is_ajax():
        if request.method == 'POST':
            main_category.english_name = request.POST.get('english_name')
            main_category.arabic_name = request.POST.get('arabic_name')

            if request.FILES.get('image'):
                main_category.image = request.FILES.get('image')

            main_category.save()

    context = {
        'title': 'Main Category Edit',
        'main_category': main_category
    }
    return render(request, 'cpanel/Main Category/main_category_edit.html', context)


@login_required(login_url='login')
def main_category_list(request):
    main_categories = Main_Category.objects.all()

    # Delete
    if request.is_ajax():
        if request.method == 'POST':
            get_object_or_none(
                Main_Category, id=request.POST.get('id')).delete()

    # Search
    if request.method == 'GET':
        query = request.GET.get('search')
        if query:
            main_categories = main_categories.filter(
                Q(id__icontains=query) |
                Q(name__icontains=query)).distinct()

    # Import from excel
    if request.method == 'POST':
        import_Main_Categories()  # handel excel files

    # Pagination
    main_categories_pages = Paginator(main_categories, 20)
    main_categories = main_categories_pages.get_page(request.GET.get('page'))
    current_page = request.GET.get('page') if request.GET.get('page') else 1
    context = {
        'title': 'Main Categories List',
        'main_categories': main_categories,
        'pages': str(main_categories_pages.num_pages),
        'current_page': str(current_page)
    }
    return render(request, 'cpanel/Main Category/main_category_list.html', context)


# Sub Category Views
@login_required(login_url='login')
def sub_category_add(request):
    main_categories = Main_Category.objects.all()
    # Add data
    if request.is_ajax():
        if request.method == 'POST':
            main_category = get_object_or_404(
                Main_Category, id=request.POST.get('main_category'))
            sub_category = Sub_Category.objects.create(
                english_name=request.POST.get('english_name'),
                arabic_name=request.POST.get('arabic_name'),
                main_category=main_category
            )
            if request.FILES.get('image'):
                sub_category.image = request.FILES.get('image')
                sub_category.save()

    context = {
        'title': 'Sub Category Add',
        'main_categories': main_categories
    }
    return render(request, 'cpanel/Sub Category/sub_category_add.html', context)


@login_required(login_url='login')
def sub_category_edit(request, id):
    main_categories = Main_Category.objects.all()
    sub_category = get_object_or_404(Sub_Category, id=id)
    if request.is_ajax():
        if request.method == 'POST':
            main_category = get_object_or_404(
                Main_Category, id=request.POST.get('main_category'))

            sub_category.english_name = request.POST.get('english_name')
            sub_category.arabic_name = request.POST.get('arabic_name')
            sub_category.main_category = main_category

            if request.FILES.get('image'):
                sub_category.image = request.FILES.get('image')

            sub_category.save()

    context = {
        'title': 'Main Category Edit',
        'main_categories': main_categories,
        'sub_category': sub_category
    }
    return render(request, 'cpanel/Sub Category/sub_category_edit.html', context)


@login_required(login_url='login')
def sub_category_list(request):
    sub_categories = Sub_Category.objects.all()

    # Delete
    if request.is_ajax():
        if request.method == 'POST':
            get_object_or_none(
                Sub_Category, id=request.POST.get('id')).delete()

    # Search
    if request.method == 'GET':
        query = request.GET.get('search')
        if query:
            sub_categories = sub_categories.filter(
                Q(id__icontains=query) |
                Q(name__icontains=query) |
                Q(main_category__name__icontains=query)).distinct()

    # Import from excel
    if request.method == 'POST':
        import_Sub_Categories()  # handel excel files

    # Pagination
    sub_categories_pages = Paginator(sub_categories, 20)
    sub_categories = sub_categories_pages.get_page(request.GET.get('page'))
    current_page = request.GET.get('page') if request.GET.get('page') else 1
    context = {
        'title': 'Sub Categories List',
        'sub_categories': sub_categories,
        'pages': str(sub_categories_pages.num_pages),
        'current_page': str(current_page)
    }
    return render(request, 'cpanel/Sub Category/sub_category_list.html', context)


# Agent Views
@login_required(login_url='login')
def agent_add(request):
    if request.is_ajax():
        if request.method == 'POST':
            agent = get_object_or_none(
                User, username=request.POST.get('username'))
            if agent:
                return HttpResponseBadRequest('This Agent is already exists')

            user = User.objects.create_user(
                username=request.POST.get('username'),
                password=request.POST.get('password')
            )

            agent = Agent.objects.create(
                user=user,
                phone=request.POST.get('phone'),
            )
            if request.FILES.get('image'):
                agent.image = request.FILES.get('image')
                agent.save()

    context = {
        'title': 'Agent Add'
    }
    return render(request, 'cpanel/Agents/agent_add.html', context)


@login_required(login_url='login')
def agent_edit(request, id):
    agent = get_object_or_404(Agent, id=id)
    if request.is_ajax():
        if request.method == 'POST':
            agent.phone = request.POST.get('phone')

            # Handle password
            if request.POST.get('password'):
                user = get_object_or_none(
                    User, username=request.POST.get('username'))
                if user.check_password(request.POST.get('old_password')):
                    user.set_password(request.POST.get('password'))
                    user.save()

            if request.FILES.get('image'):
                agent.image = request.FILES.get('image')

            agent.save()

    context = {
        'title': 'Agent Edit',
        'agent': agent
    }
    return render(request, 'cpanel/Agents/agent_edit.html', context)


@login_required(login_url='login')
def agent_list(request):
    agents = Agent.objects.all()

    # Delete
    if request.is_ajax():
        if request.method == 'POST':
            get_object_or_none(Agent, id=request.POST.get('id')).delete()

    # Search
    if request.method == 'GET':
        query = request.GET.get('search')
        if query:
            agents = agents.filter(
                Q(id__icontains=query) |
                Q(user__username__icontains=query) |
                Q(phone__icontains=query)).distinct()

    # Import from excel
    if request.method == 'POST':
        import_Agents()  # handel excel files

    # Pagination
    agents_pages = Paginator(agents, 20)
    agents = agents_pages.get_page(request.GET.get('page'))
    current_page = request.GET.get('page') if request.GET.get('page') else 1
    context = {
        'title': 'Agents List',
        'agents': agents,
        'pages': str(agents_pages.num_pages),
        'current_page': str(current_page)
    }
    return render(request, 'cpanel/Agents/agent_list.html', context)


# Donor Views
@login_required(login_url='login')
def donor_add(request):
    if request.is_ajax():
        if request.method == 'POST':
            donor = get_object_or_none(
                User, username=request.POST.get('username'))
            if donor:
                return HttpResponseBadRequest('This Donor is already exists')

            user = User.objects.create_user(
                username=request.POST.get('username'),
                password=request.POST.get('password'),
            )
            Donor.objects.create(
                name=request.POST.get('name'),
                user=user,
                city_1=request.POST.get('city_1'),
                country_1=request.POST.get('country_1'),
                apartment_no_1=request.POST.get('apartment_no_1'),
                building_1=request.POST.get('building_1'),
                area_1=request.POST.get('area_1'),
                phone_1=request.POST.get('phone_1'),
                street_1=request.POST.get('street_1'),
                floor_1=request.POST.get('floor_1'),
                address_1=request.POST.get('address_1'),
                city_2=request.POST.get('city_2'),
                country_2=request.POST.get('country_2'),
                apartment_no_2=request.POST.get('apartment_no_2'),
                building_2=request.POST.get('building_2'),
                area_2=request.POST.get('area_2'),
                phone_2=request.POST.get('phone_2'),
                street_2=request.POST.get('street_2'),
                floor_2=request.POST.get('floor_2'),
                address_2=request.POST.get('address_2'))
    context = {
        'title': 'Donor Add'
    }
    return render(request, 'cpanel/Donors/donor_add.html', context)


@login_required(login_url='login')
def donor_edit(request, id):
    donor = get_object_or_404(Donor, id=id)
    if request.is_ajax():
        if request.method == 'POST':

            donor.name = request.POST.get('name')
            donor.city_1 = request.POST.get('city_1')
            donor.country_1 = request.POST.get('country_1')
            donor.apartment_no_1 = request.POST.get('apartment_no_1')
            donor.building_1 = request.POST.get('building_1')
            donor.area_1 = request.POST.get('area_1')
            donor.phone_1 = request.POST.get('phone_1')
            donor.street_1 = request.POST.get('street_1')
            donor.floor_1 = request.POST.get('floor_1')
            donor.address_1 = request.POST.get('address_1')
            donor.city_2 = request.POST.get('city_2')
            donor.country_2 = request.POST.get('country_2')
            donor.apartment_no_2 = request.POST.get('apartment_no_2')
            donor.building_2 = request.POST.get('building_2')
            donor.area_2 = request.POST.get('area_2')
            donor.phone_2 = request.POST.get('phone_2')
            donor.street_2 = request.POST.get('street_2')
            donor.floor_2 = request.POST.get('floor_2')
            donor.address_2 = request.POST.get('address_2')

            # Handle password
            if request.POST.get('password'):
                user = get_object_or_none(
                    User, username=request.POST.get('username'))
                if user.check_password(request.POST.get('old_password')):
                    user.set_password(request.POST.get('password'))
                    user.save()

            donor.save()

    context = {
        'title': 'Donor Edit',
        'donor': donor
    }
    return render(request, 'cpanel/Donors/donor_edit.html', context)


@login_required(login_url='login')
def donor_list(request):
    donors = Donor.objects.all()

    # Delete
    if request.is_ajax():
        if request.method == 'POST':
            get_object_or_none(Donor, id=request.POST.get('id')).delete()

    # Search
    if request.method == 'GET':
        query = request.GET.get('search')
        if query:
            donors = donors.filter(
                Q(name__icontains=query) |
                Q(user__username__icontains=query)).distinct()

    # Import from excel
    if request.method == 'POST':
        import_Donors()  # handel excel files

    # Pagination
    donors_pages = Paginator(donors, 20)
    donors = donors_pages.get_page(request.GET.get('page'))
    current_page = request.GET.get('page') if request.GET.get('page') else 1
    context = {
        'title': 'Donors List',
        'donors': donors,
        'pages': str(donors_pages.num_pages),
        'current_page': str(current_page)
    }
    return render(request, 'cpanel/Donors/donor_list.html', context)


# Donation Views
@login_required(login_url='login')
def donation_add(request):
    contributions = Contribution.objects.all()
    charitable_activities = Sub_Category.objects.all()

    if request.is_ajax():
        if request.method == 'POST':
            user = get_object_or_none(User, username=request.POST.get('donor'))
            donor = get_object_or_none(Donor, user=user)
            if not donor:
                return HttpResponseBadRequest('This Donor is not exists')

            contribution = get_object_or_none(
                Contribution, id=request.POST.get('contribution'))
            charitable_activity = get_object_or_none(
                Sub_Category, id=request.POST.get('charitable_activity'))

            Donation.objects.create(
                donor=donor,
                contribution=contribution,
                charitable_activity=charitable_activity,
                amount=request.POST.get('amount'),
                address_no=request.POST.get('address_no')
            )

    context = {
        'contributions': contributions,
        'charitable_activities': charitable_activities,
        'title': 'Donation Add'
    }
    return render(request, 'cpanel/Donations/donation_add.html', context)


@login_required(login_url='login')
def donation_edit(request, id):
    donation = get_object_or_404(Donation, id=id)
    contributions = Contribution.objects.all()
    charitable_activities = Sub_Category.objects.all()

    if request.is_ajax():
        if request.method == 'POST':
            contribution = get_object_or_none(
                Contribution, id=request.POST.get('contribution'))
            charitable_activity = get_object_or_none(
                Sub_Category, id=request.POST.get('charitable_activity'))
            donation.contribution = contribution
            donation.charitable_activity = charitable_activity
            donation.amount = request.POST.get('amount')
            donation.address_no = request.POST.get('address_no')
            donation.save()

    context = {
        'contributions': contributions,
        'charitable_activities': charitable_activities,
        'title': 'Donation Edit',
        'donation': donation
    }
    return render(request, 'cpanel/Donations/donation_edit.html', context)


@login_required(login_url='login')
def donation_list(request):
    donations = Donation.objects.all()

    # Delete
    if request.is_ajax():
        if request.method == 'POST':
            get_object_or_none(Donation, id=request.POST.get('id')).delete()

    # Search
    if request.method == 'GET':
        query = request.GET.get('search')
        if query:
            donations = donations.filter(
                Q(donor__name__icontains=query) |
                Q(assigned_agent__user__username__icontains=query) |
                Q(charitable_activity__name__icontains=query)).distinct()

    # Import from excel
    if request.method == 'POST':
        import_Donors()  # handel excel files

    # Pagination
    donations_pages = Paginator(donations, 20)
    donations = donations_pages.get_page(request.GET.get('page'))
    current_page = request.GET.get('page') if request.GET.get('page') else 1
    context = {
        'title': 'Donations List',
        'donations': donations,
        'pages': str(donations_pages.num_pages),
        'current_page': str(current_page)
    }
    return render(request, 'cpanel/Donations/donation_list.html', context)


@login_required(login_url='login')
def donation_view(request, id):
    donation = get_object_or_404(Donation, id=id)
    agents = Agent.objects.all()
    if request.is_ajax():
        if request.method == 'POST':
            collected = True if request.POST.get(
                'collected') == 'on' else False
            if request.POST.get('assigned_agent'):
                agent = get_object_or_none(
                    Agent, id=request.POST.get('assigned_agent'))
                donation.assigned_agent = agent

            donation.collected = collected
            donation.save()

    context = {
        'title': 'Donation View',
        'agents': agents,
        'donation': donation
    }
    return render(request, 'cpanel/Donations/donation_view.html', context)


# Authentication views
def login_view(request):
    if not request.user.is_authenticated:
        form = AuthenticationForm()
        error = False
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                if not user.is_staff:
                    error = True
                else:
                    login(request, user)
                    if request.GET.get('next'):
                        return redirect(request.GET.get('next'))
                    return redirect('cpanel:dashboard')
        context = {
            'form': form,
            'error': error
        }
        return render(request, 'cpanel/Auth/login.html', context)
    else:
        return redirect('cpanel:dashboard')


def lock_screen(request):
    form = AuthenticationForm()
    context = {
        'user': request.user,
        'form': form
    }

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('cpanel:dashboard')
        else:
            return redirect('login')

    if request.user.is_authenticated:
        logout(request)
        return render(request, 'cpanel/Auth/lock-screen.html', context)
    else:
        return redirect('login')


def logout_view(request):
    logout(request)
    return redirect('login')


# Slider Image Views
@login_required(login_url='login')
def slider_image_add(request):
    # Add data
    if request.is_ajax():
        if request.method == 'POST':
            slider_image = Slider_Image.objects.create(
                name=request.POST.get('name')
            )
            if request.FILES.get('image'):
                slider_image.image = request.FILES.get('image')
                slider_image.save()

    context = {
        'title': 'Slider Image Add',
    }
    return render(request, 'cpanel/Slider Image/slider_image_add.html', context)


@login_required(login_url='login')
def slider_image_edit(request, id):
    slider_image = get_object_or_404(Slider_Image, id=id)
    if request.is_ajax():
        if request.method == 'POST':
            slider_image.name = request.POST.get('name')

            if request.FILES.get('image'):
                slider_image.image = request.FILES.get('image')

            slider_image.save()

    context = {
        'title': 'Slider Image Edit',
        'slider': slider_image
    }
    return render(request, 'cpanel/Slider Image/slider_image_edit.html', context)


@login_required(login_url='login')
def slider_image_list(request):
    slider_images = Slider_Image.objects.all()
    # Delete
    if request.is_ajax():
        if request.method == 'POST':
            get_object_or_none(
                Slider_Image, id=request.POST.get('id')).delete()

    # Search
    if request.method == 'GET':
        query = request.GET.get('search')
        if query:
            slider_images = slider_images.filter(
                Q(id__icontains=query) |
                Q(name__icontains=query)).distinct()

    # Pagination
    slider_images_pages = Paginator(slider_images, 20)
    slider_images = slider_images_pages.get_page(request.GET.get('page'))
    current_page = request.GET.get('page') if request.GET.get('page') else 1
    context = {
        'title': 'Slider Images List',
        'slider_images': slider_images,
        'pages': str(slider_images_pages.num_pages),
        'current_page': str(current_page)
    }
    return render(request, 'cpanel/Slider Image/slider_image_list.html', context)


# Our Sponsors Views
@login_required(login_url='login')
def our_sponsor_add(request):
    # Add data
    if request.is_ajax():
        if request.method == 'POST':
            our_sponsor = Our_Sponsor.objects.create(
                name=request.POST.get('name')
            )
            if request.FILES.get('image'):
                our_sponsor.image = request.FILES.get('image')
                our_sponsor.save()

    context = {
        'title': 'Our Sponsor Add',
    }
    return render(request, 'cpanel/Our Sponsors/our_sponsor_add.html', context)


@login_required(login_url='login')
def our_sponsor_edit(request, id):
    our_sponsor = get_object_or_404(Our_Sponsor, id=id)
    if request.is_ajax():
        if request.method == 'POST':
            our_sponsor.name = request.POST.get('name')

            if request.FILES.get('image'):
                our_sponsor.image = request.FILES.get('image')

            our_sponsor.save()

    context = {
        'title': 'Our Sponsor Edit',
        'slider': our_sponsor
    }
    return render(request, 'cpanel/Our Sponsors/our_sponsor_edit.html', context)


@login_required(login_url='login')
def our_sponsor_list(request):
    our_sponsors = Our_Sponsor.objects.all()

    # Delete
    if request.is_ajax():
        if request.method == 'POST':
            get_object_or_none(
                Our_Sponsor, id=request.POST.get('id')).delete()

    # Search
    if request.method == 'GET':
        query = request.GET.get('search')
        if query:
            our_sponsors = our_sponsors.filter(
                Q(id__icontains=query) |
                Q(name__icontains=query)).distinct()

    # Pagination
    our_sponsors_pages = Paginator(our_sponsors, 20)
    our_sponsors = our_sponsors_pages.get_page(request.GET.get('page'))
    current_page = request.GET.get('page') if request.GET.get('page') else 1
    context = {
        'title': 'Slider Images List',
        'slider_images': our_sponsors,
        'pages': str(our_sponsors_pages.num_pages),
        'current_page': str(current_page)
    }
    return render(request, 'cpanel/Our Sponsors/our_sponsor_list.html', context)


# Error views
def error_400(request, exception):
    return render(request, 'cpanel/Error/400.html')


def error_403(request, exception):
    return render(request, 'cpanel/Error/403.html')


def error_404(request, exception):
    return render(request, 'cpanel/Error/404.html')


def error_500(request):
    return render(request, 'cpanel/Error/500.html')
