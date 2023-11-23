from django.db import migrations

import organizations.fields


class Migration(migrations.Migration):
    dependencies = [("organizations", "0002_model_update")]

    operations = [
        migrations.AlterField(
            model_name="organization",
            name="slug",
            field=organizations.fields.SlugField(
                editable=True,
                help_text="The name in all lowercase, suitable for URL identification",
                max_length=200,
                populate_from="name",
                unique=True,
            ),
        )
    ]
