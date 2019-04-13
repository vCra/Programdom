from factory import Factory, Sequence, DjangoModelFactory
from programdom.models import User


class AuthUserFactory(DjangoModelFactory):

    class Meta:
        model = User

    username = Sequence(lambda n: f"user{n}")
    email = Sequence(lambda n: f"user{0}@example.com")

    @classmethod
    def _prepare(cls, new, **kwargs):
        password = 'password'
        user = super(AuthUserFactory, cls)._prepare(new, **kwargs)

        user.set_password(password)

        if new:
            user.save()

        return user
