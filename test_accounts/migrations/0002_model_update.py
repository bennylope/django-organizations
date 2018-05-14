# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("test_accounts", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="accountuser",
            name="user_type",
            field=models.CharField(default="", max_length=1),
        )
    ]
