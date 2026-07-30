# E-commerce Conversion Funnel Analysis

## Executive Summary
Using SQL Server and Streamlit, I analyzed session-level user behavior across an e-commerce platform's purchase funnel (912,885 sessions, Jan 2020) to identify where customers drop off between viewing a product and completing a purchase. Only 3.55% of sessions that viewed a product resulted in a purchase. While the largest raw drop-off occurs between viewing and adding to cart, the more business-critical leak is cart-to-purchase conversion (16.5%) — since these are already high-intent users. I found this weak point is not constant across the week: it peaks Monday/Tuesday (~18%) and drops meaningfully from Wednesday through Sunday (~15–16%). Based on this, I recommend the business target cart-abandonment interventions specifically during the Wednesday–Sunday window.

## Business Problem
E-commerce conversion from product view to completed purchase is a core revenue driver, yet a large share of users who show purchase intent (by adding a product to cart) never complete the transaction. This project asks: **where in the funnel are users dropping off, and does that drop-off vary in a way the business could act on?**

## Methodology
1. **Data validation** — Loaded ~4.26M raw events into SQL Server; identified and handled data quality issues (39 rows with missing price values, sparse `category_code` for accessory-type products, malformed timestamps requiring cleanup).
2. **Session-level funnel construction** — Reshaped event-level data to session grain, flagging whether each session reached view, cart, and/or purchase stages.
3. **Conversion rate analysis** — Computed step-by-step conversion (view→cart, cart→purchase) at both the aggregate and rate level, distinguishing where the largest *number* of users drop off vs. where the *highest-intent* users are lost.
4. **Segmentation** — Broke down cart→purchase conversion by day of week to test whether the drop-off is uniform or concentrated in a specific window. Also explored category-level segmentation as a secondary angle.
5. **Sanity checks** — Verified segment-level counts were large enough to be reliable (thousands of sessions per day, not small-sample noise) before drawing conclusions.
6. **Dashboard** — Built an interactive Streamlit dashboard to visualize the funnel, conversion rates, and day-of-week pattern for a non-technical audience.

## Skills
- **SQL:** Session-level aggregation, conditional aggregation (`CASE WHEN` inside `COUNT(DISTINCT)`), date functions, data cleaning (type conversion, null handling)
- **Data Quality:** Identifying and documenting real-world data issues rather than ignoring them
- **Python/Streamlit:** Building an interactive dashboard with Plotly visualizations
- **Analysis:** Distinguishing absolute vs. rate-based drop-off, segmenting a metric to find an actionable pattern rather than stopping at a single headline number

## Results & Business Recommendation
- **912,885** sessions viewed a product → **196,304** added to cart (21.5%) → **32,385** completed a purchase (16.5% of carts, 3.55% overall).
- Cart-to-purchase conversion is not flat across the week — it's meaningfully stronger on **Monday (18.1%) and Tuesday (18.8%)** than **Wednesday through Sunday (15.2–16.1%)**, a relative decline of roughly 15–20%.
- **Recommendation:** Target cart-abandonment interventions (reminder emails, limited-time incentives) specifically during the Wednesday–Sunday window, where the drop-off is concentrated. Separately, investigate what differs about Monday/Tuesday shopping behavior (e.g., more planned/deliberate purchases) to see whether that pattern can be encouraged later in the week.

## Data Quality Notes
- 39 rows (out of 4.26M) had missing `price` values — excluded from price-based analysis, negligible at ~0.001% of data.
- `category_code` is frequently null for accessory-type products (by design in the source data) — category-level analysis was restricted to rows with a populated category.
- Raw timestamps included a trailing "UTC" string incompatible with SQL Server's native datetime parsing — cleaned via string replacement before conversion.

## Tech Stack
SQL Server, T-SQL, Python, Pandas, Plotly, Streamlit

## Dataset
[REES46 eCommerce Events History — Cosmetics Shop](https://www.kaggle.com/datasets/mkechinov/ecommerce-events-history-in-cosmetics-shop) (Kaggle), January 2020 subset.

## Next Steps
- Investigate the causal driver behind the Monday/Tuesday conversion strength (would require additional data, e.g., traffic source or device type)
- A/B test cart-abandonment email timing concentrated on the Wednesday–Sunday window
- Extend segmentation to category × day-of-week interaction to see if the weekly pattern holds across product types
