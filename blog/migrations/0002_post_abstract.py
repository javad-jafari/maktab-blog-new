# Generated by Django 3.1.4 on 2020-12-06 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='abstract',
            field=models.CharField(default='none', max_length=130, verbose_name='Abstract'),
        ),
    ]
