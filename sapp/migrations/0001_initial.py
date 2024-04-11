# Generated by Django 4.1.7 on 2024-03-07 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('phone', models.BigIntegerField(unique=True)),
                ('password', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('streetname', models.CharField(default='a', max_length=50)),
                ('villagecity', models.CharField(default='v', max_length=50)),
                ('pincode', models.BigIntegerField(default=0)),
                ('state', models.CharField(default='andhra pradesh', max_length=50)),
                ('country', models.CharField(default='india', max_length=50)),
                ('usersname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sapp.userprofile')),
            ],
        ),
    ]
