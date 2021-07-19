from goutdotcom.profiles.tests.factories import PatientProfileFactory
from goutdotcom.users.tests.factories import UserFactory
from goutdotcom.users.models import User
import pytest

from decimal import *

from .factories import UrateFactory, ASTFactory, ALTFactory, PlateletFactory, WBCFactory, HemoglobinFactory, CreatinineFactory

pytestmark = pytest.mark.django_db

class TestRoundDecimal:
    def test_value_return(self):
        value = Decimal(0.59403423)
        assert(value.quantize(Decimal(10) ** -2) == Decimal(0.59))

class TestLabMethods:
    def test_profile_does_not_exist(self):
        user_without_profile = UserFactory()
        Creatinine = CreatinineFactory(user=user_without_profile)
        assert(Creatinine.user.patientprofile, None)

class TestUrateMethods:
    def test__str__(self):
        Urate = UrateFactory()
        assert(Urate.__str__() == str(Urate.value))

    def test__unicode__(self):
        Urate = UrateFactory()
        assert(Urate.__unicode__() == str(Urate.name))

    def test_get_absolute_url(self):
        Urate = UrateFactory()
        assert Urate.get_absolute_url() == f"/lab/urate/{Urate.pk}/"

class TestALTMethods:
    def test__str__(self):
        ALT = ALTFactory()
        assert(ALT.__str__() == str(ALT.value))

    def test__unicode__(self):
        ALT = ALTFactory()
        assert(ALT.__unicode__() == str(ALT.name))

    def test_get_absolute_url(self):
        ALT = ALTFactory()
        assert ALT.get_absolute_url() == f"/lab/ALT/{ALT.pk}/"

class TestASTMethods:
    def test__str__(self):
        AST = ASTFactory()
        assert(AST.__str__() == str(AST.value))

    def test__unicode__(self):
        AST = ASTFactory()
        assert(AST.__unicode__() == str(AST.name))

    def test_get_absolute_url(self):
        AST = ASTFactory()
        assert AST.get_absolute_url() == f"/lab/AST/{AST.pk}/"


class TestPlateletMethods:
    def test__str__(self):
        Platelet = PlateletFactory()
        assert(Platelet.__str__() == str(Platelet.value))

    def test__unicode__(self):
        Platelet = PlateletFactory()
        assert(Platelet.__unicode__() == str(Platelet.name))

    def test_get_absolute_url(self):
        Platelet = PlateletFactory()
        assert Platelet.get_absolute_url() == f"/lab/platelet/{Platelet.pk}/"


class TestWBCMethods:
    def test__str__(self):
        WBC = WBCFactory()
        assert(WBC.__str__() == str(WBC.value))

    def test__unicode__(self):
        WBC = WBCFactory()
        assert(WBC.__unicode__() == str(WBC.name))

    def test_get_absolute_url(self):
        WBC = WBCFactory()
        assert WBC.get_absolute_url() == f"/lab/WBC/{WBC.pk}/"


class TestHemoglobinMethods:
    def test__str__(self):
        Hemoglobin = HemoglobinFactory()
        assert(Hemoglobin.__str__() == str(Hemoglobin.value))

    def test__unicode__(self):
        Hemoglobin = HemoglobinFactory()
        assert(Hemoglobin.__unicode__() == str(Hemoglobin.name))

    def test_get_absolute_url(self):
        Hemoglobin = HemoglobinFactory()
        assert Hemoglobin.get_absolute_url() == f"/lab/hemoglobin/{Hemoglobin.pk}/"


class TestCreatinineMethods:
    def test__str__(self):
        Creatinine = CreatinineFactory()
        assert(Creatinine.__str__() == str(Creatinine.value))

    def test__unicode__(self):
        Creatinine = CreatinineFactory()
        assert(Creatinine.__unicode__() == str(Creatinine.name))

    def test_get_absolute_url(self):
        Creatinine = CreatinineFactory()
        assert Creatinine.get_absolute_url() == f"/lab/creatinine/{Creatinine.pk}/"

    def test_sex_vars_kappa(self):
        profile = PatientProfileFactory()
        Creatinine = CreatinineFactory()
        Creatinine.user.patientprofile = profile

        if profile.gender == 'male':
            assert Creatinine.eGFR_calculator().sex_vars_kappa() == Decimal(0.9)
        elif profile.gender == 'female':
            assert Creatinine.eGFR_calculator().sex_vars_kappa() == Decimal(0.7)
        else: 
            assert Creatinine.eGFR_calculator().sex_vars_kappa() == False