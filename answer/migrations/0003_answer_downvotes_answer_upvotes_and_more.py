# Generated by Django 4.0 on 2022-04-26 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('answer', '0002_alter_answercomment_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='downvotes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='answer',
            name='upvotes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='answercomment',
            name='downvotes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='answercomment',
            name='upvotes',
            field=models.IntegerField(default=0),
        ),
    ]
