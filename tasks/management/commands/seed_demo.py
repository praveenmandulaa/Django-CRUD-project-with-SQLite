from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from tasks.models import Task
class Command(BaseCommand):
    help = 'Create fictional sample tasks for an existing username; no passwords are set.'
    def add_arguments(self, parser):
        parser.add_argument('username')
    def handle(self, *args, **options):
        user = get_user_model().objects.filter(username=options['username']).first()
        if user is None:
            raise CommandError('Create an account first using /signup/.')
        for title, status, priority in [('Build Django REST endpoints','progress','high'),('Review database migrations','todo','medium'),('Write ownership tests','done','high'),('Polish task dashboard','progress','medium'),('Document GitHub setup','todo','low')]:
            Task.objects.get_or_create(owner=user,title=title,defaults={'status':status,'priority':priority,'description':'Portfolio project milestone; fictional demo data.'})
        self.stdout.write(self.style.SUCCESS('Demo tasks ready.'))
