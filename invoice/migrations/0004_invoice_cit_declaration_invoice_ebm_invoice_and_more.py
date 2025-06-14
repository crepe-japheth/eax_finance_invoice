# Generated by Django 5.0 on 2025-06-05 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0003_contract_invoice_contract'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='CIT_declaration',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='EBM_invoice',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='advance_security',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='attendance_list',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='delivery_note',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='evaluation_report_of_previous_period',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='final_notification_letter',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='good_received_note',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='mission_clearance_signed_at_destination',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='official_appointment_of_receiving_committee',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='perfomance_guaranty',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='profoma',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='requisition_form',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='tender_advertisement',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='tender_evaluation_report',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='contract',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
