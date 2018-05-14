# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("test_vendors", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="vendor",
            name="city",
            field=models.CharField(default="", max_length=100),
        ),
        migrations.AlterField(
            model_name="vendor",
            name="street_address",
            field=models.CharField(default="", max_length=100),
        ),
        migrations.AlterField(
            model_name="vendoruser",
            name="user_type",
            field=models.CharField(default="", max_length=1),
        ),
    ]
