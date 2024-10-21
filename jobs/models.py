# models.py

from django.db import models

class Job(models.Model):
    job_id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    number_of_posts = models.IntegerField(default=1)
    location = models.JSONField(null=True, blank=True)  # Stores locationMap
    eures_flag = models.BooleanField(default=False)  # Captures the euresFlag field
    job_categories_codes = models.JSONField(null=True, blank=True)  # Stores job categories
    position_schedule_codes = models.JSONField(null=True, blank=True)  # Stores schedule codes
    employer = models.JSONField(null=True, blank=True)  # Allow NULL and blank values
    available_languages = models.JSONField(null=True, blank=True)  # Stores available languages
    score = models.FloatField(null=True, blank=True)  # Stores score if available
    json_data = models.JSONField()  # Full job JSON data
    first_added = models.DateTimeField(auto_now_add=True)  # First time added
    last_updated = models.DateTimeField(auto_now=True)  # Last updated time
    update_count = models.IntegerField(default=0)  # Number of updates
    unavailable_date = models.DateTimeField(null=True, blank=True)  # Date when job became unavailable
    job_active = models.BooleanField(default=True)  # Is the job active or not

    def __str__(self):
        return f'{self.title} : {self.job_id}'

class JobHistory(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    json_data = models.JSONField()  # Store old version of job JSON
    version_timestamp = models.DateTimeField(auto_now_add=True)
    update_reason = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.job.title} : {self.job.job_id}'
