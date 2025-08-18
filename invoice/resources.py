from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Invoice, User

class InvoiceResource(resources.ModelResource):
    created_by = fields.Field(attribute='created_by', column_name='Created By', widget=ForeignKeyWidget(User, 'username'))
    reviewed_by = fields.Field(attribute='reviewed_by', column_name='Reviewed By', widget=ForeignKeyWidget(User, 'username'))
    received_by = fields.Field(attribute='received_by', column_name='Received By', widget=ForeignKeyWidget(User, 'username'))

    class Meta:
        model = Invoice
        fields = (
            'invoice_number',
            'customer_name',
            'amount',
            'status',
            'date_received',
            'payment_due_date',
            'created_by',
            'reviewed_by',
            'received_by',
            'received_at',
            'CIT_declaration',
            'good_received_note',
            'delivery_note',
            'purchase_order',
            'profoma',
            'contract_copy',
            'final_notification_letter',
            'tender_evaluation_report',
            'perfomance_guaranty',
            'advance_security',
            'tender_advertisement',
            'requisition_form',
            'official_appointment_of_receiving_committee',
            'evaluation_report_of_previous_period',
            'attendance_list',
            'mission_clearance_signed_at_destination',
            'received_by_finance',
        )

    def dehydrate_CIT_declaration(self, obj):
        return "Yes" if obj.CIT_declaration else "No"

    def dehydrate_good_received_note(self, obj):
        return "Yes" if obj.good_received_note else "No"

    def dehydrate_delivery_note(self, obj):
        return "Yes" if obj.delivery_note else "No"

    def dehydrate_purchase_order(self, obj):
        return "Yes" if obj.purchase_order else "No"

    def dehydrate_profoma(self, obj):
        return "Yes" if obj.profoma else "No"

    def dehydrate_contract_copy(self, obj):
        return "Yes" if obj.contract_copy else "No"

    def dehydrate_final_notification_letter(self, obj):
        return "Yes" if obj.final_notification_letter else "No"

    def dehydrate_tender_evaluation_report(self, obj):
        return "Yes" if obj.tender_evaluation_report else "No"

    def dehydrate_perfomance_guaranty(self, obj):
        return "Yes" if obj.perfomance_guaranty else "No"

    def dehydrate_advance_security(self, obj):
        return "Yes" if obj.advance_security else "No"

    def dehydrate_tender_advertisement(self, obj):
        return "Yes" if obj.tender_advertisement else "No"

    def dehydrate_requisition_form(self, obj):
        return "Yes" if obj.requisition_form else "No"

    def dehydrate_official_appointment_of_receiving_committee(self, obj):
        return "Yes" if obj.official_appointment_of_receiving_committee else "No"

    def dehydrate_evaluation_report_of_previous_period(self, obj):
        return "Yes" if obj.evaluation_report_of_previous_period else "No"

    def dehydrate_attendance_list(self, obj):
        return "Yes" if obj.attendance_list else "No"

    def dehydrate_mission_clearance_signed_at_destination(self, obj):
        return "Yes" if obj.mission_clearance_signed_at_destination else "No"

    def dehydrate_received_by_finance(self, obj):
        return "Yes" if obj.received_by_finance else "No"
