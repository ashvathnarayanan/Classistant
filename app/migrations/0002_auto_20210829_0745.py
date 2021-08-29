# Generated by Django 2.2.8 on 2021-08-29 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='total_students',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='student',
            name='classes',
            field=models.ManyToManyField(related_name='students', to='app.Class'),
        ),
    ]