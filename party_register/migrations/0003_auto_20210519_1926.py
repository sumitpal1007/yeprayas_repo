# Generated by Django 3.2.3 on 2021-05-19 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('party_register', '0002_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='isAdmin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='party',
            name='contact_number',
            field=models.CharField(max_length=15),
        ),
    ]
