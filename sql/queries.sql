SELECT scheme_name, aum_crore
FROM fact_performance
ORDER BY aum_crore DESC
LIMIT 5;

SELECT ROUND(AVG(nav),2) AS average_nav
FROM fact_nav;

SELECT state,
COUNT(*) AS total_transactions
FROM fact_transactions
GROUP BY state
ORDER BY total_transactions DESC;

SELECT scheme_name, expense_ratio_pct
FROM fact_performance
WHERE expense_ratio_pct < 1
ORDER BY expense_ratio_pct;

SELECT transaction_type,
COUNT(*) total_count
FROM fact_transactions
GROUP BY transaction_type;

SELECT scheme_name, sharpe_ratio
FROM fact_performance
ORDER BY sharpe_ratio DESC
LIMIT 5;

SELECT scheme_name, return_5yr
FROM fact_performance
ORDER BY return_5yr DESC
LIMIT 10;

SELECT ROUND(AVG(amount_inr),2)
AS avg_amount
FROM fact_transactions;

SELECT risk_category,
COUNT(*) total_funds
FROM dim_fund
GROUP BY risk_category;

