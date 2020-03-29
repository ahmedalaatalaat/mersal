from django.db import models
from django.contrib.auth.models import User
from main.utils import get_object_or_none


Address_no = [('1', '1'), ('2', '2')]


class Contribution(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.IntegerField()
    description = models.TextField()
    is_urgent = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']
        verbose_name = "Contribution"
        verbose_name_plural = "Contributions"

    def __str__(self):
        return str(self.id)

    @property
    def get_name(self):
        name = get_object_or_none(Case, case_id=self.id)
        if name:
            name = name.code
        else:
            name = get_object_or_none(Project, project_id=self.id)
        return name


class Project(models.Model):
    project_id = models.OneToOneField(Contribution, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)

    class Meta:
        ordering = ['project_id']
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return str(self.name)


class Donor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    user = models.OneToOneField(User, models.CASCADE)
    join_date = models.DateField(auto_now_add=True)
    # Address #1
    city_1 = models.CharField(max_length=12, blank=True, null=True)
    country_1 = models.CharField(max_length=12, blank=True, null=True)
    apartment_no_1 = models.CharField(max_length=6, blank=True, null=True)
    building_1 = models.CharField(max_length=6, blank=True, null=True)
    area_1 = models.CharField(max_length=30, blank=True, null=True)
    phone_1 = models.CharField(max_length=16, blank=True, null=True)
    street_1 = models.CharField(max_length=30, blank=True, null=True)
    floor_1 = models.CharField(max_length=6, blank=True, null=True)
    address_1 = models.TextField(blank=True, null=True)
    # Address #2
    city_2 = models.CharField(max_length=12, blank=True, null=True)
    country_2 = models.CharField(max_length=12, blank=True, null=True)
    apartment_no_2 = models.CharField(max_length=6, blank=True, null=True)
    building_2 = models.CharField(max_length=6, blank=True, null=True)
    area_2 = models.CharField(max_length=30, blank=True, null=True)
    phone_2 = models.CharField(max_length=16, blank=True, null=True)
    street_2 = models.CharField(max_length=30, blank=True, null=True)
    floor_2 = models.CharField(max_length=6, blank=True, null=True)
    address_2 = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['id']
        verbose_name = "Donor"
        verbose_name_plural = "Donors"

    def __str__(self):
        return str(self.name)


class Main_Category(models.Model):
    id = models.AutoField(primary_key=True)
    english_name = models.CharField(max_length=32)
    arabic_name = models.CharField(max_length=32, default="")
    image = models.ImageField(
        default='img/Categories/category.png', upload_to='img/Categories')

    class Meta:
        ordering = ['id']
        verbose_name = "Main_Category"
        verbose_name_plural = "Main_Categories"

    def __str__(self):
        return str(self.english_name)


class Sub_Category(models.Model):
    id = models.AutoField(primary_key=True)
    main_category = models.ForeignKey(
        Main_Category, on_delete=models.DO_NOTHING)
    english_name = models.CharField(max_length=32)
    arabic_name = models.CharField(max_length=32, default="")
    image = models.ImageField(
        default='img/Categories/category.png', upload_to='img/Categories')

    class Meta:
        ordering = ['id']
        verbose_name = "Sub_Category"
        verbose_name_plural = "Sub_Categories"

    def __str__(self):
        return str(self.english_name)


class Case(models.Model):
    case_id = models.OneToOneField(Contribution, on_delete=models.CASCADE)
    code = models.CharField(max_length=64, unique=True)
    sub_category = models.ForeignKey(Sub_Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']
        verbose_name = "Case"
        verbose_name_plural = "Cases"

    def __str__(self):
        return str(self.code)


class Agent(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=16)
    image = models.ImageField(
        default='img/agents/avatar.jpg', upload_to='img/agents')
    join_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['id']
        verbose_name = "Agent"
        verbose_name_plural = "Agents"

    def __str__(self):
        return str(self.user.username)


class Donation(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.SET_NULL, null=True)
    contribution = models.ForeignKey(
        Contribution, on_delete=models.SET_NULL, null=True)
    assigned_agent = models.ForeignKey(
        Agent, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.IntegerField()
    address_no = models.CharField(max_length=1, choices=Address_no)
    charitable_activity = models.ForeignKey(
        Sub_Category, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)
    collected = models.BooleanField(default=False)

    class Meta:
        ordering = ['date']
        verbose_name = "Donation"
        verbose_name_plural = "Donations"

    def __str__(self):
        try:
            return str(self.donor.name)
        except Exception:
            return str(self.id)

    @property
    def get_address(self):
        address = {
            'city_1': self.donor.city_1,
            'country_1': self.donor.country_1,
            'apartment_no_1': self.donor.apartment_no_1,
            'building_1': self.donor.building_1,
            'area_1': self.donor.area_1,
            'phone_1': self.donor.phone_1,
            'street_1': self.donor.street_1,
            'floor_1': self.donor.floor_1,
            'address_1': self.donor.address_1,
            'city_2': self.donor.city_2,
            'country_2': self.donor.country_2,
            'apartment_no_2': self.donor.apartment_no_2,
            'building_2': self.donor.building_2,
            'area_2': self.donor.area_2,
            'phone_2': self.donor.phone_2,
            'street_2': self.donor.street_2,
            'floor_2': self.donor.floor_2,
            'address_2': self.donor.address_2
        }
        return address

    @property
    def get_address_ar(self):
        address = {
            'المدينة_1': self.donor.city_1,
            'القرية_1': self.donor.country_1,
            'رقم_الشقة_1': self.donor.apartment_no_1,
            'المبني_1': self.donor.building_1,
            'المنطقة_1': self.donor.area_1,
            'المحمول_1': self.donor.phone_1,
            'الشارع_1': self.donor.street_1,
            'الطابق_1': self.donor.floor_1,
            'العنوان_1': self.donor.address_1,
            'المدينة_2': self.donor.city_2,
            'القرية_2': self.donor.country_2,
            'رقم_الشقة_2': self.donor.apartment_no_2,
            'المبني_2': self.donor.building_2,
            'المنطقة_2': self.donor.area_2,
            'المحمول_2': self.donor.phone_2,
            'الشارع_2': self.donor.street_2,
            'الطابق_2': self.donor.floor_2,
            'العنوان_2': self.donor.address_2
        }
        return address


class Slider_Image(models.Model):
    name = models.CharField(max_length=32)
    image = models.ImageField()

    class Meta:
        verbose_name = "Slider_Image"
        verbose_name_plural = "Slider_Images"

    def __str__(self):
        return str(self.name)


class Our_Sponsor(models.Model):
    name = models.CharField(max_length=32)
    image = models.ImageField()

    class Meta:
        verbose_name = "Our_Sponsor"
        verbose_name_plural = "Our_Sponsors"

    def __str__(self):
        return str(self.name)
