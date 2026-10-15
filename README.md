

# olist-delivery-logistics-dashboard
Operations analytics: on-time delivery, delay hotspots, seller/carrier performance (Power BI)


'''
https://public.tableau.com/app/profile/pallavi.dasari5644/viz/Book1_17915807794560/Lanes

https://public.tableau.com/app/profile/pallavi.dasari5644/viz/Book1_17915807794560/DelayHotspots?publish=yes

https://public.tableau.com/app/profile/pallavi.dasari5644/viz/Book1_17915807794560/Overview?publish=yes
'''

# 🚚 Delivery & Logistics Efficiency Dashboard (Olist) — Tableau

## Business Problem
Which regions and shipping lanes drive late deliveries, and how can operations improve on-time performance?

## Live Dashboard
🔗 [View on Tableau Public](PASTE-YOUR-TABLEAU-LINK)

## Key Results
- **On-time rate:** 92.3% across 95,964 delivered orders | **Avg delivery:** 12.2 days
- **Worst states:** AL (23.2% late), MA (18.5%), PI (14.9%) vs 5.7% in SP
- **Worst lane:** SP → AL (25.7% late, 21.5 transit days)
- **Time lost:** 2.8 days at seller handoff vs 9.0 days in carrier transit
- **Customer impact:** 4.29 stars on time vs 2.61 when late
- **3 recommendations:** [docs/recommendations.pdf](docs/recommendations.pdf)

## Dashboard Preview
![Overview](images/PASTE-FILENAME-overview.png)
![Hotspots](images/PASTE-FILENAME-hotspots.png)

## Tools
Python (pandas), Jupyter, Tableau Public, Git/GitHub

## Approach
1. Merged 5 Olist tables into one order-level table (`src/build_dataset.py`)
2. Cleaned data and engineered delay, handling and transit metrics
3. EDA in `notebooks/01_eda.ipynb` to find hotspots and root causes
4. Tableau dashboards with Region → State → City and Year → Month drill-downs
5. Recommendations tied to metrics

## Metric Definitions
- **On-time:** delivered date ≤ estimated date
- **Delay days:** actual − estimated delivery date
- **Seller handling:** carrier pickup − order approval
- **Carrier transit:** customer delivery − carrier pickup

## Limitations
- No carrier name in the dataset; carrier performance is proxied by seller handling, carrier transit time and shipping lane.
- Only delivered orders analysed; data covers 2016 to 2018.
- Rankings use minimum volumes (states over 200 orders, lanes over 150) to avoid small-sample distortion.

## How to Run
1. Download the Olist dataset from Kaggle into `data/raw/`
2. `pip install -r requirements.txt`
3. `python src/build_dataset.py`
4. Open the Tableau Public link above

## Author
Pallavi Dasari | [[https://www.linkedin.com/in/dasari-pallavi/?isSelfProfile=true)]]| [dasaripallavi2113@gmail.com]