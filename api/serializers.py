from rest_framework import serializers
from django.contrib.auth.models import User
from cpanel.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = ['id', 'name', 'city_1', 'country_1', 'apartment_no_1', 'building_1', 'area_1', 'phone_1', 'street_1', 'floor_1', 'address_1', 'city_2', 'country_2', 'apartment_no_2', 'building_2', 'area_2', 'phone_2', 'street_2', 'floor_2', 'address_2']


class ResgistrationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=20, min_length=8)
    city = serializers.CharField(max_length=20)
    country = serializers.CharField(max_length=20)


class SliderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider_Image
        fields = ['id', 'name', 'image']


class MainCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Main_Category
        fields = ['id', 'english_name', 'arabic_name', 'image']


class SubCategorySerializer(serializers.ModelSerializer):
    main_category = MainCategorySerializer(read_only=True)

    class Meta:
        model = Sub_Category
        fields = ['id', 'english_name', 'arabic_name', 'main_category', 'image']


class ContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contribution
        fields = ['id', 'amount', 'description', 'is_urgent']


class ProjectSerializer(serializers.ModelSerializer):
    project_id = ContributionSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ['project_id', 'name']


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Our_Sponsor
        fields = ['id', 'name', 'image']


class CaseSerializer(serializers.ModelSerializer):
    case_id = ContributionSerializer(read_only=True)
    sub_category = SubCategorySerializer(read_only=True)

    class Meta:
        model = Case
        fields = ['case_id', 'code', 'sub_category']


class AgentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Agent
        fields = ['id', 'user', 'phone', 'image', 'join_date']


class DonationSerializer(serializers.ModelSerializer):
    donor = DonorSerializer(read_only=True)
    contribution = ContributionSerializer(read_only=True)
    assigned_agent = AgentSerializer(read_only=True)
    charitable_activity = SubCategorySerializer(read_only=True)

    class Meta:
        model = Donation
        fields = ['id', 'donor', 'contribution', 'assigned_agent', 'amount', 'address_no', 'charitable_activity', 'date', 'collected']
