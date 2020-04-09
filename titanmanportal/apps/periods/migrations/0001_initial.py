# Generated by Django 3.0.4 on 2020-04-09 12:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_datetime', models.DateTimeField(editable=False)),
                ('start', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Period start date')),
                ('end', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Period end date')),
            ],
            options={
                'get_latest_by': 'start',
                'unique_together': {('start', 'end')},
            },
        ),
    ]
