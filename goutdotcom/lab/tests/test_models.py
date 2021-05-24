import pytest

from .factories import UrateFactory, ASTFactory, ALTFactory, PlateletFactory, WBCFactory, HemoglobinFactory, CreatinineFactory

pytestmark = pytest.mark.django_db

class TestUrateMethods:
    def test__str__(self):
        urate = UrateFactory()
        assert(urate.__str__() == str(urate.uric_acid))

    def test__unicode__(self):
        urate = UrateFactory()
        assert(urate.__unicode__() == str(urate.name))

    def test_get_absolute_url(self):
        urate = UrateFactory()
        assert urate.get_absolute_url() == f"/lab/urate/{urate.pk}/"

class TestALTMethods:
    def test__str__(self):
        ALT = ALTFactory()
        assert(ALT.__str__() == str(ALT.alt_sgpt))

    def test__unicode__(self):
        ALT = ALTFactory()
        assert(ALT.__unicode__() == str(ALT.name))

    def test_get_absolute_url(self):
        ALT = ALTFactory()
        assert ALT.get_absolute_url() == f"/lab/ALT/{ALT.pk}/"

class TestASTMethods:
    def test__str__(self):
        AST = ASTFactory()
        assert(AST.__str__() == str(AST.ast_sgot))

    def test__unicode__(self):
        AST = ASTFactory()
        assert(AST.__unicode__() == str(AST.name))

    def test_get_absolute_url(self):
        AST = ASTFactory()
        assert AST.get_absolute_url() == f"/lab/AST/{AST.pk}/"


class TestPlateletMethods:
    def test__str__(self):
        Platelet = PlateletFactory()
        assert(Platelet.__str__() == str(Platelet.platelets))

    def test__unicode__(self):
        Platelet = PlateletFactory()
        assert(Platelet.__unicode__() == str(Platelet.name))

    def test_get_absolute_url(self):
        Platelet = PlateletFactory()
        assert Platelet.get_absolute_url() == f"/lab/platelet/{Platelet.pk}/"


class TestWBCMethods:
    def test__str__(self):
        WBC = WBCFactory()
        assert(WBC.__str__() == str(WBC.white_blood_cells))

    def test__unicode__(self):
        WBC = WBCFactory()
        assert(WBC.__unicode__() == str(WBC.name))

    def test_get_absolute_url(self):
        WBC = WBCFactory()
        assert WBC.get_absolute_url() == f"/lab/WBC/{WBC.pk}/"


class TestHemoglobinMethods:
    def test__str__(self):
        Hemoglobin = HemoglobinFactory()
        assert(Hemoglobin.__str__() == str(Hemoglobin.hemoglobin))

    def test__unicode__(self):
        Hemoglobin = HemoglobinFactory()
        assert(Hemoglobin.__unicode__() == str(Hemoglobin.name))

    def test_get_absolute_url(self):
        Hemoglobin = HemoglobinFactory()
        assert Hemoglobin.get_absolute_url() == f"/lab/hemoglobin/{Hemoglobin.pk}/"
