import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "retail_star_warehouse.db")

def init_warehouse():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
    DROP TABLE IF EXISTS fact_sales;
    DROP TABLE IF EXISTS dim_customer;
    DROP TABLE IF EXISTS dim_product;

    CREATE TABLE dim_customer (
        customer_sk INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id TEXT NOT NULL,
        full_name TEXT NOT NULL,
        city TEXT NOT NULL,
        loyalty_tier TEXT NOT NULL,
        is_current INTEGER NOT NULL DEFAULT 1
    );

    CREATE TABLE dim_product (
        product_sk INTEGER PRIMARY KEY AUTOINCREMENT,
        sku TEXT NOT NULL,
        product_name TEXT NOT NULL,
        category TEXT NOT NULL,
        unit_cost REAL NOT NULL
    );

    CREATE TABLE fact_sales (
        sales_sk INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id TEXT NOT NULL,
        customer_sk INTEGER NOT NULL,
        product_sk INTEGER NOT NULL,
        order_date TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        net_revenue REAL NOT NULL,
        FOREIGN KEY (customer_sk) REFERENCES dim_customer(customer_sk),
        FOREIGN KEY (product_sk) REFERENCES dim_product(product_sk)
    );

    INSERT INTO dim_customer (customer_id, full_name, city, loyalty_tier, is_current) VALUES
        ('C101', 'Aarav Sharma', 'Hyderabad', 'Gold', 1),
        ('C102', 'Diya Nair', 'Bengaluru', 'Platinum', 1),
        ('C103', 'Rohan Verma', 'Hyderabad', 'Silver', 1),
        ('C104', 'Meera Iyer', 'Mumbai', 'Gold', 1);

    INSERT INTO dim_product (sku, product_name, category, unit_cost) VALUES
        ('LGT-01', 'Antique Brass Pendant Lamp', 'Decorative Lighting', 1800.0),
        ('LGT-02', 'Matte Black Wall Sconce', 'Decorative Lighting', 1100.0),
        ('LGT-03', 'Warm LED Chandelier 6-Arm', 'Luxury Fixtures', 5200.0);

    INSERT INTO fact_sales (order_id, customer_sk, product_sk, order_date, quantity, net_revenue) VALUES
        ('ORD-9001', 1, 1, '2026-10-05', 2, 5400.0),
        ('ORD-9002', 2, 3, '2026-10-12', 1, 8900.0),
        ('ORD-9003', 3, 2, '2026-10-18', 3, 5100.0),
        ('ORD-9004', 1, 3, '2026-11-02', 1, 8900.0),
        ('ORD-9005', 4, 1, '2026-11-09', 4, 10800.0);
    """)
    conn.commit()
    conn.close()
    print(f"Initialized Star Schema Warehouse at {DB_PATH}")

if __name__ == "__main__":
    init_warehouse()
