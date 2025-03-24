import factory
from Gestor.models import Group, User
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

# administradores_group = GroupFactory(desc_group="administradores")
# administrador_user=UserFactory(name='admin', email='admin@admin.com', password=make_password('1234'), real_name='Administrador', group=administradores_group)