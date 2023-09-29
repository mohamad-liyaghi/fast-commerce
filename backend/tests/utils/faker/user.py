from faker import Faker

faker = Faker()
USER_PASSWORD = "1234"


async def create_fake_credential() -> dict:
    return {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "email": faker.email(),
        "password": USER_PASSWORD,
    }
