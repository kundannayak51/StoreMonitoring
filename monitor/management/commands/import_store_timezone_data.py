import csv
from django.core.management.base import BaseCommand
from monitor.models import Store, StoreBusinessHours

class Command(BaseCommand):
    help = 'Import data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csvfile', help='./store_timezone.csv')

    def handle(self, *args, **options):
        with open(options['csvfile'], 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                store_id = int(row['store_id'])
                timezone_str = row['timezone_str']

                # Check if the store exists in the database
                store = Store(store_id=store_id, timezone_str=timezone_str)
                store.save()

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
