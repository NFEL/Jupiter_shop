# Generated by Django 3.1.2 on 2020-12-26 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phonenumber',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_join_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
