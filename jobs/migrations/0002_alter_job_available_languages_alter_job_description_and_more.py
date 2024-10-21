# Generated by Django 5.1.2 on 2024-10-20 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='available_languages',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='employer',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='job_categories_codes',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='location',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='position_schedule_codes',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
