# Generated by Django 5.0.6 on 2024-09-10 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppScraping', '0003_remove_scrapingstatus_is_scraping_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scrapingstatus',
            name='status',
        ),
        migrations.RemoveField(
            model_name='scrapingstatus',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='scrapingstatus',
            name='is_scraping',
            field=models.BooleanField(default=False),
        ),
    ]
