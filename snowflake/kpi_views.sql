USE WAREHOUSE WH_WHOOP_ANALYTICS;
USE DATABASE WHOOP_PORTFOLIO;
USE SCHEMA ANALYTICS;

-- ------------------------------------------------------------
-- 1) Overall Support KPI
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW KPI_SUPPORT_OVERALL AS
SELECT
  COUNT(*) AS total_tickets,
  AVG(CSAT_SCORE) AS avg_csat,
  AVG(FIRST_CONTACT_RESOLUTION) AS fcr_rate,
  AVG(REPEAT_CONTACT_FLAG) AS repeat_contact_rate,
  AVG(ESCALATED) AS escalation_rate,
  AVG(RESOLUTION_TIME_HOURS) AS avg_resolution_time_hours
FROM V_TICKETS_ENRICHED;

-- ------------------------------------------------------------
-- 2) Monthly trend
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW KPI_SUPPORT_MONTHLY AS
SELECT
  DATE_TRUNC('month', CONTACT_DATE) AS month,
  COUNT(*) AS ticket_count,
  AVG(CSAT_SCORE) AS avg_csat,
  AVG(FIRST_CONTACT_RESOLUTION) AS fcr_rate,
  AVG(REPEAT_CONTACT_FLAG) AS repeat_contact_rate,
  AVG(ESCALATED) AS escalation_rate,
  AVG(RESOLUTION_TIME_HOURS) AS avg_resolution_time_hours
FROM V_TICKETS_ENRICHED
GROUP BY 1
ORDER BY 1;

-- ------------------------------------------------------------
-- 3) Root cause table: KPIs by Issue Category
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW KPI_SUPPORT_BY_ISSUE AS
SELECT
  ISSUE_CATEGORY,
  COUNT(*) AS ticket_count,
  AVG(CSAT_SCORE) AS avg_csat,
  AVG(FIRST_CONTACT_RESOLUTION) AS fcr_rate,
  AVG(REPEAT_CONTACT_FLAG) AS repeat_contact_rate,
  AVG(ESCALATED) AS escalation_rate,
  AVG(RESOLUTION_TIME_HOURS) AS avg_resolution_time_hours
FROM V_TICKETS_ENRICHED
GROUP BY 1
ORDER BY ticket_count DESC;

-- ------------------------------------------------------------
-- 4) KPIs by Channel
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW KPI_SUPPORT_BY_CHANNEL AS
SELECT
  CHANNEL,
  COUNT(*) AS ticket_count,
  AVG(CSAT_SCORE) AS avg_csat,
  AVG(FIRST_CONTACT_RESOLUTION) AS fcr_rate,
  AVG(REPEAT_CONTACT_FLAG) AS repeat_contact_rate,
  AVG(ESCALATED) AS escalation_rate,
  AVG(RESOLUTION_TIME_HOURS) AS avg_resolution_time_hours
FROM V_TICKETS_ENRICHED
GROUP BY 1
ORDER BY ticket_count DESC;

-- ------------------------------------------------------------
-- 5) Churn by Membership Plan
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW KPI_CHURN_BY_PLAN AS
SELECT
  MEMBERSHIP_PLAN,
  COUNT(*) AS members,
  AVG(CHURN_FLAG) AS churn_rate,
  AVG(TOTAL_TICKETS) AS avg_tickets_per_member,
  AVG(AVG_CSAT) AS avg_member_csat,
  AVG(TOTAL_REPEAT_CONTACTS) AS avg_repeat_contacts,
  AVG(TOTAL_ESCALATIONS) AS avg_escalations
FROM V_MEMBER_ANALYTICS
GROUP BY 1
ORDER BY churn_rate DESC;

-- ------------------------------------------------------------
-- 6) Churn by Repeat Contact Bucket
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW KPI_CHURN_BY_REPEAT_BUCKET AS
SELECT
  CASE
    WHEN TOTAL_REPEAT_CONTACTS = 0 THEN '0'
    WHEN TOTAL_REPEAT_CONTACTS = 1 THEN '1'
    WHEN TOTAL_REPEAT_CONTACTS = 2 THEN '2'
    ELSE '3+'
  END AS repeat_bucket,
  COUNT(*) AS members,
  AVG(CHURN_FLAG) AS churn_rate,
  AVG(AVG_CSAT) AS avg_member_csat,
  AVG(TOTAL_TICKETS) AS avg_tickets_per_member
FROM V_MEMBER_ANALYTICS
GROUP BY 1
ORDER BY
  CASE repeat_bucket
    WHEN '0' THEN 0
    WHEN '1' THEN 1
    WHEN '2' THEN 2
    ELSE 3
  END;

-- ------------------------------------------------------------
-- 7) Churn by CSAT Bucket
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW KPI_CHURN_BY_CSAT_BUCKET AS
SELECT
  CASE
    WHEN AVG_CSAT >= 4.5 THEN 'High (>=4.5)'
    WHEN AVG_CSAT >= 3.5 THEN 'Medium (3.5-4.49)'
    ELSE 'Low (<3.5)'
  END AS csat_bucket,
  COUNT(*) AS members,
  AVG(CHURN_FLAG) AS churn_rate,
  AVG(TOTAL_REPEAT_CONTACTS) AS avg_repeat_contacts,
  AVG(TOTAL_ESCALATIONS) AS avg_escalations
FROM V_MEMBER_ANALYTICS
GROUP BY 1
ORDER BY
  CASE csat_bucket
    WHEN 'High (>=4.5)' THEN 0
    WHEN 'Medium (3.5-4.49)' THEN 1
    ELSE 2
  END;