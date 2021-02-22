# Generated by Django 3.1.7 on 2021-02-21 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'Active'), ('DONE', 'Done')], default='ACTIVE', max_length=10),
        ),
    ]