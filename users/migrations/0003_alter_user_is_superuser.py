# Generated by Django 4.1 on 2022-11-06 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_user_message"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="is_superuser",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
