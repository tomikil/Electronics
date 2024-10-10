from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        user = create(email='admin@admin.ru',
                                   is_staff=True,
                                   is_superuser=True,
                                   is_active=True
                                   )

        user.set_password('admin')
        user.save()
