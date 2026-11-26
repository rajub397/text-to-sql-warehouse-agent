import os
from warehouse_setup import init_warehouse, DB_PATH
from sql_guardrails import execute_safe_query

INTENT_TEMPLATES = {
    "revenue by city": """
        SELECT c.city, COUNT(f.order_id) AS total_orders, SUM(f.net_revenue) AS total_revenue
        FROM fact_sales f
        JOIN dim_customer c ON f.customer_sk = c.customer_sk
        GROUP BY c.city
        ORDER BY total_revenue DESC;
    """,
    "top products": """
        SELECT p.product_name, p.category, SUM(f.quantity) AS units_sold, SUM(f.net_revenue) AS revenue
        FROM fact_sales f
        JOIN dim_product p ON f.product_sk = p.product_sk
        GROUP BY p.product_sk
        ORDER BY revenue DESC;
    """,
    "loyalty tier": """
        SELECT c.loyalty_tier, COUNT(DISTINCT c.customer_id) AS customers, SUM(f.net_revenue) AS revenue
        FROM fact_sales f
        JOIN dim_customer c ON f.customer_sk = c.customer_sk
        GROUP BY c.loyalty_tier
        ORDER BY revenue DESC;
    """,
}

def ask_warehouse(question: str) -> dict:
    q = question.lower()
    if "city" in q:
        sql = INTENT_TEMPLATES["revenue by city"]
    elif "product" in q or "sku" in q:
        sql = INTENT_TEMPLATES["top products"]
    else:
        sql = INTENT_TEMPLATES["loyalty tier"]

    result = execute_safe_query(DB_PATH, sql)
    return {"question": question, "generated_sql": sql.strip(), "execution": result}

if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        init_warehouse()
    for prompt in [
        "Show me total revenue by city",
        "Which products generated the highest revenue?",
    ]:
        out = ask_warehouse(prompt)
        print(f"\nQ: {out['question']}")
        print(f"SQL:\n{out['generated_sql']}")
        print(f"Result: {out['execution']['rows']}")
