from django.contrib import admin
from .models import Job, JobHistory

# Custom ModelAdmin class for the Job model
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'first_added', 'last_updated', 'update_count', 'unavailable_date', 'job_active')
    list_filter = ('job_active', 'first_added', 'last_updated')  # Filters for status and dates
    search_fields = ('job_id', 'title')  # Allow searching by JobID and title
    readonly_fields = ('first_added', 'last_updated')  # Make these fields read-only in the admin form

# Custom ModelAdmin class for the JobHistory model
class JobHistoryAdmin(admin.ModelAdmin):
    list_display = ('job', 'version_timestamp', 'update_reason')  # Fields to display in list view
    search_fields = ('job__job_id', 'update_reason')  # Allow searching by JobID and update reason
    readonly_fields = ('version_timestamp',)  # Timestamp is read-only

# Register the Job model with its custom ModelAdmin
admin.site.register(Job, JobAdmin)

# Register the JobHistory model with its custom ModelAdmin
admin.site.register(JobHistory, JobHistoryAdmin)
admin.site.site_header = "Euro Jobs Administration"
admin.site.site_title = "Euro Jobs Admin Portal"
admin.site.index_title = "Welcome to the Euro Jobs Admin"
