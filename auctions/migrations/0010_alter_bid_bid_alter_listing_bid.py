# Generated by Django 5.0.3 on 2024-04-13 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_rename_bidamount_bid_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid',
            field=models.DecimalField(decimal_places=10, max_digits=19),
        ),
        migrations.AlterField(
            model_name='listing',
            name='bid',
            field=models.DecimalField(decimal_places=2, max_digits=19),
        ),
    ]
