import pandas as pd
from pathlib import Path

RAW, OUT = Path("data/raw"), Path("data/processed")
OUT.mkdir(parents=True, exist_ok=True)

# ---------- Load ----------
date_cols = ["order_purchase_timestamp", "order_approved_at",
             "order_delivered_carrier_date", "order_delivered_customer_date",
             "order_estimated_delivery_date"]
orders = pd.read_csv(RAW / "olist_orders_dataset.csv", parse_dates=date_cols)
items = pd.read_csv(RAW / "olist_order_items_dataset.csv")
customers = pd.read_csv(RAW / "olist_customers_dataset.csv")
sellers = pd.read_csv(RAW / "olist_sellers_dataset.csv")
reviews = pd.read_csv(RAW / "olist_order_reviews_dataset.csv")

# ---------- One row per order ----------
items_agg = (items.groupby("order_id")
             .agg(seller_id=("seller_id", "first"),
                  n_items=("order_item_id", "count"),
                  order_value=("price", "sum"),
                  freight_value=("freight_value", "sum"))
             .reset_index())
reviews_agg = reviews.groupby("order_id")["review_score"].mean().reset_index()

# ---------- Merge ----------
df = (orders
      .merge(customers[["customer_id", "customer_city", "customer_state"]], on="customer_id", how="left")
      .merge(items_agg, on="order_id", how="left")
      .merge(sellers[["seller_id", "seller_city", "seller_state"]], on="seller_id", how="left")
      .merge(reviews_agg, on="order_id", how="left"))

# ---------- Clean ----------
df = df[(df["order_status"] == "delivered") &
        df["order_delivered_customer_date"].notna()].copy()
df = df[df["order_delivered_customer_date"] >= df["order_purchase_timestamp"]]
df = df[(df["order_delivered_carrier_date"].isna()) |
        (df["order_delivered_carrier_date"] <= df["order_delivered_customer_date"])]
df["customer_city"] = df["customer_city"].str.title().str.strip()

# ---------- Feature engineering ----------
d = lambda a, b: (df[a] - df[b]).dt.total_seconds() / 86400

df["delivery_days"]        = d("order_delivered_customer_date", "order_purchase_timestamp")
df["estimated_days"]       = d("order_estimated_delivery_date", "order_purchase_timestamp")
df["delay_days"]           = d("order_delivered_customer_date", "order_estimated_delivery_date")  # >0 = late
df["is_late"]              = (df["delay_days"] > 0).astype(int)
df["on_time"]              = 1 - df["is_late"]
df["seller_handling_days"] = d("order_delivered_carrier_date", "order_approved_at")
df["carrier_transit_days"] = d("order_delivered_customer_date", "order_delivered_carrier_date")

# Time fields
df["order_date"]    = df["order_purchase_timestamp"].dt.date
df["order_year"]    = df["order_purchase_timestamp"].dt.year
df["order_month"]   = df["order_purchase_timestamp"].dt.to_period("M").astype(str)
df["order_quarter"] = df["order_purchase_timestamp"].dt.to_period("Q").astype(str)
df["weekday"]       = df["order_purchase_timestamp"].dt.day_name()

# Regions
region_map = {
 **dict.fromkeys(["AC","AM","AP","PA","RO","RR","TO"], "North"),
 **dict.fromkeys(["AL","BA","CE","MA","PB","PE","PI","RN","SE"], "Northeast"),
 **dict.fromkeys(["DF","GO","MT","MS"], "Central-West"),
 **dict.fromkeys(["ES","MG","RJ","SP"], "Southeast"),
 **dict.fromkeys(["PR","RS","SC"], "South")}
df["customer_region"] = df["customer_state"].map(region_map)
df["seller_region"]   = df["seller_state"].map(region_map)

# Full state names (Tableau maps these reliably) + country
state_names = {
 "AC":"Acre","AL":"Alagoas","AM":"Amazonas","AP":"Amapá","BA":"Bahia","CE":"Ceará",
 "DF":"Distrito Federal","ES":"Espírito Santo","GO":"Goiás","MA":"Maranhão",
 "MG":"Minas Gerais","MS":"Mato Grosso do Sul","MT":"Mato Grosso","PA":"Pará",
 "PB":"Paraíba","PE":"Pernambuco","PI":"Piauí","PR":"Paraná","RJ":"Rio de Janeiro",
 "RN":"Rio Grande do Norte","RO":"Rondônia","RR":"Roraima","RS":"Rio Grande do Sul",
 "SC":"Santa Catarina","SE":"Sergipe","SP":"São Paulo","TO":"Tocantins"}
df["customer_state_name"] = df["customer_state"].map(state_names)
df["country"] = "Brazil"

# Shipping lane (carrier proxy)
df["lane"] = df["seller_state"] + " → " + df["customer_state"]
df["same_state"] = (df["seller_state"] == df["customer_state"]).astype(int)

# Lateness severity
df["delay_bucket"] = pd.cut(df["delay_days"], [-999, 0, 3, 7, 999],
                            labels=["On time", "1-3 days late", "4-7 days late", "7+ days late"])

# Drop extreme outliers (top 0.5%)
cap = df["delivery_days"].quantile(0.995)
df = df[df["delivery_days"] <= cap]

df.to_csv(OUT / "delivery_master.csv", index=False, encoding="utf-8-sig")
print(f"Saved {len(df):,} rows | On-time rate: {df['on_time'].mean():.1%}")