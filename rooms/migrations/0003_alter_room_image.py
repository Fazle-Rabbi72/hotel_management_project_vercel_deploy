# Generated by Django 5.1.1 on 2024-09-27 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0002_alter_room_room_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='image',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]