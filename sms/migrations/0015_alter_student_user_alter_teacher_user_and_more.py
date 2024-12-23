# Generated by Django 5.1.1 on 2024-11-24 10:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0014_grade_remove_curriculum_image_alter_curriculum_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student', to='sms.user'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='teacher', to='sms.user'),
        ),
        migrations.AlterField(
            model_name='user',
            name='contact_no',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
