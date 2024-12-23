# Generated by Django 5.1.1 on 2024-11-19 11:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0012_schoolyear_remove_semestercurriculum_semester_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(default='2024', max_length=50)),
                ('subject', models.CharField(max_length=100, null=True)),
                ('details', models.TextField()),
                ('image', models.ImageField(upload_to='curriculum_images/')),
                ('syllabus_link', models.URLField(blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='semester',
            name='school_year',
        ),
        migrations.AddField(
            model_name='semester',
            name='session',
            field=models.CharField(default='2024', max_length=100),
        ),
        migrations.AlterField(
            model_name='semesteractivity',
            name='date',
            field=models.CharField(max_length=255),
        ),
        migrations.CreateModel(
            name='OfferedSubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit_hours', models.PositiveIntegerField()),
                ('offered_in', models.CharField(choices=[('Morning', 'Morning'), ('Evening', 'Evening')], max_length=50)),
                ('capacity', models.PositiveIntegerField(default=0)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sms.teacher')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sms.subject')),
            ],
        ),
        migrations.DeleteModel(
            name='SchoolYear',
        ),
    ]