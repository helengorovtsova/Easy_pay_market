from faker import Faker
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "easy_pay_market.settings")
django.setup()

from pay_market.models import Discount, Item, Tax

def create_fake_data():
    fake = Faker()
    for _ in range(10):
        Item.objects.create(
            name=fake.word(),
            price=fake.pyfloat(left_digits=4, right_digits=2, positive=True),
            description=fake.text(),
        )
    Tax.objects.create(
        name="GST",
        amount=10,
    )
    Discount.objects.create(
        name="Season sale",
        amount=20,
    )
    print("Test data created.")

if __name__ == '__main__':
    create_fake_data()
