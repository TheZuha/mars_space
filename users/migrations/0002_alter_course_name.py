# Generated by Django 5.1.2 on 2024-11-03 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(choices=[('Programming Backend', 'Programming Backend'), ('Programming Frontend', 'Programming Frontend'), ('Starter', 'Starter')], max_length=50),
        ),
    ]