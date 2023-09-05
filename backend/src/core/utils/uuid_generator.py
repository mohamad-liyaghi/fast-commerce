from uuid import uuid4


def generate_uuid() -> str:
    return str(str(uuid4()))
