# StoreMonitoring

### Project Details

|                          |                  |
|--------------------------|------------------|
| **Service name**         | store_monitoring |
| **Language / Framework** | Python/Django    |
| **Database**             | postgreSQL       | 

### CurrentTime
Currently the project has hard-coded currentTime = "2023-01-25 18:13:22.47922 UTC" which max of time present in store_status db. You can edit it in utils.py file.

### Requirements
Activate your virtual environment and run: pip install -r requirements.txt

### Database setup in local
1. create a database `store_monitoring` in pgAdmin:

2. We want 5 tables `store_business_hour`, `store_status`, `timezones`, `report_status`, and `report`

3. Run migration commands:


    python manage.py makemigrations
    python manage.py migrate




4. Importing csv data to tables: put your csv files in monitor/management/commands directory and run:


    python manage.py import_store_timezone_data monitor/management/commands/store_timezone.csv
    python manage.py import_store_status_data monitor/management/commands/store_status.csv
    python manage.py import_store_business_hours_data monitor/management/commands/business_hours.csv

If a store_id found in business_hours.csv file which is not there is Store, it will create an entry with default timezone.


5. Change the `USER`, `PASSWORD`, and `NAME` accordingly in `settings.py` 

### API cURLS

    curl --location --request POST 'http://localhost:8000/api/monitor/trigger_report' \
    --header 'Content-Type: application/json'

    {
    "report_id": "6GwrNmgx"
    }


    curl --location 'http://localhost:8000/api/monitor/get_report/NjXtUGWP' \
    --header 'Content-Type: application/json'


### Run
I have used `Celery` to run asynchronous tasks in a background process. Before running the project make sure redis is running on configured port, I am using port 6380, you can change the port in setting.py CELERY configuration. And then start celery worker.

    redis-server --port 6380
    celery -A store_monitoring worker -l info

If you face an error ecause the environment in which Celery is running is configured to use ASCII as the encoding. You need to set the environment variable LC_ALL to a UTF-8 encoding
    

    export LC_ALL=en_US.UTF-8



### Explanation:
1. The first api trigger_report is a POST endpoint that triggers the generation of a report. It generates a unique report ID and creates an entry in the ReportStatus model with the status set to Running. It then triggers an asynchronous task `trigger_report_generation_for_each_store` passing the report_id and a list of all stores. And, it returns a JSON response containing the report_id.

2. `trigger_report_generation_for_each_store(report_id, stores_info)`: this method calls `generate_and_store_report_for_store(report_id, store_id, timezone_str)` for each store_id and once the report is generated for all the store_id, it updates the status of report_id in `ReportStatus` with {report_id, "Completed"}.

3. `generate_and_store_report_for_store(report_id, store_id, timezone_str)`: since we have to generate report for last week for each store_id, we are fetching the business_hours of store_id for each each in last week, if data for any day is missing, enrich the data with start_time `00:00:00` and end_time `23:59:59`. Now fetch all the status of this store_id within a week and call `calculate_weekly_observation_and_generate_report(report_id, store_id, store_statuses, business_hours, timezone, day_time_mapping)` to generate the report for this store_id and insert the record in `Report` .

4. `calculate_weekly_observation_and_generate_report(report_id, store_id, store_statuses, business_hours, timezone, day_time_mapping)`: I have divided business hours for each into chunks of `60 mins` and initialized each chunk with value `None`. Then iterate over list of status of the store_id and if the time of this status lies in between the business hour of that day, update the chunk in which this lies with the status `inactive` or `active` value. Interpolate the remaining `None` value chunks with `enrich_status_map_with_nearest_status(status_map)` method, generate the weekly report with `create_weekly_observation(store_id, status_map, day)` and return the report.

5. `enrich_status_map_with_nearest_status(status_map)`: For each business hour we need to replace `None` status with `active` or `inactive` status. If the day has zero `active` or `inactive` status, I have simply updated the status of each business hour by geerating a random value between 0 to 1, if its >= 0.5, status is `active` else `inactive`. For those days which has some `active` and `inactive` status, then if the status of a chunk is `None` replace it with nearest `active` or `inactive`chunk status. For the starting reference point again I have taken random value generation approach.

6. `create_weekly_observation(store_id, status_map, day)`: now we have `active` or `inactive` status for every chunk of each day, simply used (no. of active chunks / no. of total chunks)*100 to generate uptime percentage of last hour, last day and last week.



7. The second api get_report is a GET endpoint that returns a CSV file containing the report data for a given report_id. It first tries to get the `ReportStatus` object associated with the given report_id. If the object is not found, it returns a 404 response. If the status of the report is Running, it returns a JSON response containing the status. Otherwise, it queries the Report model to get all the reports associated with the given report_id and generates a CSV file containing the report data. If any error occurs, it returns a 500 response.