from alembic import op
import sqlalchemy as sa

revision = '3fe0f65a9ceb'
down_revision = '4bfe71371157'  # Replace with the actual previous migration ID
branch_labels = None
depends_on = None


def upgrade():
    # Drop foreign key temporarily
    op.drop_constraint("fk_invoices_booking_id_bookings", "invoices", type_="foreignkey")

    # Change bookings.id type
    op.alter_column("bookings", "id",
                    existing_type=sa.INTEGER(),
                    type_=sa.String(36),
                    existing_nullable=False)

    # Change invoices.booking_id type
    op.alter_column("invoices", "booking_id",
                    existing_type=sa.INTEGER(),
                    type_=sa.String(36),
                    existing_nullable=False)

    # Recreate foreign key
    op.create_foreign_key("fk_invoices_booking_id_bookings",
                          "invoices", "bookings",
                          ["booking_id"], ["id"])

def downgrade():
    # Reverse the process if needed
    op.drop_constraint("fk_invoices_booking_id_bookings", "invoices", type_="foreignkey")

    op.alter_column("invoices", "booking_id",
                    existing_type=sa.String(36),
                    type_=sa.INTEGER(),
                    existing_nullable=False)

    op.alter_column("bookings", "id",
                    existing_type=sa.String(36),
                    type_=sa.INTEGER(),
                    existing_nullable=False)

    op.create_foreign_key("fk_invoices_booking_id_bookings",
                          "invoices", "bookings",
                          ["booking_id"], ["id"])
