from goutdotcom.profiles.models import PatientProfile
from goutdotcom.profiles.tests.factories import FamilyProfileFactory, PatientProfileFactory, SocialProfileFactory
from goutdotcom.users.tests.factories import UserFactory
from goutdotcom.lab.models import round_decimal
import pytest

from decimal import *

from .factories import UrateFactory, ASTFactory, ALTFactory, PlateletFactory, WBCFactory, HemoglobinFactory, CreatinineFactory

pytestmark = pytest.mark.django_db

class TestRoundDecimal:
    def test_value_return(self):
        value = Decimal(0.59343)
        assert(value.quantize(Decimal(10) ** -2) == Decimal('0.59'))

class TestUrateMethods:
    def test__str__(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        urate = UrateFactory(user=user)
        assert(urate.__str__() == str(urate.value))

    def test__unicode__(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        urate = UrateFactory(user=user)
        assert(urate.__unicode__() == str(urate.name))

    def test_get_absolute_url(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        urate = UrateFactory(user=user)
        assert urate.get_absolute_url() == f"/lab/urate/{urate.pk}/"

class TestALTMethods:
    def test__str__(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        ALT = ALTFactory(user=user)
        assert(ALT.__str__() == str(ALT.value))

    def test__unicode__(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        ALT = ALTFactory(user=user)
        assert(ALT.__unicode__() == str(ALT.name))

    def test_get_absolute_url(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        ALT = ALTFactory(user=user)
        assert ALT.get_absolute_url() == f"/lab/ALT/{ALT.pk}/"

class TestASTMethods:
    def test__str__(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        AST = ASTFactory(user=user)
        assert(AST.__str__() == str(AST.value))

    def test__unicode__(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        AST = ASTFactory(user=user)
        assert(AST.__unicode__() == str(AST.name))

    def test_get_absolute_url(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        AST = ASTFactory(user=user)
        assert AST.get_absolute_url() == f"/lab/AST/{AST.pk}/"


class TestPlateletMethods:
    def test__str__(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        platelet = PlateletFactory(user=user)
        assert(platelet.__str__() == str(platelet.value))

    def test__unicode__(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        platelet = PlateletFactory(user=user)
        assert(platelet.__unicode__() == str(platelet.name))

    def test_get_absolute_url(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        platelet = PlateletFactory(user=user)
        assert platelet.get_absolute_url() == f"/lab/platelet/{platelet.pk}/"


class TestWBCMethods:
    def test__str__(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        WBC = WBCFactory(user=user)
        assert(WBC.__str__() == str(WBC.value))

    def test__unicode__(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        WBC = WBCFactory(user=user)
        assert(WBC.__unicode__() == str(WBC.name))

    def test_get_absolute_url(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        WBC = WBCFactory(user=user)
        assert WBC.get_absolute_url() == f"/lab/WBC/{WBC.pk}/"


class TestHemoglobinMethods:
    def test__str__(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        hemoglobin = HemoglobinFactory(user=user)
        assert(hemoglobin.__str__() == str(hemoglobin.value))

    def test__unicode__(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        hemoglobin = HemoglobinFactory(user=user)
        assert(hemoglobin.__unicode__() == str(hemoglobin.name))

    def test_get_absolute_url(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        hemoglobin = HemoglobinFactory(user=user)
        assert hemoglobin.get_absolute_url() == f"/lab/hemoglobin/{hemoglobin.pk}/"


class TestCreatinineMethods:
    def test__str__(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        creatinine = CreatinineFactory(user=user)
        assert(creatinine.__str__() == str(creatinine.value))

    def test__unicode__(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        creatinine = CreatinineFactory(user=user)
        assert(creatinine.__unicode__() == str(creatinine.name))

    def test_get_absolute_url(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        creatinine = CreatinineFactory(user=user)
        assert creatinine.get_absolute_url() == f"/lab/creatinine/{creatinine.pk}/"

    def test_sex_vars_kappa(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        creatinine = CreatinineFactory(user=user)

        if profile.gender == 'male':
            assert creatinine.sex_vars_kappa() == Decimal(0.9)
        elif profile.gender == 'female':
            assert creatinine.sex_vars_kappa() == Decimal(0.7)
        else:
            assert creatinine.eGFR_calculator().sex_vars_kappa() == False

    def test_sex_vars_alpha(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        creatinine = CreatinineFactory(user=user)

        if profile.gender == 'male':
            assert creatinine.sex_vars_alpha() == Decimal(-0.411)
        elif profile.gender == 'female':
            assert creatinine.sex_vars_alpha() == Decimal(-0.329)
        else:
            assert creatinine.eGFR_calculator().sex_vars_kappa() == False

    def test_race_modifier(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        creatinine = CreatinineFactory(user=user)

        if profile.race == 'black':
            assert creatinine.race_modifier() == Decimal(1.159)
        elif profile.race == 'white' or profile.race == 'asian' or profile.race == 'native american' or profile.race == 'hispanic':
            assert creatinine.race_modifier() == Decimal(1.00)
        else:
            assert creatinine.eGFR_calculator() == False

    def test_sex_modifier(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        creatinine = CreatinineFactory(user=user)

        if profile.gender == 'male':
            assert creatinine.sex_modifier() == Decimal(1.018)
        elif profile.gender == 'female' or profile.gender == 'non-binary':
            assert creatinine.sex_modifier() == Decimal(1.00)
        else:
            assert creatinine.eGFR_calculator() == False

    def test_eGFR_calculator(self):
        user = UserFactory()
        profile = PatientProfileFactory(user=user)
        familyprofile = FamilyProfileFactory(user=user)
        socialprofile = SocialProfileFactory(user=user)
        creatinine = CreatinineFactory(user=user)
        ##assert Creatinine.eGFR_calculator() == "Can't calculate eGFR without an age (make a profile)"
        kappa = 0
        alpha = 0
        race = 0
        sex = 0
        age = profile.get_age()

        if profile.gender == 'male':
            sex = Decimal(1.018)
            kappa = Decimal(0.9)
            alpha = Decimal(-0.411)
        elif profile.gender == 'female':
            sex = Decimal(1.00)
            kappa = Decimal(0.7)
            alpha = Decimal(-0.329)
        else:
            return "Something went wrong with eGFR calculation"
        if profile.race == 'black':
            race = Decimal(1.159)
        elif profile.race == 'white' or profile.race == 'asian' or profile.race == 'native american' or profile.race == 'hispanic':
            race = Decimal(1.00)
        else:
            return "Something went wrong with eGFR calculation"
        eGFR = Decimal(141) * min(creatinine.value / kappa, Decimal(1.00)) ** alpha * max(creatinine.value / kappa, Decimal(1.00)
                                                                                          ) ** Decimal(-1.209) * Decimal(0.993) ** age * race * sex
        assert creatinine.eGFR_calculator() == round_decimal(eGFR, 2)
