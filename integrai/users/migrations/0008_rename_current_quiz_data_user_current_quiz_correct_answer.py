# Generated by Django 5.1.7 on 2025-04-01 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_current_quiz_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='current_quiz_data',
            new_name='current_quiz_correct_answer',
        ),
    ]
