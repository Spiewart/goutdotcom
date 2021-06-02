import factory

from .factories import AllopurinolFactory, FebuxostatFactory, ColchicineFactory, IbuprofenFactory, NaproxenFactory, MeloxicamFactory, CelecoxibFactory, PrednisoneFactory, MethylprednisoloneFactory, ProbenecidFactory

from goutdotcom.users.models import User

class ColchicineSpiewFactory(ColchicineFactory):
    user = User.objects.get(username="spiew")

class ColchicineUserFactory(ColchicineFactory):
    user = factory.Iterator(User.objects.all())

class IbuprofenSpiewFactory(IbuprofenFactory):
    user = User.objects.get(username="spiew")

class IbuprofenUserFactory(IbuprofenFactory):
    user = factory.Iterator(User.objects.all())

class NaproxenSpiewFactory(NaproxenFactory):
    user = User.objects.get(username="spiew")

class NaproxenUserFactory(NaproxenFactory):
    user = factory.Iterator(User.objects.all())

class MeloxicamSpiewFactory(MeloxicamFactory):
    user = User.objects.get(username="spiew")

class MeloxicamUserFactory(MeloxicamFactory):
    user = factory.Iterator(User.objects.all())

class CelecoxibSpiewFactory(CelecoxibFactory):
    user = User.objects.get(username="spiew")

class CelecoxibUserFactory(CelecoxibFactory):
    user = factory.Iterator(User.objects.all())

class PrednisoneSpiewFactory(PrednisoneFactory):
    user = User.objects.get(username="spiew")

class PrednisoneUserFactory(PrednisoneFactory):
    user = factory.Iterator(User.objects.all())

class MethylprednisoloneSpiewFactory(MethylprednisoloneFactory):
    user = User.objects.get(username="spiew")

class MethylprednisoloneUserFactory(MethylprednisoloneFactory):
    user = factory.Iterator(User.objects.all())