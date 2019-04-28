from factory import Factory, Sequence

from programdom.models import Workshop


class EmptyWorkshopFactory(Factory):
    class Meta:
        model = Workshop

    title = Sequence(lambda n: f"Workshop {n}")
