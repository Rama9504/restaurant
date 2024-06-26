# Generated by Django 5.0.3 on 2024-04-08 16:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0009_deliverymappingss'),
        ('sapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField()),
                ('complaint', models.CharField(max_length=200)),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.dishes')),
                ('ords', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.orders')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sapp.userprofile')),
            ],
        ),
    ]
