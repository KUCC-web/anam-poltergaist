# Generated by Django 2.0.2 on 2018-03-10 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0008_question_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='content_type',
            field=models.CharField(choices=[('Q', 'Quiz'), ('W', 'Worldcup')], default='Q', max_length=1),
        ),
    ]
