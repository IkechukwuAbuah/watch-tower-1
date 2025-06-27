"""Initial migration with PostGIS

Revision ID: 51a2dbdd075c
Revises: 
Create Date: 2025-06-27 22:23:40.087985

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import geoalchemy2


# revision identifiers, used by Alembic.
revision: str = '51a2dbdd075c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enable PostGIS extension
    op.execute('CREATE EXTENSION IF NOT EXISTS postgis')
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    
    # Create trucks table
    op.create_table('trucks',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('truck_number', sa.String(length=50), nullable=False),
        sa.Column('loconav_vehicle_id', sa.String(length=100), nullable=True),
        sa.Column('company', sa.String(length=100), nullable=True),
        sa.Column('fleet_manager', sa.String(length=100), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True, server_default='operational'),
        sa.Column('brand', sa.String(length=50), nullable=True),
        sa.Column('trailer_size', sa.String(length=20), nullable=True),
        sa.Column('operating_location', sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('loconav_vehicle_id'),
        sa.UniqueConstraint('truck_number')
    )
    
    # Create trips table
    op.create_table('trips',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('vpc_id', sa.String(length=100), nullable=False),
        sa.Column('loconav_trip_id', sa.String(length=100), nullable=True),
        sa.Column('truck_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=True, server_default='scheduled'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('origin_location', geoalchemy2.types.Geography(geometry_type='POINT', srid=4326), nullable=True),
        sa.Column('destination_location', geoalchemy2.types.Geography(geometry_type='POINT', srid=4326), nullable=True),
        sa.Column('origin_address', sa.Text(), nullable=True),
        sa.Column('destination_address', sa.Text(), nullable=True),
        sa.Column('distance_km', sa.DECIMAL(precision=8, scale=2), nullable=True),
        sa.Column('estimated_duration_minutes', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['truck_id'], ['trucks.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('loconav_trip_id'),
        sa.UniqueConstraint('vpc_id')
    )
    op.create_index(op.f('ix_trips_status'), 'trips', ['status'], unique=False)
    op.create_index(op.f('ix_trips_truck_id'), 'trips', ['truck_id'], unique=False)
    
    # Create vehicle_positions table
    op.create_table('vehicle_positions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('truck_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('location', geoalchemy2.types.Geography(geometry_type='POINT', srid=4326), nullable=False),
        sa.Column('speed', sa.DECIMAL(precision=5, scale=2), nullable=True),
        sa.Column('heading', sa.Integer(), nullable=True),
        sa.Column('ignition', sa.Boolean(), nullable=True),
        sa.Column('altitude', sa.DECIMAL(precision=8, scale=2), nullable=True),
        sa.Column('accuracy', sa.DECIMAL(precision=6, scale=2), nullable=True),
        sa.ForeignKeyConstraint(['truck_id'], ['trucks.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_vehicle_positions_location'), 'vehicle_positions', ['location'], unique=False, postgresql_using='gist')
    op.create_index(op.f('ix_vehicle_positions_timestamp'), 'vehicle_positions', ['timestamp'], unique=False)
    op.create_index(op.f('ix_vehicle_positions_truck_id'), 'vehicle_positions', ['truck_id'], unique=False)


def downgrade() -> None:
    # Drop tables
    op.drop_index(op.f('ix_vehicle_positions_truck_id'), table_name='vehicle_positions')
    op.drop_index(op.f('ix_vehicle_positions_timestamp'), table_name='vehicle_positions')
    op.drop_index(op.f('ix_vehicle_positions_location'), table_name='vehicle_positions', postgresql_using='gist')
    op.drop_table('vehicle_positions')
    
    op.drop_index(op.f('ix_trips_truck_id'), table_name='trips')
    op.drop_index(op.f('ix_trips_status'), table_name='trips')
    op.drop_table('trips')
    
    op.drop_table('trucks')
    
    # Drop extensions
    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp"')
    op.execute('DROP EXTENSION IF EXISTS postgis')