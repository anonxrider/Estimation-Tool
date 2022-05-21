# Generated by Django 4.0.4 on 2022-05-19 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0007_invoice_total_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(max_length=100)),
                ('bill_titlefront', models.CharField(max_length=100)),
                ('bill_titleback', models.CharField(max_length=100)),
                ('bill_title', models.CharField(max_length=100)),
                ('termsandconditions', models.CharField(max_length=100)),
                ('fulldescription', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('service_type', models.CharField(max_length=100)),
                ('total_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('service', models.TextField(max_length=100)),
                ('gst', models.CharField(max_length=100)),
                ('gsttotal', models.CharField(max_length=100)),
                ('subtotal', models.CharField(max_length=100)),
                ('gstpercentage', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=False)),
                ('currency', models.TextField(max_length=100)),
                ('footer', models.TextField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(max_length=100)),
                ('bill_title', models.CharField(max_length=100)),
                ('termsandconditions', models.CharField(max_length=100)),
                ('fulldescription', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('service_type', models.CharField(max_length=100)),
                ('total_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('service', models.TextField(max_length=100)),
                ('subtotal', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=False)),
                ('currency', models.TextField(max_length=100)),
                ('footer', models.TextField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='LineItem1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.TextField()),
                ('description', models.TextField()),
                ('quantity', models.IntegerField()),
                ('rate', models.DecimalField(decimal_places=2, max_digits=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=100)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.invoice1')),
            ],
        ),
        migrations.CreateModel(
            name='LineItem2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.TextField()),
                ('description', models.TextField()),
                ('quantity', models.IntegerField()),
                ('amount', models.CharField(max_length=100)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.invoice2')),
            ],
        ),
        migrations.RemoveField(
            model_name='lineitem',
            name='customer',
        ),
        migrations.DeleteModel(
            name='Invoice',
        ),
        migrations.DeleteModel(
            name='LineItem',
        ),
    ]