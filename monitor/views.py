import csv
import logging


from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from monitor.constants import STATUS_RUNNING
from monitor.models import Store, ReportStatus, Report
from monitor.utils import generate_report_id

from .tasks import trigger_report_generation_for_each_store

logger = logging.getLogger(__name__)

@api_view(['POST'])
def trigger_report(request):
    all_store_info = get_all_stores()
    report_id = generate_report_id()

    report_status = ReportStatus(report_id=report_id, status=STATUS_RUNNING)
    report_status.save()

    trigger_report_generation_for_each_store.apply_async(args=(report_id, all_store_info,))

    return Response({"report_id": report_id})

@api_view(['GET'])
def get_csv_report(request, report_id):
    try:
        report_status_info = ReportStatus.objects.get(pk=report_id)
    except ObjectDoesNotExist as e:
        return Response(data={"message": "Report not found"}, status=status.HTTP_404_NOT_FOUND)

    report_status = report_status_info.status
    if report_status == STATUS_RUNNING:
        return Response(data={"status": "RUNNING"}, status=status.HTTP_200_OK)

    try:
        reports = Report.objects.filter(report=report_status_info)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'
        response['data'] = {"status": "COMPLETED"}

        writer = csv.writer(response)
        writer.writerow(
            ['store_id', 'uptime_last_hour(%)', 'uptime_last_day(%)', 'uptime_last_week(%)', 'downtime_last_hour(%)',
             'downtime_last_day(%)', 'downtime_last_week(%)'])

        for r in reports:
            writer.writerow([r.store_id, r.uptime_last_hour, r.uptime_last_day, r.uptime_last_week, r.downtime_last_hour,
                             r.downtime_last_day, r.downtime_last_week])

        return response
    except Exception as e:
        return Response(data={"message": "Error in generating csv report"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_all_stores():
    stores = Store.objects.all().values('store_id', 'timezone_str')
    store_info = [(store['store_id'], store['timezone_str']) for store in stores]
    return store_info
