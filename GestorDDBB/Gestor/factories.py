import factory
from Gestor.models import Group, User, Permission, Value, Enumerate
from django.contrib.auth.hashers import make_password

class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    desc_group = factory.Faker('word')

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    name = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.LazyAttribute(lambda obj: make_password('default_password'))
    real_name = factory.Faker('name')
    group = factory.SubFactory(GroupFactory)

class PermissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Permission
    name=factory.Faker('user_name')

class EnumerateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Enumerate
    name=factory.Faker('word')

class ValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Value
    placeholder=factory.Faker('word')
    value=factory.Faker('word')
    order = factory.Faker('random_int', min=1, max=1000)