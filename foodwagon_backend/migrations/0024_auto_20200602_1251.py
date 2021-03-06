# Generated by Django 3.0.6 on 2020-06-02 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodwagon_backend', '0023_merge_20200601_1358'),
    ]

    operations = [
        migrations.CreateModel(
            name='Special',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('speciality', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='chef',
            name='Speciality',
        ),
        migrations.AddField(
            model_name='chef',
            name='Speciality',
            field=models.ManyToManyField(to='foodwagon_backend.Special'),
        ),
    ]
