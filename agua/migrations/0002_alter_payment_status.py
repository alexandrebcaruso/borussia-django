# Generated by Django 5.1.3 on 2024-12-16 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agua', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('rejected', 'Rejected'), ('awaiting_approval', 'Awaiting Approval'), ('paid', 'Paid')], default='awaiting_approval', max_length=20),
        ),
    ]
