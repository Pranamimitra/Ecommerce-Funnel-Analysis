CREATE DATABASE FUNNELANALYSIS;

-- Total row count that made it in
SELECT COUNT(*) AS total_rows FROM Events;

-- Check how many price values are actually missing/null
SELECT COUNT(*) AS missing_price
FROM Events
WHERE price IS NULL;

--event type count
SELECT event_type, COUNT(*) AS cnt
FROM Events
GROUP BY event_type

--build the funnel at session grain
SELECT 
	user_session,
	MAX(CASE WHEN event_type = 'view' THEN 1 ELSE 0 END) AS reached_view,
	MAX(CASE WHEN event_type = 'cart' THEN 1 ELSE 0 END) AS reached_cart,
	MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS reached_purchase
INTO session_funnel
FROM Events
WHERE user_session IS NOT NULL
GROUP BY user_session

--checking the actual funnel
SELECT 
	sessions_viewed,
	sessions_carted,
	sessions_purchased,
	CAST(196304 AS FLOAT) * 100 / 912885 AS view_to_cart_rate, --21%
    CAST(32385 AS FLOAT) * 100 / 196304 AS cart_to_purchase_rate, --16%
    CAST(32385 AS FLOAT) * 100/ 912885 AS view_to_purchase_rate --0.03%
FROM (
	SELECT
		SUM(reached_view) AS sessions_viewed,
		SUM(reached_view) - SUM(reached_cart) AS view_to_cart_drop_off,
		SUM(reached_cart) AS sessions_carted,
		SUM(reached_cart) - SUM(reached_purchase) AS cart_to_purchase_drop_off,
		SUM(reached_purchase) AS sessions_purchased,
		SUM(reached_view) - SUM(reached_purchase) AS view_to_purchase_drop_off
	FROM session_funnel
)t;

SELECT TOP 50 *
FROM session_funnel
 
--creating a new column for the datetime ommiting the UTC (preparing the table for further analysis)
SELECT 
	TOP 5 *
FROM Events

ALTER TABLE events ADD event_time_clean datetime2;

UPDATE Events
SET event_time_clean = TRY_CONVERT(datetime2, REPLACE(event_time, ' UTC', ''))

SELECT
	COUNT (*) AS total_rows,
	COUNT(event_time_clean) AS converted_rows
FROM Events

--Segmenting it on the basis of day-of-week (Mon, tue, wed..)
SELECT
	DATENAME(WEEKDAY, event_time_clean) AS DAYNAME,
	COUNT(DISTINCT CASE WHEN event_type = 'view' THEN user_session END) AS sessions_viewed,
	COUNT(DISTINCT CASE WHEN event_type = 'cart' THEN user_session END) AS sessions_carted,
	COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN user_session END) AS sessions_purchased,
	CAST(
    COUNT(DISTINCT CASE WHEN event_type='cart' THEN user_session END)
    AS FLOAT
	) * 100 /
	COUNT(DISTINCT CASE WHEN event_type='view' THEN user_session END)
	AS view_to_cart_rate,
	CAST(
		COUNT(DISTINCT CASE WHEN event_type='purchase' THEN user_session END)
		AS FLOAT
	) * 100 /
	COUNT(DISTINCT CASE WHEN event_type='cart' THEN user_session END)
	AS cart_to_purchase_rate
FROM Events
WHERE event_time_clean IS NOT NULL
GROUP BY DATENAME(WEEKDAY, event_time_clean)
ORDER BY 
	CASE DATENAME(WEEKDAY, event_time_clean)
		WHEN 'Monday' THEN 1
		WHEN 'Tuesday' THEN 2
		WHEN 'Wednesday' THEN 3
		WHEN 'Thursday' THEN 4
		WHEN 'Friday' THEN 5
		WHEN 'Saturday' THEN 6
		WHEN 'Sunday' THEN 7
	END


--Segmenting it on the basis of category
SELECT TOP 15
	category_code,
	COUNT(DISTINCT CASE WHEN event_type = 'view' THEN user_session END) AS sessions_viewed,
	COUNT(DISTINCT CASE WHEN event_type = 'cart' THEN user_session END) AS sessions_carted,
	COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN user_session END) AS sessions_purchased
FROM Events
WHERE category_code IS NOT NULL
GROUP BY category_code
ORDER BY sessions_viewed DESC
