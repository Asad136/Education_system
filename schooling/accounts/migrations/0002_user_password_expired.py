# Generated by Django 5.0.7 on 2024-08-08 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password_expired',
            field=models.BooleanField(default=False),
        ),
    ]
