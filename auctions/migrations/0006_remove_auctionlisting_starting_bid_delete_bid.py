# Generated by Django 4.2.3 on 2023-11-26 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_bid_starting_bid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlisting',
            name='starting_bid',
        ),
        migrations.DeleteModel(
            name='Bid',
        ),
    ]
