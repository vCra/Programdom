from factory import Sequence, DjangoModelFactory, PostGenerationMethodCall
from programdom.models import User


class AuthUserFactory(DjangoModelFactory):

    class Meta:
        model = User

    username = Sequence(lambda n: f"user{n}")
    email = Sequence(lambda n: f"user{0}@example.com")
    password = PostGenerationMethodCall('set_password', 'password')
