# Generated by Django 2.2 on 2021-08-14 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockman', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='category',
            field=models.CharField(blank=True, choices=[('Construction Equipment', 'Construction Equipment'), ('Electronics', 'Electronics'), ('Furniture', 'Furniture'), ('IT Equipment', 'IT Equipment'), ('Phone', 'Phone')], max_length=50, null=True),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
