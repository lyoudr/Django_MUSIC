# Generated by Django 3.1.4 on 2021-11-12 03:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20211112_0332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='order',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='order_info_a', to='order.order'),
            preserve_default=False,
        ),
    ]
