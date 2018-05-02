from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
raspb3B = Table('raspb3B', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('type', VARCHAR(length=24)),
    Column('number', VARCHAR(length=8)),
    Column('pin_info', VARCHAR(length=140)),
)

ras_models = Table('ras_models', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('mname', String(length=24)),
    Column('mpins', Integer),
)

raspb3_b_pins = Table('raspb3_b_pins', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('type', String(length=24)),
    Column('number', String(length=8)),
    Column('pin_info', String(length=140)),
)

sensors = Table('sensors', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=140)),
    Column('pin_id', Integer),
)

sensorsdb = Table('sensorsdb', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=140)),
    Column('about', String(length=140)),
    Column('pic', String(length=256)),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=64)),
    Column('password_hash', String(length=64)),
    Column('email', String(length=120)),
    Column('role', SmallInteger, default=ColumnDefault(0)),
    Column('about_me', String(length=140)),
    Column('my_raspberry', String(length=140)),
    Column('last_seen', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['raspb3B'].drop()
    post_meta.tables['ras_models'].create()
    post_meta.tables['raspb3_b_pins'].create()
    post_meta.tables['sensors'].create()
    post_meta.tables['sensorsdb'].create()
    post_meta.tables['user'].columns['my_raspberry'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['raspb3B'].create()
    post_meta.tables['ras_models'].drop()
    post_meta.tables['raspb3_b_pins'].drop()
    post_meta.tables['sensors'].drop()
    post_meta.tables['sensorsdb'].drop()
    post_meta.tables['user'].columns['my_raspberry'].drop()
