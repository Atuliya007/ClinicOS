"""complete ClinicOS workflow tables

Revision ID: a1b2c3d4e5f6
Revises: fc67b9477b96
"""
from alembic import op
import sqlalchemy as sa

revision = "a1b2c3d4e5f6"
down_revision = "fc67b9477b96"
branch_labels = None
depends_on = None

def audit_columns():
    return [sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False)]

def upgrade():
    op.create_table("departments", sa.Column("department_code",sa.String(20),nullable=False,unique=True),sa.Column("name",sa.String(120),nullable=False,unique=True),sa.Column("description",sa.Text()),sa.Column("is_active",sa.Boolean(),nullable=False,server_default=sa.true()),*audit_columns())
    op.create_table("receptionists", sa.Column("receptionist_code",sa.String(20),nullable=False,unique=True),sa.Column("first_name",sa.String(100),nullable=False),sa.Column("last_name",sa.String(100),nullable=False),sa.Column("phone_number",sa.String(20),nullable=False,unique=True),sa.Column("email",sa.String(255),unique=True),sa.Column("shift",sa.Enum("MORNING","EVENING","NIGHT",name="shift"),nullable=False),sa.Column("is_active",sa.Boolean(),nullable=False,server_default=sa.true()),*audit_columns())
    op.create_table("appointments",sa.Column("patient_id",sa.Uuid(),sa.ForeignKey("patients.id"),nullable=False),sa.Column("doctor_id",sa.Uuid(),sa.ForeignKey("doctors.id"),nullable=False),sa.Column("receptionist_id",sa.Uuid(),sa.ForeignKey("receptionists.id"),nullable=False),sa.Column("problem",sa.Text(),nullable=False),sa.Column("appointment_datetime",sa.DateTime(timezone=True),nullable=False),sa.Column("appointment_status",sa.Enum("PENDING","WAITING","IN_PROCESS","COMPLETED","CANCELLED","NO_SHOW",name="appointmentstatus"),nullable=False),sa.Column("notes",sa.Text()),*audit_columns(),sa.UniqueConstraint("doctor_id","appointment_datetime",name="uq_doctor_appointment_datetime"))
    op.create_table("lab_tests",sa.Column("test_code",sa.String(20),unique=True,nullable=False),sa.Column("name",sa.String(150),unique=True,nullable=False),sa.Column("price",sa.Numeric(10,2),nullable=False),sa.Column("description",sa.Text()),sa.Column("is_active",sa.Boolean(),nullable=False,server_default=sa.true()),*audit_columns())
    op.create_table("lab_orders",sa.Column("patient_id",sa.Uuid(),sa.ForeignKey("patients.id"),nullable=False),sa.Column("lab_test_id",sa.Uuid(),sa.ForeignKey("lab_tests.id"),nullable=False),sa.Column("appointment_id",sa.Uuid(),sa.ForeignKey("appointments.id")),sa.Column("status",sa.Enum("ORDERED","SAMPLE_COLLECTED","PROCESSING","COMPLETED","CANCELLED",name="laborderstatus"),nullable=False),sa.Column("result",sa.Text()),sa.Column("notes",sa.Text()),sa.Column("completed_at",sa.DateTime(timezone=True)),*audit_columns())
    op.create_table("medicines",sa.Column("medicine_code",sa.String(20),unique=True,nullable=False),sa.Column("name",sa.String(150),unique=True,nullable=False),sa.Column("description",sa.Text()),sa.Column("unit_price",sa.Numeric(10,2),nullable=False),sa.Column("stock_quantity",sa.Integer(),nullable=False),sa.Column("reorder_level",sa.Integer(),nullable=False),sa.Column("is_active",sa.Boolean(),nullable=False,server_default=sa.true()),*audit_columns())
    op.create_table("prescriptions",sa.Column("patient_id",sa.Uuid(),sa.ForeignKey("patients.id"),nullable=False),sa.Column("doctor_id",sa.Uuid(),sa.ForeignKey("doctors.id"),nullable=False),sa.Column("appointment_id",sa.Uuid(),sa.ForeignKey("appointments.id")),sa.Column("notes",sa.Text()),*audit_columns())
    op.create_table("prescription_items",sa.Column("prescription_id",sa.Uuid(),sa.ForeignKey("prescriptions.id"),nullable=False),sa.Column("medicine_id",sa.Uuid(),sa.ForeignKey("medicines.id"),nullable=False),sa.Column("quantity",sa.Integer(),nullable=False),sa.Column("dosage",sa.String(255),nullable=False),sa.Column("dispensed_quantity",sa.Integer(),nullable=False,server_default="0"),*audit_columns())
    op.create_table("invoices",sa.Column("invoice_code",sa.String(20),unique=True,nullable=False),sa.Column("patient_id",sa.Uuid(),sa.ForeignKey("patients.id"),nullable=False),sa.Column("appointment_id",sa.Uuid(),sa.ForeignKey("appointments.id")),sa.Column("total_amount",sa.Numeric(12,2),nullable=False),sa.Column("paid_amount",sa.Numeric(12,2),nullable=False),sa.Column("payment_status",sa.Enum("PENDING","PARTIALLY_PAID","PAID","CANCELLED",name="paymentstatus"),nullable=False),*audit_columns())
    op.create_table("invoice_items",sa.Column("invoice_id",sa.Uuid(),sa.ForeignKey("invoices.id"),nullable=False),sa.Column("description",sa.String(255),nullable=False),sa.Column("quantity",sa.Integer(),nullable=False),sa.Column("unit_price",sa.Numeric(12,2),nullable=False),sa.Column("line_total",sa.Numeric(12,2),nullable=False),*audit_columns())
    op.create_table("payments",sa.Column("invoice_id",sa.Uuid(),sa.ForeignKey("invoices.id"),nullable=False),sa.Column("amount",sa.Numeric(12,2),nullable=False),sa.Column("method",sa.Enum("CASH","CARD","UPI","BANK_TRANSFER",name="paymentmethod"),nullable=False),*audit_columns())
    for table,column in [("patients","phone_number"),("doctors","phone_number"),("appointments","patient_id"),("appointments","doctor_id"),("appointments","receptionist_id"),("appointments","appointment_datetime")]: op.create_index(f"ix_{table}_{column}",table,[column],unique=table in {"patients", "doctors"})

def downgrade():
    for table in ["payments","invoice_items","invoices","prescription_items","prescriptions","medicines","lab_orders","lab_tests","appointments","receptionists","departments"]: op.drop_table(table)
