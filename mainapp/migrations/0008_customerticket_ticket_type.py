# Generated by Django 4.1.1 on 2022-09-07 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_worker_online_worker_servicing'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerticket',
            name='ticket_type',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
