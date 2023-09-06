import uuid
from sqlalchemy import types


class UUIDType(types.TypeDecorator):
    """
    A custom uuid type for SQLAlchemy that uses Postgresql's UUID type
    when using Postgresql, otherwise uses a CHAR(36), storing as stringified
    hex values.
    """

    impl = types.String(36)

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(types.UUID())
        else:
            return dialect.type_descriptor(types.String(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return value if isinstance(value, uuid.UUID) else uuid.UUID(value)
        else:
            return str(value) if isinstance(value, uuid.UUID) else value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return value
        else:
            return uuid.UUID(value)
