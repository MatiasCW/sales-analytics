# Databricks notebook source
# MAGIC %md
# MAGIC # Data Cleaning and Transformation Summary
# MAGIC
# MAGIC ## Overview
# MAGIC The raw retail sales CSV was cleaned and transformed in Databricks to create an analysis-ready dataset for SQL reporting and Power BI dashboarding.
# MAGIC
# MAGIC ## Raw Data Issues Identified
# MAGIC The original dataset required preprocessing because:
# MAGIC
# MAGIC - several numeric fields were stored as strings
# MAGIC - currency values included `$` and `,`
# MAGIC - discount values included `%`
# MAGIC - date fields were stored as text
# MAGIC - unnecessary columns such as `Address` were not needed for analysis
# MAGIC - an extra `Total` column appeared in the raw file and was excluded from the cleaned dataset
# MAGIC
# MAGIC ## Cleaning Steps Performed
# MAGIC
# MAGIC ### 1. Loaded the raw CSV into Databricks
# MAGIC The dataset was ingested from a CSV file and converted into a Spark DataFrame for inspection and transformation.
# MAGIC
# MAGIC ### 2. Inspected schema and column structure
# MAGIC The raw schema was reviewed to identify:
# MAGIC - column names
# MAGIC - row count
# MAGIC - incorrect data types
# MAGIC - unnecessary fields
# MAGIC
# MAGIC ### 3. Selected relevant columns
# MAGIC The dataset was reduced to the columns needed for sales analysis, customer segmentation, shipping analysis, and profitability reporting.
# MAGIC
# MAGIC ### 4. Renamed columns
# MAGIC Column names were standardized to a lowercase, underscore-based format for easier SQL querying and cleaner Power BI modeling.
# MAGIC
# MAGIC Examples:
# MAGIC - `Order No` → `order_no`
# MAGIC - `Order Date` → `order_date`
# MAGIC - `Customer Name` → `customer_name`
# MAGIC - `Discount %` → `discount_pct`
# MAGIC - `Shipping Cost` → `shipping_cost`
# MAGIC
# MAGIC ### 5. Cleaned date fields
# MAGIC The `Order Date` and `Ship Date` columns were parsed from text format into proper date fields so they could be used for:
# MAGIC - time trend analysis
# MAGIC - filtering
# MAGIC - shipping delay calculations
# MAGIC
# MAGIC ### 6. Cleaned numeric fields
# MAGIC Currency and percentage symbols were removed and the following fields were converted into numeric types:
# MAGIC - `cost_price`
# MAGIC - `retail_price`
# MAGIC - `profit_margin`
# MAGIC - `order_quantity`
# MAGIC - `sub_total`
# MAGIC - `discount_pct`
# MAGIC - `discount_amt`
# MAGIC - `order_total`
# MAGIC - `shipping_cost`
# MAGIC
# MAGIC Examples:
# MAGIC - `$4,533.52` → `4533.52`
# MAGIC - `2%` → `2.0`
# MAGIC
# MAGIC ### 7. Removed problematic records
# MAGIC Rows with missing critical values such as `order_quantity` were filtered out to ensure calculations remained consistent.
# MAGIC
# MAGIC ## New Derived Columns Created
# MAGIC
# MAGIC ### Time-based features
# MAGIC - `year` — extracted from `order_date`
# MAGIC - `month` — extracted from `order_date`
# MAGIC - `quarter` — extracted from `order_date`
# MAGIC
# MAGIC These fields support monthly, quarterly, and yearly trend analysis.
# MAGIC
# MAGIC ### Shipping feature
# MAGIC - `ship_delay_days` — calculated as the difference between `ship_date` and `order_date`
# MAGIC
# MAGIC This measures the time taken to ship an order.
# MAGIC
# MAGIC ### Margin and profit features
# MAGIC - `unit_margin` — calculated as `retail_price - cost_price`
# MAGIC - `gross_profit_estimate` — calculated as `unit_margin * order_quantity`
# MAGIC
# MAGIC These fields help estimate profitability at the order-line level.
# MAGIC
# MAGIC ### Discount features
# MAGIC - `discount_pct_decimal` — calculated as `discount_pct / 100`
# MAGIC - `discount_band` — grouped discount levels into:
# MAGIC   - `No Discount`
# MAGIC   - `Low`
# MAGIC   - `Medium`
# MAGIC   - `High`
# MAGIC
# MAGIC These fields support discount impact analysis and profitability comparisons.
# MAGIC
# MAGIC ## Final Output
# MAGIC The cleaned and enriched dataset was saved as `sales_clean` and used for:
# MAGIC - SQL-based KPI analysis
# MAGIC - trend reporting
# MAGIC - product and regional analysis
# MAGIC - Power BI dashboard development

# COMMAND ----------

display(spark.table("sales_clean"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Overall KPI Summary
# MAGIC Calculates high-level business metrics including revenue, estimated gross profit, total orders, units sold, average discount, and average shipping delay.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   COUNT(*) AS total_rows,
# MAGIC   COUNT(DISTINCT order_no) AS total_orders,
# MAGIC   ROUND(SUM(order_total), 2) AS total_revenue,
# MAGIC   ROUND(SUM(gross_profit_estimate), 2) AS total_gross_profit,
# MAGIC   ROUND(AVG(order_total), 2) AS avg_order_value,
# MAGIC   SUM(order_quantity) AS total_units_sold,
# MAGIC   ROUND(AVG(discount_pct_decimal), 4) AS avg_discount_pct,
# MAGIC   ROUND(AVG(ship_delay_days), 2) AS avg_ship_delay_days
# MAGIC FROM sales_clean;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Revenue Trend by Year and Month
# MAGIC Aggregates revenue, estimated gross profit, and order volume over time to support monthly sales trend analysis.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   year,
# MAGIC   month,
# MAGIC   ROUND(SUM(order_total), 2) AS total_revenue,
# MAGIC   ROUND(SUM(gross_profit_estimate), 2) AS total_gross_profit,
# MAGIC   COUNT(DISTINCT order_no) AS total_orders
# MAGIC FROM sales_clean
# MAGIC GROUP BY year, month
# MAGIC ORDER BY year, month;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Product Category Performance
# MAGIC Evaluates product categories by revenue, estimated gross profit, units sold, and average discount level.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   product_category,
# MAGIC   ROUND(SUM(order_total), 2) AS total_revenue,
# MAGIC   ROUND(SUM(gross_profit_estimate), 2) AS total_gross_profit,
# MAGIC   SUM(order_quantity) AS total_units_sold,
# MAGIC   ROUND(AVG(discount_pct_decimal), 4) AS avg_discount_pct
# MAGIC FROM sales_clean
# MAGIC GROUP BY product_category
# MAGIC ORDER BY total_revenue DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC ## State-Level Sales Performance
# MAGIC Compares state-level revenue, estimated gross profit, order volume, and average shipping delay.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   state,
# MAGIC   ROUND(SUM(order_total), 2) AS total_revenue,
# MAGIC   ROUND(SUM(gross_profit_estimate), 2) AS total_gross_profit,
# MAGIC   COUNT(DISTINCT order_no) AS total_orders,
# MAGIC   ROUND(AVG(ship_delay_days), 2) AS avg_ship_delay_days
# MAGIC FROM sales_clean
# MAGIC GROUP BY state
# MAGIC ORDER BY total_revenue DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Discount Band Analysis
# MAGIC Measures how different discount levels affect revenue, estimated gross profit, and average discount rate.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   discount_band,
# MAGIC   COUNT(*) AS line_count,
# MAGIC   ROUND(SUM(order_total), 2) AS total_revenue,
# MAGIC   ROUND(SUM(gross_profit_estimate), 2) AS total_gross_profit,
# MAGIC   ROUND(AVG(discount_pct_decimal), 4) AS avg_discount_pct
# MAGIC FROM sales_clean
# MAGIC GROUP BY discount_band
# MAGIC ORDER BY avg_discount_pct;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Customer Type Analysis
# MAGIC Compares customer segments using revenue, estimated gross profit, total orders, and average order value.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   customer_type,
# MAGIC   ROUND(SUM(order_total), 2) AS total_revenue,
# MAGIC   ROUND(SUM(gross_profit_estimate), 2) AS total_gross_profit,
# MAGIC   COUNT(DISTINCT order_no) AS total_orders,
# MAGIC   ROUND(AVG(order_total), 2) AS avg_order_value
# MAGIC FROM sales_clean
# MAGIC GROUP BY customer_type
# MAGIC ORDER BY total_revenue DESC;