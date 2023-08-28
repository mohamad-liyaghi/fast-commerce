from faker import Faker

faker = Faker()


async def create_vendor_credential() -> dict:
    return {
        "name": faker.name(),
        "description": faker.text(),
        "domain": faker.url(),
        "address": faker.address(),
    }
