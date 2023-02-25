import csv
from django.core.management.base import BaseCommand

from monitor.constants import DEFAULT_TIMEZONE
from monitor.models import Store, StoreBusinessHours

class Command(BaseCommand):
    help = 'Import data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csvfile', help='./business_hours.csv')

    def handle(self, *args, **options):
        with open(options['csvfile'], 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                store_id = int(row['store_id'])
                day_of_week = int(row['day'])
                start_time_local = row['start_time_local']
                end_time_local = row['end_time_local']

                store, created = Store.objects.get_or_create(store_id=store_id, defaults={'timezone_str': DEFAULT_TIMEZONE})

                business_hours = StoreBusinessHours(store=store, day_of_week=day_of_week, start_time_local=start_time_local, end_time_local=end_time_local)
                business_hours.save()

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
