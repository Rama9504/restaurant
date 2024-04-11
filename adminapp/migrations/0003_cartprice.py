# Generated by Django 4.1.7 on 2024-03-11 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sapp', '0001_initial'),
        ('adminapp', '0002_alter_orders_date_of_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='cartprice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('discount', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('dish_codese', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.dishes')),
                ('usere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sapp.userprofile')),
            ],
        ),
    ]