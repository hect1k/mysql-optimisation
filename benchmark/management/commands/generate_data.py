from django.core.management.base import BaseCommand
from benchmark.models import TestData
from faker import Faker
from tqdm import tqdm

fake = Faker()


class Command(BaseCommand):
    help = "Generates fake test data"

    def handle(self, *args, **kwargs):
        TestData.objects.all().delete()
        total_rows = 100000
        batch_size = 1000
        buffer = []

        for i in tqdm(range(1, total_rows + 1)):
            row = TestData(
                order_id=i,
                user_id=fake.random_int(1, 10000),
                product_id=fake.random_int(1, 100000),
                product_name=fake.word(),
                category_id=fake.random_int(1, 50),
                price=round(fake.random_number(digits=3) + fake.random.random(), 2),
                quantity=fake.random_int(1, 10),
                discount=round(fake.random.uniform(0, 0.3), 2),
                tax=round(fake.random.uniform(0, 0.2), 2),
                status=fake.random_element(
                    ["pending", "shipped", "delivered", "returned"]
                ),
                order_date=fake.random_int(1600000000, 1700000000),
                delivery_date=fake.random_int(1600000000, 1700000000),
                city=fake.city(),
                state=fake.state(),
                country_id=fake.random_int(1, 200),
                email=fake.email(),
                phone=fake.phone_number(),
                customer_name=fake.name(),
                shipping_address=fake.address().replace("\n", ", "),
                billing_address=fake.address().replace("\n", ", "),
                rating=round(fake.random.uniform(1, 5), 1),
                is_returned=fake.boolean(chance_of_getting_true=10),
                platform=fake.random_element(["web", "mobile", "app"]),
                device_type=fake.random_element(["desktop", "tablet", "phone"]),
                notes=fake.text(max_nb_chars=50),
                coupon_code=fake.bothify(text="???###"),
                shipping_method=fake.random_element(
                    ["standard", "express", "overnight"]
                ),
                payment_method=fake.random_element(["credit_card", "paypal", "cash"]),
                invoice_number=fake.bothify(text="INV#######"),
                gift_wrap=fake.random_element(["yes", "no"]),
                warehouse_id=fake.random_int(1, 50),
                batch_number=fake.random_int(1, 100),
                supplier_id=fake.random_int(1, 5000),
                shipment_id=fake.random_int(1, 10000),
                carrier_id=fake.random_int(1, 300),
                tracking_number=fake.bothify(text="TRK######"),
                browser=fake.random_element(["Chrome", "Firefox", "Safari", "Edge"]),
                os=fake.random_element(["Windows", "Linux", "macOS", "Android", "iOS"]),
                os_version=fake.random_int(1, 15),
                ip_address=fake.ipv4(),
                user_agent=fake.user_agent(),
                latitude=fake.latitude(),
                longitude=fake.longitude(),
                timezone=fake.timezone(),
                campaign_name=fake.word(),
                referral_source=fake.word(),
                session_id=fake.uuid4()[:8],
                page_views=fake.random_int(1, 5000),
                clicks=fake.random_int(1, 1000),
                impressions=fake.random_int(1, 10000),
                is_new_customer=fake.boolean(chance_of_getting_true=30),
                conversion_rate=round(fake.random.uniform(0, 1), 3),
                avg_order_value=round(fake.random.uniform(10, 1000), 2),
                lifetime_value=round(fake.random.uniform(100, 10000), 2),
                loyalty_points=fake.random_int(0, 1000),
                membership_level=fake.random_element(
                    ["Bronze", "Silver", "Gold", "Platinum"]
                ),
                age=fake.random_int(18, 75),
                occupation=fake.job(),
                education_level=fake.random_element(
                    ["High School", "Bachelors", "Masters", "PhD"]
                ),
                income_range=fake.random_element(
                    ["<20K", "20K-50K", "50K-100K", ">100K"]
                ),
                marital_status=fake.random_element(["Single", "Married", "Divorced"]),
                preferred_language=fake.random_element(
                    ["English", "Spanish", "French", "Mandarin"]
                ),
                custom_field_1=fake.word(),
                custom_field_2=fake.word(),
                custom_field_3=fake.word(),
                custom_field_4=fake.word(),
            )
            buffer.append(row)

            if i % batch_size == 0:
                TestData.objects.bulk_create(buffer)
                buffer = []

        if buffer:
            TestData.objects.bulk_create(buffer)

        self.stdout.write(self.style.SUCCESS("Data generation completed."))
