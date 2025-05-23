import mysql.connector
from faker import Faker
from tqdm import tqdm

fake = Faker()

COLUMNS = [
    "order_id",
    "user_id",
    "product_id",
    "product_name",
    "category_id",
    "price",
    "quantity",
    "discount",
    "tax",
    "status",
    "order_date",
    "delivery_date",
    "city",
    "state",
    "country_id",
    "email",
    "phone",
    "customer_name",
    "shipping_address",
    "billing_address",
    "rating",
    "is_returned",
    "platform",
    "device_type",
    "notes",
    "coupon_code",
    "shipping_method",
    "payment_method",
    "invoice_number",
    "gift_wrap",
    "warehouse_id",
    "batch_number",
    "supplier_id",
    "shipment_id",
    "carrier_id",
    "tracking_number",
    "browser",
    "os",
    "os_version",
    "ip_address",
    "user_agent",
    "latitude",
    "longitude",
    "timezone",
    "campaign_name",
    "referral_source",
    "session_id",
    "page_views",
    "clicks",
    "impressions",
    "is_new_customer",
    "conversion_rate",
    "avg_order_value",
    "lifetime_value",
    "loyalty_points",
    "membership_level",
    "age",
    "occupation",
    "education_level",
    "income_range",
    "marital_status",
    "preferred_language",
    "custom_field_1",
    "custom_field_2",
    "custom_field_3",
    "custom_field_4",
]


def create_table(cursor):
    cursor.execute("DROP TABLE IF EXISTS test_data")
    cursor.execute("""
    CREATE TABLE test_data (
        order_id INT PRIMARY KEY,
        user_id INT,
        product_id INT,
        product_name VARCHAR(255),
        category_id INT,
        price DECIMAL(10,2),
        quantity INT,
        discount FLOAT,
        tax FLOAT,
        status VARCHAR(20),
        order_date BIGINT,
        delivery_date BIGINT,
        city VARCHAR(100),
        state VARCHAR(100),
        country_id INT,
        email VARCHAR(255),
        phone VARCHAR(50),
        customer_name VARCHAR(255),
        shipping_address TEXT,
        billing_address TEXT,
        rating FLOAT,
        is_returned BOOLEAN,
        platform VARCHAR(50),
        device_type VARCHAR(50),
        notes TEXT,
        coupon_code VARCHAR(50),
        shipping_method VARCHAR(50),
        payment_method VARCHAR(50),
        invoice_number VARCHAR(50),
        gift_wrap VARCHAR(10),
        warehouse_id INT,
        batch_number INT,
        supplier_id INT,
        shipment_id INT,
        carrier_id INT,
        tracking_number VARCHAR(50),
        browser VARCHAR(50),
        os VARCHAR(50),
        os_version INT,
        ip_address VARCHAR(50),
        user_agent TEXT,
        latitude DOUBLE,
        longitude DOUBLE,
        timezone VARCHAR(100),
        campaign_name VARCHAR(255),
        referral_source VARCHAR(255),
        session_id VARCHAR(50),
        page_views INT,
        clicks INT,
        impressions INT,
        is_new_customer BOOLEAN,
        conversion_rate FLOAT,
        avg_order_value FLOAT,
        lifetime_value FLOAT,
        loyalty_points INT,
        membership_level VARCHAR(50),
        age INT,
        occupation VARCHAR(100),
        education_level VARCHAR(50),
        income_range VARCHAR(50),
        marital_status VARCHAR(50),
        preferred_language VARCHAR(100),
        custom_field_1 VARCHAR(100),
        custom_field_2 VARCHAR(100),
        custom_field_3 VARCHAR(100),
        custom_field_4 VARCHAR(100)
    )
    """)


def generate_fake_row(idx):
    return (
        idx,  # order_id
        fake.random_int(1, 10000),  # user_id
        fake.random_int(1, 100000),  # product_id
        fake.word(),  # product_name
        fake.random_int(1, 50),  # category_id
        round(fake.random_number(digits=3) + fake.random.random(), 2),  # price
        fake.random_int(1, 10),  # quantity
        round(fake.random.uniform(0, 0.3), 2),  # discount
        round(fake.random.uniform(0, 0.2), 2),  # tax
        fake.random_element(["pending", "shipped", "delivered", "returned"]),  # status
        fake.random_int(1600000000, 1700000000),  # order_date
        fake.random_int(1600000000, 1700000000),  # delivery_date
        fake.city(),  # city
        fake.state(),  # state
        fake.random_int(1, 200),  # country_id
        fake.email(),  # email
        fake.phone_number(),  # phone
        fake.name(),  # customer_name
        fake.address().replace("\n", ", "),  # shipping_address
        fake.address().replace("\n", ", "),  # billing_address
        round(fake.random.uniform(1, 5), 1),  # rating
        fake.boolean(chance_of_getting_true=10),  # is_returned
        fake.random_element(["web", "mobile", "app"]),  # platform
        fake.random_element(["desktop", "tablet", "phone"]),  # device_type
        fake.text(max_nb_chars=50),  # notes
        fake.bothify(text="???###"),  # coupon_code
        fake.random_element(["standard", "express", "overnight"]),  # shipping_method
        fake.random_element(["credit_card", "paypal", "cash"]),  # payment_method
        fake.bothify(text="INV#######"),  # invoice_number
        fake.random_element(["yes", "no"]),  # gift_wrap
        fake.random_int(1, 50),  # warehouse_id
        fake.random_int(1, 100),  # batch_number
        fake.random_int(1, 5000),  # supplier_id
        fake.random_int(1, 10000),  # shipment_id
        fake.random_int(1, 300),  # carrier_id
        fake.bothify(text="TRK######"),  # tracking_number
        fake.random_element(["Chrome", "Firefox", "Safari", "Edge"]),  # browser
        fake.random_element(["Windows", "Linux", "macOS", "Android", "iOS"]),  # os
        fake.random_int(1, 15),  # os_version
        fake.ipv4(),  # ip_address
        fake.user_agent(),  # user_agent
        fake.latitude(),  # latitude
        fake.longitude(),  # longitude
        fake.timezone(),  # timezone
        fake.word(),  # campaign_name
        fake.word(),  # referral_source
        fake.uuid4()[:8],  # session_id
        fake.random_int(1, 5000),  # page_views
        fake.random_int(1, 1000),  # clicks
        fake.random_int(1, 10000),  # impressions
        fake.boolean(chance_of_getting_true=30),
        round(fake.random.uniform(0, 1), 3),  # conversion_rate
        round(fake.random.uniform(10, 1000), 2),  # avg_order_value
        round(fake.random.uniform(100, 10000), 2),  # lifetime_value
        fake.random_int(0, 1000),  # loyalty_points
        fake.random_element(
            ["Bronze", "Silver", "Gold", "Platinum"]
        ),  # membership_level
        fake.random_int(18, 75),  # age
        fake.job(),  # occupation
        fake.random_element(
            ["High School", "Bachelors", "Masters", "PhD"]
        ),  # education_level
        fake.random_element(["<20K", "20K-50K", "50K-100K", ">100K"]),  # income_range
        fake.random_element(["Single", "Married", "Divorced"]),  # marital_status
        fake.random_element(
            ["English", "Spanish", "French", "Mandarin"]
        ),  # prefered_language
        fake.word(),
        fake.word(),
        fake.word(),
        fake.word(),
    )


def insert_rows(cursor, table_name, columns, rows):
    cols_str = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(columns))
    sql = f"INSERT INTO {table_name} ({cols_str}) VALUES ({placeholders})"
    cursor.executemany(sql, rows)


def main():
    conn = mysql.connector.connect(
        host="localhost", user="root", password="root", database="test_performance"
    )
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS test_performance")
    cursor.execute("USE test_performance")
    create_table(cursor)

    cursor.execute("TRUNCATE TABLE test_data")

    print("Generating and inserting data...")
    batch_size = 1000
    total_rows = 100000
    data_batch = []

    for i in tqdm(range(1, total_rows + 1)):
        data_batch.append(generate_fake_row(i))
        if i % batch_size == 0:
            insert_rows(cursor, "test_data", COLUMNS, data_batch)
            conn.commit()
            data_batch = []

    if data_batch:
        insert_rows(cursor, "test_data", COLUMNS, data_batch)
        conn.commit()

    print("Data generation and insertion completed.")
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
