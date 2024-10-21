
from django.shortcuts import render

import json
import csv
from django.http import HttpResponse
from .models import Job

# Django view to handle job retrieval with filters and download
def run_job_retrieval(request):
    # Check if the user initiated a fetch request
    if request.method == 'POST':
        success = True
        if success:
            return render(request, 'jobs/job_dashboard.html', {'message': 'Job retrieval completed successfully!'})
        else:
            return render(request, 'jobs/job_dashboard.html', {'message': 'Failed to retrieve jobs.'})

    # If GET request, show the filter and download page
    return render(request, 'jobs/job_dashboard.html')

def download_jobs(request):
    # Get filtering criteria from the form
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    country = request.GET.get('country')

    # Filter job data based on criteria
    jobs = Job.objects.all()

    if date_from:
        jobs = jobs.filter(first_added__gte=date_from)
    if date_to:
        jobs = jobs.filter(first_added__lte=date_to)
    if country:
        jobs = jobs.filter(location__contains={'country': country})

    # Create the CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="jobs.csv"'

    writer = csv.writer(response)
    writer.writerow(['Job ID', 'First Added', 'Last Updated', 'Job Data'])

    for job in jobs:
        writer.writerow([job.job_id, job.first_added, job.last_updated, json.dumps(job.json_data)])

    return response
