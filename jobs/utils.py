import json
import time

from .models import Job, JobHistory
from datetime import datetime
import requests

import logging
import traceback

# Set up logging for the scraping process
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_jobs_from_eures():
    url = "https://europa.eu/eures/eures-apps/searchengine/page/jv-search/search"
    session_id = "0pr1pteikkifp4yls1p95b"
    results_per_page = 50

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Cookie': 'EURES_JVSE_SESSIONID=28639435133425341A3541D7CDA08C0A; XSRF-TOKEN=551c7ef7-be80-44a5-a0e4-834e95869af3;',
        'Origin': 'https://europa.eu',
        'Referer': 'https://europa.eu/eures/portal/jv-se/search?page=1&resultsPerPage=10&orderBy=BEST_MATCH&lang=en',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'X-XSRF-TOKEN': '551c7ef7-be80-44a5-a0e4-834e95869af3',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }

    while True:
        try:
            # Loop for continuous execution
            page = 1
            total_jobs = 0

            # Fetch all currently active jobs from the database
            active_jobs = Job.objects.filter(job_active=True)
            active_job_ids = set(active_jobs.values_list('job_id', flat=True))  # Get job IDs of active jobs

            fetched_job_ids = set()  # To store job IDs fetched from the API

            while True:
                # Prepare payload for the current page request
                payload = json.dumps({
                    "resultsPerPage": results_per_page,
                    "page": page,
                    "sortSearch": "BEST_MATCH",
                    "keywords": [],
                    "publicationPeriod": None,
                    "occupationUris": [],
                    "skillUris": [],
                    "requiredExperienceCodes": [],
                    "positionScheduleCodes": [],
                    "sectorCodes": [],
                    "educationLevelCodes": [],
                    "positionOfferingCodes": [],
                    "locationCodes": [],
                    "euresFlagCodes": [],
                    "otherBenefitsCodes": [],
                    "requiredLanguages": [],
                    "minNumberPost": None,
                    "sessionId": "0pr1pteikkifp4yls1p95b"
                })

                # Send the request
                response = requests.post(url, headers=headers, data=payload)
                response.raise_for_status()  # Check if the request was successful
                data = response.json()

                # On the first request, determine the total number of jobs
                if total_jobs == 0:
                    total_jobs = data.get('numberRecords', 0)
                    if total_jobs == 0:
                        logging.info("No jobs found.")
                        break
                    logging.info(f"Total number of jobs to fetch: {total_jobs}")

                # Save the job data in the database and track fetched job IDs
                for job in data['jvs']:
                    fetched_job_ids.add(job['id'])  # Track this job ID

                    job_obj, created = Job.objects.update_or_create(
                        job_id=job['id'],
                        defaults={
                            'json_data': job,  # Store all JSON fields
                            'last_updated': datetime.fromtimestamp(job['lastModificationDate'] / 1000.0),
                            'job_active': True,
                            'title': job['title'],
                            'description': job['description'],
                            'number_of_posts': job['numberOfPosts'],
                            'location': job['locationMap'],
                            'eures_flag': job['euresFlag'],
                            'job_categories_codes': job['jobCategoriesCodes'],
                            'position_schedule_codes': job['positionScheduleCodes'],
                            'employer': job.get('employer', {}),  # Handle missing employer data
                            'available_languages': job['availableLanguages'],
                            'score': job['score'],
                        }
                    )

                    # If the job was updated, save the update in the JobHistory model
                    if not created:
                        JobHistory.objects.create(
                            job=job_obj,
                            json_data=job,
                            version_timestamp=datetime.now(),
                            update_reason='Updated job'
                        )

                logging.info(f"Fetched page {page} with {len(data['jvs'])} jobs.")

                # Check if all jobs have been fetched
                if page * results_per_page >= total_jobs:
                    logging.info(f"All jobs fetched. Total jobs retrieved: {page * results_per_page}")
                    break

                # Increment the page and sleep for 5 seconds to avoid detection
                page += 1
                time.sleep(5)

            # Mark jobs as inactive if their job IDs were not fetched in the current API call
            jobs_to_mark_inactive = active_job_ids - fetched_job_ids  # Set difference
            Job.objects.filter(job_id__in=jobs_to_mark_inactive).update(job_active=False, unavailable_date=datetime.now())

            logging.info(f"Marked {len(jobs_to_mark_inactive)} jobs as inactive.")

        except requests.RequestException as e:
            logging.error(f"Error fetching jobs from EURES: {str(e)}")
            logging.error(traceback.format_exc())  # Log the full traceback for debugging
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            logging.error(traceback.format_exc())  # Log unexpected errors

        # Sleep for a certain interval before starting the next cycle (e.g., 10 minutes)
        logging.info("Sleeping for 10 minutes before retrying...")
        time.sleep(30)  # Sleep for 10 minutes before restarting the loop
