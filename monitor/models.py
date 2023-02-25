from django.db import models

class Store(models.Model):
    store_id = models.BigIntegerField(primary_key=True)
    timezone_str = models.TextField()

    class Meta:
        db_table = 'timezones'

class StoreBusinessHours(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    day_of_week = models.IntegerField()
    start_time_local = models.TextField()
    end_time_local = models.TextField()

    class Meta:
        db_table = 'store_business_hours'

class StoreStatus(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    timestamp_utc = models.DateTimeField()
    status = models.TextField()

    class Meta:
        db_table = 'store_status'

class ReportStatus(models.Model):
    report_id = models.CharField(max_length=32, primary_key=True)
    status = models.CharField(max_length=16)

    class Meta:
        db_table = 'report_status'
class Report(models.Model):
    report = models.ForeignKey(ReportStatus, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    uptime_last_hour = models.FloatField()
    uptime_last_day = models.FloatField()
    uptime_last_week = models.FloatField()
    downtime_last_hour = models.FloatField()
    downtime_last_day = models.FloatField()
    downtime_last_week = models.FloatField()

    class Meta:
        db_table = 'report'
        unique_together = ('report', 'store')