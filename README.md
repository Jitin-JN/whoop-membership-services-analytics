# Improving Member Experience Through Support Analytics

### A WHOOP-Inspired Membership Services Analytics Case Study

---

# Overview

This project analyzes **support operations and member experience** for a subscription-based wearable fitness platform inspired by WHOOP.

The objective is to understand how **customer support interactions impact member satisfaction and churn**, identify the **primary drivers of support demand** and uncover **operational opportunities to improve the member experience**.

The analysis simulates the work of a **Business / Product Analyst within a Membership Services organization**, using data to support operational decision-making.

---

# Business Problem

Subscription fitness platforms rely heavily on **member retention**. Poor support experiences—such as slow resolution times, repeated contacts or unresolved technical issues can negatively impact the overall member experience and increase churn.

This project investigates four key questions:

* What are the **primary drivers of support tickets**?
* Which issues create **repeat contacts and escalations**?
* How does **support experience affect member churn**?
* What operational improvements could **reduce support demand and improve retention**?

---

# Dataset Overview

The dataset was **synthetically generated** to simulate a realistic support operations environment.

| Metric           | Value                  |
| ---------------- | ---------------------- |
| Total Members    | 200,000+               |
| Support Tickets  | 10,000                 |
| Membership Plans | Trial, One, Peak, Life |
| Countries        | US, UK, CA, AU         |

### Support Ticket Data

Each ticket contains:

* Issue category
* Resolution time
* First contact resolution
* Repeat contact flag
* Escalation flag
* CSAT score

### Member-Level Data

Each member record includes:

* Member tenure
* Support interaction history
* Average CSAT score
* Repeat contact count
* Churn flag

---

# Tech Stack

| Layer           | Technology             |
| --------------- | ---------------------- |
| Data Generation | Python (Pandas, NumPy) |
| Data Warehouse  | Snowflake              |
| Data Modeling   | SQL                    |
| Visualization   | Power BI               |

---

# Data Architecture

```
Synthetic Data Generation (Python)
        ↓
Snowflake Data Warehouse
        ↓
SQL Analytics Models / KPI Views
        ↓
Power BI Dashboard
```

---

# Key Support Metrics

| Metric                   | Value      |
| ------------------------ | ---------- |
| Average CSAT             | 4.40       |
| First Contact Resolution | 82.9%      |
| Repeat Contact Rate      | 17.1%      |
| Escalation Rate          | 20.8%      |
| Avg Resolution Time      | 30.2 hours |

Overall support performance is strong, but a subset of **technical issues creates operational inefficiencies**.

---

# Major Support Drivers

Support demand is concentrated in a few key categories.

| Issue Category | Ticket Volume |
| -------------- | ------------- |
| Battery Drain  | ~2,000        |
| Sync Issues    | ~1,800        |
| Billing        | ~1,500        |
| App Bugs       | ~1,475        |

Battery and connectivity issues alone account for **~38% of all support tickets**.

These categories also have the **highest escalation rates and longest resolution times**.

---

# Root Cause Analysis

Some issue types are significantly harder to resolve.

| Issue         | Repeat Rate | Escalation Rate | Resolution Time |
| ------------- | ----------- | --------------- | --------------- |
| App Bugs      | 25.6%       | 28.1%           | 42 hrs          |
| Sync Issues   | 23.4%       | 27.7%           | 38 hrs          |
| Battery Drain | 16.6%       | 30.2%           | 50 hrs          |

These issues frequently require **multiple interactions and engineering escalation**, suggesting that the root cause lies in **product reliability rather than support workflow inefficiencies**.

---

# Impact on Member Retention

Support experience strongly correlates with **member churn risk**.

### Key Insights

* **Trial members show the highest churn rate (22.7%)**
* Members with **multiple repeat contacts churn significantly more often**
* **Resolution times above 48 hours** correlate with the highest churn
* **Lower CSAT scores strongly predict churn**

Overall churn rate in the simulated dataset: **11.4%**

---

# Operational Improvement Opportunities

## 1. Improve Device Reliability

Battery and connectivity issues drive the largest share of support tickets.

Improving **firmware stability and device diagnostics** could significantly reduce ticket volume.

---

## 2. Improve App Bug Resolution

App bugs generate the highest **repeat contact rates**.

Better **debugging tools, monitoring, and faster release cycles** could reduce repeated support interactions.

---

## 3. Reduce Resolution Time

Tickets exceeding **48 hours** show significantly higher churn.

Improving **internal escalation workflows and engineering response times** could improve retention.

---

## 4. Improve Trial Member Onboarding

Trial members show the highest churn risk.

Improving **onboarding education and product guidance** could reduce early frustration.

---

# Estimated Operational Impact

If repeat contacts were reduced from **17% → 12%**, the projected operational impact would be:

| Metric                   | Estimated Impact     |
| ------------------------ | -------------------- |
| Repeat Tickets Reduced   | ~500 per month       |
| Agent Time Saved         | ~250 hours per month |
| Operational Cost Savings | ~$6.3K per month     |
| Annual Savings           | ~$75K                |
| Retention Lift           | ~0.8%                |

---

# Power BI Dashboard

The Power BI dashboard tracks:

* Support ticket volume by issue type
* Resolution time distribution
* Escalation and repeat contact rates
* CSAT performance
* Churn risk segmentation
and more.
![Dashboard_report_1](https://github.com/user-attachments/assets/c90ada37-c034-484d-ac5f-53058800ffc5)

![Dashboard_report_2](https://github.com/user-attachments/assets/bfbe2886-a23d-4b14-82da-c010344897f3)

![Dashboard_report_3](https://github.com/user-attachments/assets/0dc0801d-ddf4-45de-b137-b64fefafd506)


---

# Reproducing the Project

### 1. Generate Synthetic Data

Run the Python script or notebook:

```
python data_generation.py
```

This creates the synthetic member and support ticket datasets.

### 2. Load Data into Snowflake

Upload the generated datasets into Snowflake tables.

### 3. Run SQL Analytics Models

Execute the SQL scripts to create KPI views.

### 4. Connect Power BI

Connect Power BI to Snowflake and load the analytics views.

---

# Key Takeaways

This project demonstrates how **support analytics can drive operational improvements** by:

* Identifying **root causes of support demand**
* Connecting **support experience to churn risk**
* Quantifying **cost and retention impact**
* Providing **data-driven operational recommendations**

The analysis mirrors the type of work performed by **Customer Experience, Membership Services and Product Analytics teams** in subscription-based technology companies.

---


