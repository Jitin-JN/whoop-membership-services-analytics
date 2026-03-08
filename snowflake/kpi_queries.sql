USE WAREHOUSE WH_WHOOP_ANALYTICS;
USE DATABASE WHOOP_PORTFOLIO;
USE SCHEMA ANALYTICS;

-- KPI 1: overall support KPIs
SELECT
  COUNT(*) AS total_tickets,
  AVG(CSAT_SCORE) AS avg_csat,
  AVG(FIRST_CONTACT_RESOLUTION) AS fcr_rate,
  AVG(REPEAT_CONTACT_FLAG) AS repeat_contact_rate,
  AVG(ESCALATED) AS escalation_rate,
  AVG(RESOLUTION_TIME_HOURS) AS avg_resolution_time_hours
FROM V_TICKETS_ENRICHED;

-- KPI 2: top contact drivers
SELECT
  ISSUE_CATEGORY,
  COUNT(*) AS ticket_count,
  AVG(CSAT_SCORE) AS avg_csat,
  AVG(REPEAT_CONTACT_FLAG) AS repeat_rate,
  AVG(ESCALATED) AS escalation_rate,
  AVG(RESOLUTION_TIME_HOURS) AS avg_resolution_time_hours
FROM V_TICKETS_ENRICHED
GROUP BY 1
ORDER BY ticket_count DESC;

-- KPI 3: trends by month
SELECT
  DATE_TRUNC('month', CONTACT_DATE) AS month,
  COUNT(*) AS ticket_count,
  AVG(CSAT_SCORE) AS avg_csat,
  AVG(REPEAT_CONTACT_FLAG) AS repeat_rate,
  AVG(FIRST_CONTACT_RESOLUTION) AS fcr_rate
FROM V_TICKETS_ENRICHED
GROUP BY 1
ORDER BY 1;

-- KPI 4: churn by plan
SELECT
  MEMBERSHIP_PLAN,
  COUNT(*) AS members,
  AVG(CHURN_FLAG) AS churn_rate,
  AVG(TOTAL_TICKETS) AS avg_tickets_per_member,
  AVG(AVG_CSAT) AS avg_member_csat,
  AVG(TOTAL_REPEAT_CONTACTS) AS avg_repeat_contacts
FROM V_MEMBER_ANALYTICS
GROUP BY 1
ORDER BY churn_rate DESC;

-- KPI 5: churn by support pain (repeat contacts bucket)
SELECT
  CASE
    WHEN TOTAL_REPEAT_CONTACTS = 0 THEN '0'
    WHEN TOTAL_REPEAT_CONTACTS = 1 THEN '1'
    WHEN TOTAL_REPEAT_CONTACTS = 2 THEN '2'
    ELSE '3+'
  END AS repeat_bucket,
  COUNT(*) AS members,
  AVG(CHURN_FLAG) AS churn_rate,
  AVG(AVG_CSAT) AS avg_csat
FROM V_MEMBER_ANALYTICS
GROUP BY 1
ORDER BY repeat_bucket;