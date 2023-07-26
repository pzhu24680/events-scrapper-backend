from django.core.management.base import BaseCommand
from gather_data import gather_data

class Command(BaseCommand):
    help = 'Scrape website data and store in the database'

    def handle(self, *args, **kwargs):
        gather_data()
        self.stdout.write(self.style.SUCCESS('Data scraping completed successfully.'))