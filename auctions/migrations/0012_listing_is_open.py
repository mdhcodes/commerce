# Generated by Django 5.0.3 on 2024-04-16 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_alter_bid_bid_alter_listing_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='is_open',
            field=models.BooleanField(default=True),
        ),
    ]
