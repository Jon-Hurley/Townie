# Generated by Django 4.1.6 on 2023-02-15 03:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longitude', models.DecimalField(decimal_places=13, max_digits=15)),
                ('latitude', models.DecimalField(decimal_places=13, max_digits=15)),
            ],
        ),
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('points', models.PositiveIntegerField(default=0)),
                ('location', models.OneToOneField(default='NULL', on_delete=django.db.models.deletion.CASCADE, to='townie_app.location')),
            ],
        ),
    ]
