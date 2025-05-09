# Generated by Django 5.0.14 on 2025-04-19 16:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0004_dog_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='DogParent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Кличка Родителя')),
                ('birthe_date', models.DateField(blank=True, null=True, verbose_name='Дата рождения Родителя')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dogs.breed', verbose_name='Порода Родителя')),
                ('dog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dogs.dog')),
            ],
            options={
                'verbose_name': 'parent',
                'verbose_name_plural': 'parents',
            },
        ),
    ]
