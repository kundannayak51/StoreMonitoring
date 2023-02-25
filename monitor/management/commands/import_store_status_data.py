import csv

from django.core.management.base import BaseCommand

from monitor.constants import DEFAULT_TIMEZONE
from monitor.models import Store, StoreBusinessHours, StoreStatus
from dateutil.parser import parse


class Command(BaseCommand):
    help = 'Import data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csvfile', help='./store_status.csv')

    def handle(self, *args, **options):
        with open(options['csvfile'], 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                store_id = int(row['store_id'])
                status = row['status']
                timestamp_utc = row['timestamp_utc']
                timestamp_dt = parse(timestamp_utc)

                store, created = Store.objects.get_or_create(store_id=store_id,
                                                             defaults={'timezone_str': DEFAULT_TIMEZONE})

                store_status = StoreStatus(store=store,status=status,timestamp_utc=timestamp_dt)
                store_status.save()

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
