import numpy as np
import pandas as pd

from .config import Config

def _clip_int(x, low, high):
    return int(np.clip(round(x), low, high))

def generate_members(cfg: Config) -> pd.DataFrame:
    rng = np.random.default_rng(cfg.seed)

    member_ids = np.arange(1, cfg.n_members + 1)

    signup_dates = pd.to_datetime(
        rng.choice(pd.date_range(cfg.signup_start, cfg.signup_end), cfg.n_members)
    )

    # WHOOP-style plans: Trial + paid tiers
    membership_plan = rng.choice(
        ["TRIAL_1M", "ONE", "PEAK", "LIFE"],
        size=cfg.n_members,
        p=[0.22, 0.45, 0.25, 0.08]
    )

    device_version = rng.choice(["4.0", "5.0"], size=cfg.n_members, p=[0.55, 0.45])

    primary_goal = rng.choice(
        ["Performance", "Recovery", "Sleep Optimization"],
        size=cfg.n_members,
        p=[0.55, 0.25, 0.20]
    )

    country = rng.choice(["US", "UK", "CA", "AU"], size=cfg.n_members, p=[0.60, 0.15, 0.15, 0.10])

    today = pd.to_datetime(cfg.today)
    tenure_days = (today - signup_dates).days.astype(int)

    members = pd.DataFrame({
        "member_id": member_ids,
        "signup_date": signup_dates,
        "membership_plan": membership_plan,
        "device_version": device_version,
        "primary_goal": primary_goal,
        "country": country,
        "tenure_days": tenure_days
    })

    return members

def generate_tickets(cfg: Config, members: pd.DataFrame) -> pd.DataFrame:
    rng = np.random.default_rng(cfg.seed + 1)

    issue_categories = [
        "Battery Drain",
        "Sync Issues",
        "Strap Replacement",
        "App Bug",
        "Billing",
        "Shipping Delay",
        "Onboarding/Setup"
    ]

    member_ids = members["member_id"].to_numpy()

    ticket_member_ids = rng.choice(member_ids, cfg.n_tickets)

    contact_dates = pd.to_datetime(
        rng.choice(pd.date_range(cfg.ticket_start, cfg.ticket_end), cfg.n_tickets)
    )

    channels = rng.choice(["Chat", "Email", "Phone"], cfg.n_tickets, p=[0.52, 0.30, 0.18])

    # Base distribution
    issues = rng.choice(
        issue_categories,
        cfg.n_tickets,
        p=[0.20, 0.18, 0.14, 0.14, 0.16, 0.08, 0.10]
    )

    # Resolution time logic (hours)
    def resolution_time(issue):
        if issue == "Battery Drain":
            return rng.normal(50, 12)
        if issue == "Sync Issues":
            return rng.normal(38, 10)
        if issue == "App Bug":
            return rng.normal(42, 15)
        if issue == "Billing":
            return rng.normal(18, 6)
        if issue == "Shipping Delay":
            return rng.normal(24, 8)
        if issue == "Strap Replacement":
            return rng.normal(12, 4)
        if issue == "Onboarding/Setup":
            return rng.normal(10, 4)
        return rng.normal(20, 8)

    resolution_times = np.array([max(1, float(resolution_time(i))) for i in issues])

    # Escalation probability by issue
    def escalated(issue):
        if issue in ["Battery Drain", "App Bug", "Sync Issues"]:
            return rng.choice([0, 1], p=[0.72, 0.28])
        if issue in ["Billing"]:
            return rng.choice([0, 1], p=[0.85, 0.15])
        return rng.choice([0, 1], p=[0.90, 0.10])

    escalations = np.array([int(escalated(i)) for i in issues])

    # CSAT influenced by resolution time + escalations
    csat_scores = []
    for rt, esc in zip(resolution_times, escalations):
        base = 5.0
        if rt > 48:
            base -= 1.0
        if rt > 72:
            base -= 0.5
        if esc == 1:
            base -= 1.0
        score = np.clip(rng.normal(base, 0.8), 1, 5)
        csat_scores.append(_clip_int(score, 1, 5))
    csat_scores = np.array(csat_scores)

    # Repeat contact probability influenced by issue + rt + csat
    repeat_flags = []
    for issue, rt, csat in zip(issues, resolution_times, csat_scores):
        prob = 0.06
        if issue in ["Sync Issues", "Billing", "App Bug"]:
            prob += 0.14
        if rt > 48:
            prob += 0.10
        if csat <= 3:
            prob += 0.10
        repeat_flags.append(int(rng.choice([0, 1], p=[1 - prob, prob])))
    repeat_flags = np.array(repeat_flags)

    fcr = 1 - repeat_flags

    tickets = pd.DataFrame({
        "ticket_id": np.arange(1, cfg.n_tickets + 1),
        "member_id": ticket_member_ids,
        "contact_date": contact_dates,
        "channel": channels,
        "issue_category": issues,
        "resolution_time_hours": resolution_times.round(1),
        "first_contact_resolution": fcr,
        "escalated": escalations,
        "csat_score": csat_scores,
        "repeat_contact_flag": repeat_flags
    })

    return tickets

def build_member_support_summary(tickets: pd.DataFrame) -> pd.DataFrame:
    member_support = tickets.groupby("member_id").agg(
        total_tickets=("ticket_id", "count"),
        avg_csat=("csat_score", "mean"),
        total_repeat_contacts=("repeat_contact_flag", "sum"),
        total_escalations=("escalated", "sum"),
        avg_resolution_time=("resolution_time_hours", "mean"),
    ).reset_index()

    # Fill for members with no tickets later after merge
    return member_support

def generate_churn(cfg: Config, members: pd.DataFrame, member_support: pd.DataFrame) -> pd.DataFrame:
    rng = np.random.default_rng(cfg.seed + 2)

    df = members.merge(member_support, on="member_id", how="left")

    # Members with no tickets get neutral values
    df["total_tickets"] = df["total_tickets"].fillna(0).astype(int)
    df["avg_csat"] = df["avg_csat"].fillna(4.6)
    df["total_repeat_contacts"] = df["total_repeat_contacts"].fillna(0).astype(int)
    df["total_escalations"] = df["total_escalations"].fillna(0).astype(int)
    df["avg_resolution_time"] = df["avg_resolution_time"].fillna(12.0)

    # Base churn probability by plan (TRIAL highest, LIFE lowest)
    plan_base = {
        "TRIAL_1M": 0.22,
        "ONE": 0.08,
        "PEAK": 0.07,
        "LIFE": 0.03
    }
    base = df["membership_plan"].map(plan_base).astype(float)

    # Add risk based on support experience
    risk = base.copy()

    # Repeat contacts strongly increase churn
    risk += 0.03 * df["total_repeat_contacts"].clip(0, 5)

    # Escalations increase churn
    risk += 0.02 * df["total_escalations"].clip(0, 5)

    # Low CSAT increases churn
    risk += np.where(df["avg_csat"] < 4.0, 0.04, 0.0)
    risk += np.where(df["avg_csat"] < 3.0, 0.06, 0.0)

    # Longer resolution time increases churn slightly
    risk += np.where(df["avg_resolution_time"] > 36, 0.03, 0.0)

    # Early tenure churn is more likely (esp. trials)
    risk += np.where(df["tenure_days"] < 60, 0.05, 0.0)

    # Device 4.0 slightly higher churn (older hardware)
    risk += np.where(df["device_version"] == "4.0", 0.01, 0.0)

    # Clamp probability
    risk = risk.clip(0.01, 0.60)

    churn_flag = (rng.random(len(df)) < risk).astype(int)

    # churn_date: random date after last ticket or within ticket range (simple simulation)
    churn_dates = []
    for cf in churn_flag:
        if cf == 0:
            churn_dates.append(pd.NaT)
        else:
            churn_dates.append(
                pd.to_datetime(rng.choice(pd.date_range("2024-06-01", "2025-01-01")))
            )

    df["churn_flag"] = churn_flag
    df["churn_date"] = pd.to_datetime(churn_dates)

    return df

def main():
    cfg = Config()
    members = generate_members(cfg)
    tickets = generate_tickets(cfg, members)
    member_support = build_member_support_summary(tickets)
    members_enriched = generate_churn(cfg, members, member_support)

    out_dir = "data/generated"
    import os
    os.makedirs(out_dir, exist_ok=True)

    members_enriched.to_csv(f"{out_dir}/members.csv", index=False)
    tickets.to_csv(f"{out_dir}/tickets.csv", index=False)
    member_support.to_csv(f"{out_dir}/member_support_summary.csv", index=False)

    print("Saved:")
    print(f"- {out_dir}/members.csv")
    print(f"- {out_dir}/tickets.csv")
    print(f"- {out_dir}/tickets.csv")
    print(f"- {out_dir}/member_support_summary.csv")

if __name__ == "__main__":
    main()