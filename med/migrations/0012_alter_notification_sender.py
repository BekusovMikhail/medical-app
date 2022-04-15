# Generated by Django 4.0.3 on 2022-04-14 13:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('med', '0011_alter_notification_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='sender',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL),
        ),
    ]
