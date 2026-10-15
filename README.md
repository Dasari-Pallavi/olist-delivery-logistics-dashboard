
# olist-delivery-logistics-dashboard
Operations analytics: on-time delivery, delay hotspots, seller/carrier performance (Power BI)


'''
https://public.tableau.com/app/profile/pallavi.dasari5644/viz/Book1_17915807794560/Lanes

https://public.tableau.com/app/profile/pallavi.dasari5644/viz/Book1_17915807794560/DelayHotspots?publish=yes

https://public.tableau.com/app/profile/pallavi.dasari5644/viz/Book1_17915807794560/Overview?publish=yes
'''

# Delivery Performance: Summary & Recommendations

**Scope:** [N] delivered orders, Sep 2016 to Aug 2018 | **On-time rate:** [X]% | **Average delivery time:** [Y] days

## Key Findings
- **Regional hotspots:** Late deliveries concentrate in [state 1], [state 2] and [state 3], with late rates of [X]% to [Y]%, against [Z]% in São Paulo.
- **Shipping lanes:** The worst lanes are [lane 1] ([X]% late) and [lane 2] ([Y]% late). Cross-state orders are [N] times more likely to be late than same-state orders.
- **Where time is lost:** Sellers take [A] days to hand over to the carrier, while carrier transit takes [B] days, so [carrier transit / seller handling] is the larger share.
- **Peak season:** On-time performance fell to [X]% in [month] and [Y]% in [month].
- **Customer impact:** Orders delivered 7+ days late score [A] stars on average, against [B] stars for on-time orders.

## Recommendations
**1. Reset delivery promises in high-delay regions.**
Add a [X]-day buffer to the estimated delivery date for [states]. This reduces late deliveries and the 1-2 star reviews that follow. *Metric: on-time rate by state.*

**2. Fix the worst shipping lanes.**
The top lanes ([lane 1], [lane 2], [lane 3]) drive a large share of late orders. Pilot a regional fulfilment hub or an alternative carrier on [lane 1]. *Metric: lane late %, carrier transit days.*

**3. Tighten seller handoff and plan for peak season.**
Sellers average [A] days to hand over. Set a handoff target of [Y] days, flag sellers above it, and add capacity before [peak months]. *Metric: seller handling days, monthly on-time %.*

## Expected Impact
Late orders score [gap] stars lower than on-time orders. Reducing the late rate by [X] percentage points should raise the average review score, based on this observed gap.

*Source: Olist Brazilian E-Commerce dataset (Kaggle). Carrier performance is proxied by seller handling time, carrier transit time and shipping lane, because the dataset has no carrier name.*