# Generated by Django 3.2.18 on 2023-02-22 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReportStatus',
            fields=[
                ('report_id', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=16)),
            ],
            options={
                'db_table': 'report_status',
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('store_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('timezone_str', models.TextField()),
            ],
            options={
                'db_table': 'timezones',
            },
        ),
        migrations.CreateModel(
            name='StoreStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp_utc', models.DateTimeField()),
                ('status', models.TextField()),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.store')),
            ],
            options={
                'db_table': 'store_status',
            },
        ),
        migrations.CreateModel(
            name='StoreBusinessHours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.IntegerField()),
                ('start_time_local', models.TextField()),
                ('end_time_local', models.TextField()),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.store')),
            ],
            options={
                'db_table': 'store_business_hours',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uptime_last_hour', models.FloatField()),
                ('uptime_last_day', models.FloatField()),
                ('uptime_last_week', models.FloatField()),
                ('downtime_last_hour', models.FloatField()),
                ('downtime_last_day', models.FloatField()),
                ('downtime_last_week', models.FloatField()),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.reportstatus')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.store')),
            ],
            options={
                'db_table': 'report',
                'unique_together': {('report', 'store')},
            },
        ),
    ]
