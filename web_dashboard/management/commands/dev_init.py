from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User
from web_dashboard.models import OrgAccount, UserAccount


class Command(BaseCommand):
    help = 'Initializes the database with some data'

    def handle(self, *args, **options):
        # Create the admin user
        if not User.objects.filter(username='dummy').exists():
            User.objects.create_user('dummy', '', 'dummy')

        # create OrgAccount
        if not OrgAccount.objects.filter(name='test').exists():
            OrgAccount.objects.create(name='test',type='dev',billing_plan='free',is_demo=True)

        # create UserAccount
        if not UserAccount.objects.filter(user__username='dummy').exists():
            user = User.objects.get(username='dummy')
            org = OrgAccount.objects.get(name='test')
            UserAccount.objects.create(user=user,org=org)

        self.stdout.write(self.style.SUCCESS('Successfully initialized database'))
