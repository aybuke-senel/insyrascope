"""Generate a realistic ProductUsage dataset for a SaaS BI platform."""

import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

SEED = 42
CUSTOMERS_PATH = (
    Path.home() / "Desktop" / "microsoft-project" / "data" / "raw" / "customers.csv"
)
FEATURES_PATH = (
    Path.home() / "Desktop" / "microsoft-project" / "data" / "raw" / "features.csv"
)
OUTPUT_PATH = (
    Path.home()
    / "Desktop"
    / "microsoft-project"
    / "data"
    / "raw"
    / "product_usage.csv"
)

DEVICES = ["Web", "Desktop", "Mobile"]
DEVICE_WEIGHTS = [0.50, 0.35, 0.15]

ANALYTICS_FEATURES = [
    "Custom Reports Builder",
    "Real-Time Analytics Dashboard",
    "KPI Scorecards",
]
INTEGRATION_FEATURES = ["API Connectors", "Webhook Automation"]
SECURITY_FEATURES = [
    "Single Sign-On (SSO)",
    "Role-Based Access Control",
    "Audit Log Viewer",
]

FEATURE_USAGE_MULTIPLIERS = {
    "User Dashboard": 1.6,
    "Data Import & Export": 0.9,
    "AI Assistant Chat": 2.0,
    "Predictive Insights": 1.3,
    "Natural Language Query": 1.7,
    "Custom Reports Builder": 1.4,
    "Real-Time Analytics Dashboard": 1.5,
    "KPI Scorecards": 1.2,
    "Team Workspaces": 1.3,
    "Shared Annotations": 1.0,
    "Single Sign-On (SSO)": 0.25,
    "Role-Based Access Control": 0.30,
    "Audit Log Viewer": 0.20,
    "User Management": 0.5,
    "Billing & Subscription Management": 0.15,
    "Task Boards": 1.25,
    "Milestone Tracking": 0.8,
    "API Connectors": 0.6,
    "Webhook Automation": 0.55,
    "System Health Monitor": 0.7,
}

FEATURE_SESSION_MULTIPLIERS = {
    "User Dashboard": 1.1,
    "Data Import & Export": 1.0,
    "AI Assistant Chat": 1.3,
    "Predictive Insights": 1.4,
    "Natural Language Query": 1.2,
    "Custom Reports Builder": 1.5,
    "Real-Time Analytics Dashboard": 1.6,
    "KPI Scorecards": 1.3,
    "Team Workspaces": 1.2,
    "Shared Annotations": 0.9,
    "Single Sign-On (SSO)": 0.5,
    "Role-Based Access Control": 0.6,
    "Audit Log Viewer": 0.5,
    "User Management": 0.7,
    "Billing & Subscription Management": 0.4,
    "Task Boards": 1.2,
    "Milestone Tracking": 1.0,
    "API Connectors": 0.8,
    "Webhook Automation": 0.75,
    "System Health Monitor": 0.85,
}

PLAN_USAGE_RANGES = {
    "Basic": (8, 65),
    "Pro": (25, 180),
    "Enterprise": (40, 280),
}
PLAN_SESSION_RANGES = {
    "Basic": (4, 12),
    "Pro": (10, 22),
    "Enterprise": (15, 32),
}

STATUS_USAGE_MULTIPLIER = {
    "Active": 1.0,
    "Inactive": 0.35,
    "Churned": 0.12,
}
STATUS_SESSION_MULTIPLIER = {
    "Active": 1.0,
    "Inactive": 0.6,
    "Churned": 0.4,
}

ANALYTICS_ADOPTION_RATES = {"Basic": 0.25, "Pro": 0.70, "Enterprise": 0.85}
INTEGRATION_ADOPTION_RATES = {"Basic": 0.05, "Pro": 0.18, "Enterprise": 0.75}

AI_CHAT_ADOPTION_RATES = {"Active": 0.90, "Inactive": 0.55, "Churned": 0.30}
NLQ_ADOPTION_RATES = {"Active": 0.82, "Inactive": 0.45, "Churned": 0.25}

GENERAL_FILLER_FEATURES = [
    "Data Import & Export",
    "Shared Annotations",
    "User Management",
    "Milestone Tracking",
    "System Health Monitor",
    "Team Workspaces",
    "Task Boards",
]

TRIM_ORDER = [
    "Audit Log Viewer",
    "Single Sign-On (SSO)",
    "Role-Based Access Control",
    "Billing & Subscription Management",
    "System Health Monitor",
    "Shared Annotations",
    "Milestone Tracking",
    "User Management",
    "Data Import & Export",
    "KPI Scorecards",
    "Custom Reports Builder",
    "Real-Time Analytics Dashboard",
    "Webhook Automation",
    "API Connectors",
    "Predictive Insights",
    "Task Boards",
    "Team Workspaces",
    "Natural Language Query",
    "AI Assistant Chat",
    "User Dashboard",
]


def _load_reference_data(
    customers_path: Path,
    features_path: Path,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, str], dict[str, str]]:
    """Load customer and feature datasets and build lookup maps."""
    customers = pd.read_csv(customers_path)
    features = pd.read_csv(features_path)
    name_to_id = dict(zip(features["feature_name"], features["feature_id"]))
    id_to_name = dict(zip(features["feature_id"], features["feature_name"]))
    return customers, features, name_to_id, id_to_name


def _generate_usage_id(index: int) -> str:
    """Return formatted usage ID (e.g. U001)."""
    return f"U{index:03d}"


def _target_feature_count(status: str) -> int:
    """Determine how many features a customer should use based on status."""
    if status == "Active":
        return random.randint(8, 14)
    if status == "Inactive":
        return random.randint(5, 10)
    return random.randint(5, 7)


def _maybe_add(selected: set[str], feature_id: str, probability: float) -> None:
    """Add a feature to the selection set based on probability."""
    if random.random() < probability:
        selected.add(feature_id)


def _select_features(
    plan: str,
    status: str,
    target_count: int,
    name_to_id: dict[str, str],
) -> set[str]:
    """Select features for a customer according to business rules."""
    selected: set[str] = set()

    _maybe_add(selected, name_to_id["User Dashboard"], 0.98)
    _maybe_add(selected, name_to_id["AI Assistant Chat"], AI_CHAT_ADOPTION_RATES[status])

    nlq_rate = NLQ_ADOPTION_RATES[status]
    if plan != "Basic" or random.random() < 0.35:
        _maybe_add(selected, name_to_id["Natural Language Query"], nlq_rate)

    if plan == "Enterprise":
        selected.add(name_to_id["Predictive Insights"])
    elif plan == "Pro":
        pi_rate = {"Active": 0.75, "Inactive": 0.45, "Churned": 0.20}[status]
        _maybe_add(selected, name_to_id["Predictive Insights"], pi_rate)
    else:
        _maybe_add(selected, name_to_id["Predictive Insights"], 0.08)

    for feature_name in ANALYTICS_FEATURES:
        _maybe_add(selected, name_to_id[feature_name], ANALYTICS_ADOPTION_RATES[plan])

    integration_rate = INTEGRATION_ADOPTION_RATES[plan]
    if plan == "Enterprise":
        integration_rate = 0.80
    for feature_name in INTEGRATION_FEATURES:
        _maybe_add(selected, name_to_id[feature_name], integration_rate)

    for feature_name in SECURITY_FEATURES:
        _maybe_add(selected, name_to_id[feature_name], 0.45)

    _maybe_add(selected, name_to_id["Billing & Subscription Management"], 0.30)

    if random.random() < 0.65:
        selected.add(name_to_id["Team Workspaces"])
        _maybe_add(selected, name_to_id["Task Boards"], 0.85)
    elif random.random() < 0.50:
        selected.add(name_to_id["Task Boards"])
        _maybe_add(selected, name_to_id["Team Workspaces"], 0.80)

    _maybe_add(selected, name_to_id["Data Import & Export"], 0.55)
    _maybe_add(selected, name_to_id["Shared Annotations"], 0.40)
    _maybe_add(selected, name_to_id["User Management"], 0.50)
    _maybe_add(selected, name_to_id["Milestone Tracking"], 0.45)
    _maybe_add(selected, name_to_id["System Health Monitor"], 0.35)

    filler_names = GENERAL_FILLER_FEATURES.copy()
    if plan in {"Pro", "Enterprise"}:
        filler_names.extend(ANALYTICS_FEATURES)
    if plan == "Enterprise":
        filler_names.extend(INTEGRATION_FEATURES)

    available = [
        name_to_id[name]
        for name in filler_names
        if name_to_id[name] not in selected
    ]
    random.shuffle(available)

    minimum_count = max(5, target_count)
    while len(selected) < minimum_count and available:
        selected.add(available.pop())

    protected = {
        name_to_id["User Dashboard"],
        name_to_id["AI Assistant Chat"],
    }
    if plan == "Enterprise":
        protected.add(name_to_id["Predictive Insights"])

    while len(selected) > target_count:
        removed = False
        for feature_name in TRIM_ORDER:
            feature_id = name_to_id[feature_name]
            if feature_id in selected and feature_id not in protected:
                selected.remove(feature_id)
                removed = True
                break
        if not removed:
            break

    while len(selected) < 5:
        candidates = [
            name_to_id[name]
            for name in filler_names
            if name_to_id[name] not in selected
        ]
        if not candidates:
            break
        selected.add(random.choice(candidates))

    return selected


def _random_last_used(status: str) -> str:
    """Generate a last_used date biased by customer status."""
    if status == "Churned":
        start = datetime(2026, 1, 1)
        end = datetime(2026, 4, 15)
    elif status == "Inactive":
        start = datetime(2026, 2, 1)
        end = datetime(2026, 5, 31)
    else:
        start = datetime(2026, 3, 1)
        end = datetime(2026, 6, 30)

    day_range = (end - start).days
    last_used = start + timedelta(days=random.randint(0, day_range))
    return last_used.strftime("%Y-%m-%d")


def _select_device(feature_name: str) -> str:
    """Select a realistic device based on feature type."""
    if feature_name in SECURITY_FEATURES or feature_name == "User Management":
        weights = [0.25, 0.60, 0.15]
    elif feature_name in {"AI Assistant Chat", "Natural Language Query"}:
        weights = [0.55, 0.25, 0.20]
    elif feature_name == "Billing & Subscription Management":
        weights = [0.60, 0.30, 0.10]
    else:
        weights = DEVICE_WEIGHTS
    return random.choices(DEVICES, weights=weights, k=1)[0]


def _generate_usage_count(
    plan: str,
    status: str,
    feature_name: str,
) -> int:
    """Generate usage_count aligned with plan, status, and feature profile."""
    low, high = PLAN_USAGE_RANGES[plan]
    base = random.randint(low, high)
    multiplier = FEATURE_USAGE_MULTIPLIERS.get(feature_name, 1.0)
    multiplier *= STATUS_USAGE_MULTIPLIER[status]
    return max(1, int(base * multiplier))


def _generate_session_duration(
    plan: str,
    status: str,
    feature_name: str,
) -> float:
    """Generate average session duration in minutes."""
    low, high = PLAN_SESSION_RANGES[plan]
    base = random.uniform(low, high)
    multiplier = FEATURE_SESSION_MULTIPLIERS.get(feature_name, 1.0)
    multiplier *= STATUS_SESSION_MULTIPLIER[status]
    return round(max(1.0, base * multiplier), 1)


def _build_usage_record(
    customer_id: str,
    feature_id: str,
    feature_name: str,
    plan: str,
    status: str,
) -> dict:
    """Build a single product usage record."""
    return {
        "customer_id": customer_id,
        "feature_id": feature_id,
        "usage_count": _generate_usage_count(plan, status, feature_name),
        "session_duration": _generate_session_duration(plan, status, feature_name),
        "last_device": _select_device(feature_name),
        "last_used": _random_last_used(status),
    }


def generate_product_usage(
    customers_path: Path = CUSTOMERS_PATH,
    features_path: Path = FEATURES_PATH,
    output_path: Path = OUTPUT_PATH,
    seed: int = SEED,
) -> pd.DataFrame:
    """
    Generate product usage records and save them to CSV.

    Args:
        customers_path: Path to the customers CSV file.
        features_path: Path to the features CSV file.
        output_path: Destination path for the output CSV file.
        seed: Seed value for reproducible output.

    Returns:
        DataFrame containing the generated product usage records.
    """
    random.seed(seed)

    customers, _, name_to_id, id_to_name = _load_reference_data(
        customers_path, features_path
    )
    records = []

    for _, customer in customers.iterrows():
        customer_id = customer["customer_id"]
        plan = customer["subscription_plan"]
        status = customer["customer_status"]
        target_count = _target_feature_count(status)
        selected_features = _select_features(plan, status, target_count, name_to_id)

        for feature_id in sorted(selected_features):
            feature_name = id_to_name[feature_id]
            records.append(
                _build_usage_record(customer_id, feature_id, feature_name, plan, status)
            )

    product_usage = pd.DataFrame(records)
    product_usage.insert(
        0,
        "usage_id",
        [_generate_usage_id(index) for index in range(1, len(product_usage) + 1)],
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    product_usage.to_csv(output_path, index=False)
    print(f"Generated {len(product_usage)} product usage records -> {output_path}")
    return product_usage


if __name__ == "__main__":
    generate_product_usage()
