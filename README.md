# Guarded Text-to-SQL Retail Warehouse Agent

A lightweight, read-only natural-language-to-SQL analytical agent built over a SQLite Star Schema retail data warehouse, protected by AST + regex SQL validation guardrails and automated GitHub Actions CI.

## Star Schema Architecture (`retail_star_warehouse.db`)
- **`fact_sales` (Fact Table):** `order_id`, `customer_sk` (FK), `product_sk` (FK), `order_date`, `quantity`, `net_revenue`
- **`dim_customer` (Dimension):** `customer_sk` (PK), `customer_name`, `city`, `segment`
- **`dim_product` (Dimension):** `product_sk` (PK), `product_name`, `category`, `unit_price`

## Multi-Layer SQL Guardrails (`src/sql_guardrails.py`)
1. **Single-Statement Enforcement:** Blocks stacked/multi-statement SQL injection payloads (`;` chaining).
2. **AST & Keyword Validation:** Enforces strictly read-only `SELECT` queries while blocking `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE`, and `ATTACH`.
3. **Schema-Grounded Execution:** Resolves KPI questions into multi-table `JOIN` queries against the Star Schema warehouse.

## Quickstart & Live Cloud Verification

    pip install -r requirements.txt
    python3 src/warehouse_setup.py
    python3 src/agent.py
    pytest -q
