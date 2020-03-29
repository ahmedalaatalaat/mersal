from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from .serializers import *
from django.contrib.auth.models import User
from cpanel.models import *
from django.db.models import Q


# Users view
class UserView(APIView):
    def get(self, request):
        '''
        get all users
        Required Data:
        ()
        '''
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        '''
        add new user
        Required Data:
        (username, password)
        '''
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(username=request.data.get('username'), password=request.data.get('password'))
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    def get(self, request, username):
        '''
        get specific user data
        Required Data:
        ()
        '''
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, username):
        '''
        update user password
        Required Data:
        (old_password, new_password)
        '''
        user = get_object_or_404(User, username=username)
        if request.data.get('old_password'):
            if user.check_password(request.data.get('old_password')):
                user.set_password(request.data.get('new_password'))
                user.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        '''
        delete user
        Required Data:
        ()
        '''
        user = get_object_or_404(User, username=username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Login and Registration view
class LoginRegistrationView(APIView):
    def get(self, request):
        '''
        Login function
        Required Data:
        (username, password)
        '''
        user = get_object_or_404(User, username=request.data.get('username'))
        serializer = UserSerializer(user)
        if user.check_password(request.data.get('password')):
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        '''
        Registration function
        Required Data:
        (email, password, name, city, country)
        '''
        serializer = ResgistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=request.data.get('email'),
                password=request.data.get('password'))
            Donor.objects.create(
                name=request.data.get('name'),
                city_1=request.data.get('city'),
                country_1=request.data.get('country'),
                user=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Donors View
class DonorView(APIView):
    def get(self, request):
        '''
        get all the donors
        Required Data:
        ()
        '''
        donors = Donor.objects.all()
        serializer = DonorSerializer(donors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DonorDetailView(APIView):
    def get(self, request, username):
        '''
        get specific donor
        Required Data:
        ()
        '''
        user = get_object_or_404(User, username=username)
        donor = get_object_or_404(Donor, user=user)
        serializer = DonorSerializer(donor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, username):
        '''
        update specific donor
        Required Data:
        ('name', 'city_1', 'country_1', 'apartment_no_1', 'building_1', 'area_1', 'phone_1', 'street_1', 'floor_1', 'address_1', 'city_2', 'country_2', 'apartment_no_2', 'building_2', 'area_2', 'phone_2', 'street_2', 'floor_2', 'address_2')
        '''
        user = get_object_or_404(User, username=username)
        donor = get_object_or_404(Donor, user=user)
        serializer = DonorSerializer(donor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


# Slider Images views
class SliderImageView(APIView):
    def get(self, request):
        '''
        get slider images
        Required Data:
        ()
        '''
        images = Slider_Image.objects.all()
        serializer = SliderImageSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Sub Category views
class SubCategoryView(APIView):
    def get(self, request):
        '''
        get sub category
        Required Data:
        ()
        '''
        categories = Sub_Category.objects.all()
        serializer = SubCategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectView(APIView):
    def get(self, request):
        '''
        get projects
        Required Data:
        ()
        '''
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)

        # Calculate collected money for each project
        for item in serializer.data:
            collected = 0
            project_id = item.get('project_id').get('id')
            project_amount = item.get('project_id').get('amount')
            contribution = get_object_or_404(Contribution, id=project_id)
            donations = Donation.objects.all().filter(contribution=contribution)
            for donation in donations:
                if donation.collected:
                    collected += int(donation.amount)

            item['collected'] = collected
        return Response(serializer.data, status=status.HTTP_200_OK)


class UrgentProjectView(APIView):
    def get(self, request):
        '''
        get all urgent cases
        Required Data:
        ()
        '''
        projects = Project.objects.all().filter(Q(project_id__is_urgent=True)).distinct()
        serializer = ProjectSerializer(projects, many=True)
        for item in serializer.data:
            collected = 0
            project_id = item.get('project_id').get('id')
            project_amount = item.get('project_id').get('amount')
            contribution = get_object_or_404(Contribution, id=project_id)
            donations = Donation.objects.all().filter(contribution=contribution)
            for donation in donations:
                if donation.collected:
                    collected += int(donation.amount)

            item['collected'] = collected
        return Response(serializer.data, status=status.HTTP_200_OK)


class SponsorView(APIView):
    def get(self, request):
        '''
        get sub category
        Required Data:
        ()
        '''
        sponsors = Our_Sponsor.objects.all()
        serializer = SponsorSerializer(sponsors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MersalNumbersView(APIView):
    def get(self, request):
        '''
        mersal numbers
        Required Data:
        ()
        '''
        data = {
            'donors': Donor.objects.all().count(),
            'projects': Project.objects.all().count(),
            'donations': Donation.objects.all().count(),
        }
        return Response(data, status=status.HTTP_200_OK)


class CaseView(APIView):
    def get(self, request):
        '''
        get all cases
        Required Data:
        ()
        '''
        cases = Case.objects.all()
        serializer = CaseSerializer(cases, many=True)
        for item in serializer.data:
            collected = 0
            case_id = item.get('case_id').get('id')
            case_amount = item.get('case_id').get('amount')
            contribution = get_object_or_404(Contribution, id=case_id)
            donations = Donation.objects.all().filter(contribution=contribution)
            for donation in donations:
                if donation.collected:
                    collected += int(donation.amount)

            item['collected'] = collected
        return Response(serializer.data, status=status.HTTP_200_OK)


class UrgentCaseView(APIView):
    def get(self, request):
        '''
        get all urgent cases
        Required Data:
        ()
        '''
        cases = Case.objects.all().filter(Q(case_id__is_urgent=True)).distinct()
        serializer = CaseSerializer(cases, many=True)
        for item in serializer.data:
            collected = 0
            case_id = item.get('case_id').get('id')
            case_amount = item.get('case_id').get('amount')
            contribution = get_object_or_404(Contribution, id=case_id)
            donations = Donation.objects.all().filter(contribution=contribution)
            for donation in donations:
                if donation.collected:
                    collected += int(donation.amount)

            item['collected'] = collected
        return Response(serializer.data, status=status.HTTP_200_OK)


class CaseByCategory(APIView):
    def get(self, request, id):
        '''
        get cases by category
        Required Data:
        ()
        '''
        cases = Case.objects.all().filter(Q(sub_category__id=id))
        serializer = CaseSerializer(cases, many=True)
        for item in serializer.data:
            collected = 0
            case_id = item.get('case_id').get('id')
            case_amount = item.get('case_id').get('amount')
            contribution = get_object_or_404(Contribution, id=case_id)
            donations = Donation.objects.all().filter(contribution=contribution)
            for donation in donations:
                if donation.collected:
                    collected += int(donation.amount)

            item['collected'] = collected
        return Response(serializer.data, status=status.HTTP_200_OK)


class DonationView(APIView):
    def get(self, request):
        '''
        get all Donations
        Required Data:
        ()
        '''
        donations = Donation.objects.all()
        serializer = DonationSerializer(donations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        '''
        Add new donation
        Required Data:
        (donor, contribution, amount, address_no, charitable_activity)
        '''
        serializer = DonationSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(User, username=request.data.get('donor'))
            donor = get_object_or_404(Donor, user=user)
            contribution = get_object_or_404(Contribution, id=request.data.get('contribution'))
            charitable_activity = get_object_or_404(Sub_Category, id=request.data.get('charitable_activity'))
            donation = Donation.objects.create(
                donor=donor,
                contribution=contribution,
                amount=request.data.get('amount'),
                address_no=request.data.get('address_no'),
                charitable_activity=charitable_activity)
            serializer = DonationSerializer(donation)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DonationDetailView(APIView):
    def get(self, request, username):
        '''
        get all donations for a specific donor
        Required Data:
        ()
        '''
        donations = Donation.objects.all().filter(Q(donor__user__username=username)).distinct()
        serializer = DonationSerializer(donations, many=True)
        return Response(serializer.data)
