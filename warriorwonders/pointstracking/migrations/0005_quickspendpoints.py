# Generated by Django 4.2.5 on 2023-09-28 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pointstracking', '0004_rename_added_by_point_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuickSpendPoints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField()),
            ],
        ),
    ]