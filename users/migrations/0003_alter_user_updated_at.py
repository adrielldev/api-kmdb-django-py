# Generated by Django 4.1.2 on 2022-10-12 22:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.DateField(default=datetime.date(2022, 10, 12)),
        ),
    ]
