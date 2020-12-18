# Generated by Django 3.1.2 on 2020-11-23 01:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20201025_1218'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='Student',
            new_name='student',
        ),
        migrations.AddField(
            model_name='course',
            name='num_reviews',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='Order Date',
            field=models.DateField(default=datetime.datetime(2020, 11, 23, 1, 36, 6, 279404, tzinfo=utc)),
        ),
    ]
