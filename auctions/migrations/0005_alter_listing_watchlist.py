# Generated by Django 5.0.3 on 2024-04-11 17:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_remove_listing_watchlist_alter_listing_createdby_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='watch_list', to=settings.AUTH_USER_MODEL),
        ),
    ]
