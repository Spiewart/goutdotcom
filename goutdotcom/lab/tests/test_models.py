import pytest

from ..models import Urate, ALT, AST, Platelet, WBC, Hemoglobin, Creatinine
from .factories import UrateFactory, ASTFactory, ALTFactory

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