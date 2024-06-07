from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker

User = get_user_model()

class Command(BaseCommand):
    help = 'Create 100 test users'

    def handle(self, *args, **kwargs):
        faker = Faker()
        self.stdout.write(self.style.NOTICE(f'creating 100 Users'))
        for _ in range(100):

            email = faker.email()
            try:
                name = email.split('@')[0]
            except IndexError:
                name = faker.name()
            password = faker.password() 
            self.stdout.write(self.style.NOTICE(f'creating User(name={name}, email={email}, password={password})'))
            try:
                user = User(email=email, name=name)
                user.set_password(password)
                user.save()
            except:
                pass

        self.stdout.write(self.style.SUCCESS('Successfully created 100 test users'))

