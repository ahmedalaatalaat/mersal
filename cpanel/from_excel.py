import pandas as pd
from .models import Case, Sub_Category, Contribution


def import_cases(file):
    try:
        df = pd.read_excel(file)
        for i in range(len(df)):
            try:
                contribution = Contribution.objects.create(
                    amount=df['التكلفة المطلوبة'][i],
                    description=df['الملخص'][i])

                sub_category = Sub_Category.objects.get(arabic_name=df['الخدمة'][i])

                Case.objects.create(
                    case_id=contribution,
                    code=df['الكود'][i],
                    sub_category=sub_category
                )
            except Exception:
                contribution.delete()
    except Exception:
        pass


def import_projects():
    pass


def import_Donors():
    pass


def import_Main_Categories():
    pass


def import_Sub_Categories():
    pass


def import_Agents():
    pass


def import_Donations():
    pass
