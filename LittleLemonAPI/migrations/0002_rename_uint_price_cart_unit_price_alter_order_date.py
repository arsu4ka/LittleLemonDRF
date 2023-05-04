# Generated by Django 4.2 on 2023-05-03 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonAPI', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='uint_price',
            new_name='unit_price',
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(auto_now=True, db_index=True),
        ),
    ]