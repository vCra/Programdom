from factory import Sequence, DjangoModelFactory

from programdom.models import Workshop


class EmptyWorkshopFactory(DjangoModelFactory):
    class Meta:
        model = Workshop

    title = Sequence(lambda n: f"Workshop {n}")
