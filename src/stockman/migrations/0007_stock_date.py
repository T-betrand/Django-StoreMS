# Generated by Django 2.2 on 2021-08-15 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockman', '0006_auto_20210815_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='date',
            field=models.DateTimeField(null=True),
        ),
    ]