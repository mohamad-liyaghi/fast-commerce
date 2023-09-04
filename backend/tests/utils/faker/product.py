from faker import Faker

faker = Faker()


async def create_product_credential() -> dict:
    return {
        "title": faker.name(),
        "description": faker.text(),
        "price": 1234,
        "specs": {
            "color": faker.color_name(),
            "size": "M",
            "weight": 123,
        },
    }
