# Generated by Django 3.0.6 on 2020-05-31 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodwagon_backend', '0018_auto_20200531_1949'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItemTruck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='foodwagon_backend.Order')),
                ('truck', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='foodwagon_backend.Trucks')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItemVenue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='foodwagon_backend.Order')),
                ('venue', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='foodwagon_backend.Venues')),
            ],
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]