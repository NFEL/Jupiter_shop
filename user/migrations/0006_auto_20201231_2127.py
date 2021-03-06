# Generated by Django 3.1.2 on 2020-12-31 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20201231_1139'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.AlterField(
            model_name='user',
            name='phonenumber',
            field=models.CharField(blank=True, max_length=12, null=True, unique=True),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.UniqueConstraint(fields=('phonenumber', 'email'), name='only one email / phone per user'),
        ),
    ]
