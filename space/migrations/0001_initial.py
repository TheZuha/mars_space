# Generated by Django 5.1.2 on 2024-11-01 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner', models.ImageField(upload_to='banners/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
