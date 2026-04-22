-- Retail Sales Analytics Dashboard
-- KPI and business analysis queries
-- Source table: sales_clean

-- 1. Overall KPI Summary
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT order_no) AS total_orders,
  ROUND(SUM(order_total), 2) AS total_revenue,
  ROUND(SUM(gross_profit_estimate), 2) AS total_gross_profit,
  ROUND(AVG(order_total), 2) AS avg_order_value,
  SUM(order_quantity) AS total_units_sold,
  ROUND(AVG(discount_pct_decimal), 4) AS avg_discount_pct,
  ROUND(AVG(ship_delay_days), 2) AS avg_ship_delay_days
FROM sales_clean;


-- 2. Revenue Trend by Year and Month
SELECT
  year,
  month,
  ROUND(SUM(order_total), 2) AS total_revenue,
  ROUND(SUM(gross_profit_estimate), 2) AS total_gross_profit,
  COUNT(DISTINCT order_no) AS total_orders
FROM sales_clean
GROUP BY year, month
ORDER BY year, month;


-- 3. Product Category Performance
SELECT
  product_category,
  ROUND(SUM(order_total), 2) AS total_revenue,
  ROUND(SUM(gross_profit_estimate), 2) AS total_gross_profit,
  SUM(order_quantity) AS total_units_sold,
  ROUND(AVG(discount_pct_decimal), 4) AS avg_discount_pct
FROM sales_clean
GROUP BY product_category
ORDER BY total_revenue DESC;


-- 4. State-Level Sales Performance
SELECT
  state,
  ROUND(SUM(order_total), 2) AS total_revenue,
  ROUND(SUM(gross_profit_estimate), 2) AS total_gross_profit,
  COUNT(DISTINCT order_no) AS total_orders,
  ROUND(AVG(ship_delay_days), 2) AS avg_ship_delay_days
FROM sales_clean
GROUP BY state
ORDER BY total_revenue DESC;


-- 5. Discount Band Analysis
SELECT
  discount_band,
  COUNT(*) AS line_count,
  ROUND(SUM(order_total), 2) AS total_revenue,
  ROUND(SUM(gross_profit_estimate), 2) AS total_gross_profit,
  ROUND(AVG(discount_pct_decimal), 4) AS avg_discount_pct
FROM sales_clean
GROUP BY discount_band
ORDER BY avg_discount_pct;


-- 6. Customer Type Analysis
SELECT
  customer_type,
  ROUND(SUM(order_total), 2) AS total_revenue,
  ROUND(SUM(gross_profit_estimate), 2) AS total_gross_profit,
  COUNT(DISTINCT order_no) AS total_orders,
  ROUND(AVG(order_total), 2) AS avg_order_value
FROM sales_clean
GROUP BY customer_type
ORDER BY total_revenue DESC;