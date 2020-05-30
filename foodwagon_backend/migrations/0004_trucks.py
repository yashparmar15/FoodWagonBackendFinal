# Generated by Django 3.0.3 on 2020-05-23 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodwagon_backend', '0003_auto_20200522_1934'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trucks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Model_Name', models.CharField(max_length=50)),
                ('Price', models.IntegerField()),
                ('Description', models.CharField(max_length=255)),
                ('image1', models.ImageField(blank=True, max_length=255, null=True, upload_to='picture/')),
                ('image2', models.ImageField(blank=True, max_length=255, null=True, upload_to='picture/')),
                ('image3', models.ImageField(blank=True, max_length=255, null=True, upload_to='picture/')),
                ('image4', models.ImageField(blank=True, max_length=255, null=True, upload_to='picture/')),
                ('image5', models.ImageField(blank=True, max_length=255, null=True, upload_to='picture/')),
            ],
        ),
    ]
