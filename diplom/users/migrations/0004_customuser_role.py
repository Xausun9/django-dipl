# Generated by Django 4.2.21 on 2025-05-12 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_customuser_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('student', 'Студент'), ('secretary', 'Секретарь'), ('admin', 'Администратор')], default='admin', max_length=20),
            preserve_default=False,
        ),
    ]
