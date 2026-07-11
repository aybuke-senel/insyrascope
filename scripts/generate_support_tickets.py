"""Generate a realistic SupportTicket dataset for a SaaS BI platform."""

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

PRODUCT_USAGE_PATH = (
    Path.home()
    / "Desktop"
    / "microsoft-project"
    / "data"
    / "raw"
    / "product_usage.csv"
)

OUTPUT_PATH = (
    Path.home()
    / "Desktop"
    / "microsoft-project"
    / "data"
    / "raw"
    / "support_tickets.csv"
)

CATEGORY_WEIGHTS = {
    "Account Management": 0.24,
    "Password Reset": 0.18,
    "Billing Question": 0.15,
    "Feature Request": 0.14,
    "Bug Report": 0.12,
    "Performance Issue": 0.09,
    "Technical Support": 0.08,
}

TEAM_MAPPING = {
    "Account Management": "Customer Success",
    "Password Reset": "Customer Success",
    "Billing Question": "Finance",
    "Feature Request": "Product Team",
    "Bug Report": "Engineering",
    "Performance Issue": "Engineering",
    "Technical Support": "Technical Support",
}

FEATURE_TICKET_PROBABILITY = {
    "User Dashboard": 0.04,
    "Data Import & Export": 0.08,
    "AI Assistant Chat": 0.02,
    "Predictive Insights": 0.04,
    "Natural Language Query": 0.05,
    "Custom Reports Builder": 0.08,
    "Real-Time Analytics Dashboard": 0.12,
    "KPI Scorecards": 0.05,
    "Team Workspaces": 0.06,
    "Shared Annotations": 0.04,
    "Single Sign-On (SSO)": 0.05,
    "Role-Based Access Control": 0.03,
    "Audit Log Viewer": 0.03,
    "User Management": 0.05,
    "Billing & Subscription Management": 0.15,
    "Task Boards": 0.06,
    "Milestone Tracking": 0.05,
    "API Connectors": 0.07,
    "Webhook Automation": 0.06,
    "System Health Monitor": 0.05,
}

DESCRIPTION_LIBRARY = {
    "Account Management": [
        "Need help updating account information.",
        "Unable to modify account settings.",
        "Account configuration assistance required.",
    ],
    "Password Reset": [
        "Unable to reset password.",
        "Password reset email not received.",
        "Login issue after password reset.",
    ],
    "Billing Question": [
        "Question regarding invoice.",
        "Unexpected subscription charge.",
        "Billing clarification required.",
    ],
    "Feature Request": [
        "Please add more filtering options.",
        "Would like more customization.",
        "Need additional export formats.",
    ],
    "Bug Report": [
        "Unexpected application error.",
        "Feature crashes occasionally.",
        "Observed inconsistent behaviour.",
    ],
    "Performance Issue": [
        "Dashboard loads very slowly.",
        "Reports take too long to generate.",
        "System response is inconsistent.",
    ],
    "Technical Support": [
        "Need help configuring the feature.",
        "Need assistance with integration.",
        "Configuration guidance required.",
    ],
}


def _load_reference_data(
    customers_path: Path,
    features_path: Path,
    usage_path: Path,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load required datasets."""

    customers = pd.read_csv(customers_path)
    features = pd.read_csv(features_path)
    usage = pd.read_csv(usage_path)

    return customers, features, usage


def _generate_ticket_id(index: int) -> str:
    """Return formatted ticket ID."""
    return f"T{index:03d}"


def _random_created_date() -> datetime:
    """Generate ticket creation date."""

    start = datetime(2026, 1, 1)
    end = datetime(2026, 6, 30)

    return start + timedelta(
        days=random.randint(0, (end - start).days)
    )


def _should_create_ticket(
    feature_name: str,
    usage_count: int,
    customer_status: str,
) -> bool:
    """Determine whether a ticket should be created."""

    probability = FEATURE_TICKET_PROBABILITY.get(
        feature_name,
        0.05,
    )

    if usage_count > 180:
        probability *= 1.40

    elif usage_count > 100:
        probability *= 1.20

    if customer_status == "Inactive":
        probability *= 0.85

    elif customer_status == "Churned":
        probability *= 0.70

    return random.random() < min(probability, 0.30)

def _generate_category(feature_name: str) -> str:
    """Generate a realistic support ticket category."""

    if feature_name == "Billing & Subscription Management":
        return random.choices(
            ["Billing Question", "Account Management"],
            weights=[0.80, 0.20],
            k=1,
        )[0]

    if feature_name == "Single Sign-On (SSO)":
        return random.choices(
            ["Password Reset", "Technical Support"],
            weights=[0.75, 0.25],
            k=1,
        )[0]

    if feature_name == "Role-Based Access Control":
        return random.choice(
            [
                "Technical Support",
                "Account Management",
            ]
        )

    if feature_name == "Audit Log Viewer":
        return "Technical Support"

    if feature_name == "AI Assistant Chat":
        return random.choices(
            ["Feature Request", "Technical Support"],
            weights=[0.75, 0.25],
            k=1,
        )[0]

    if feature_name == "Natural Language Query":
        return random.choices(
            [
                "Feature Request",
                "Bug Report",
                "Technical Support",
            ],
            weights=[0.55, 0.25, 0.20],
            k=1,
        )[0]

    if feature_name == "Real-Time Analytics Dashboard":
        return random.choices(
            [
                "Performance Issue",
                "Bug Report",
                "Feature Request",
            ],
            weights=[0.45, 0.35, 0.20],
            k=1,
        )[0]

    return random.choices(
        population=list(CATEGORY_WEIGHTS.keys()),
        weights=list(CATEGORY_WEIGHTS.values()),
        k=1,
    )[0]


def _generate_priority(category: str) -> str:
    """Generate ticket priority."""

    if category == "Performance Issue":
        return random.choices(
            ["High", "Medium"],
            weights=[0.45, 0.55],
            k=1,
        )[0]

    if category == "Bug Report":
        return random.choices(
            ["High", "Medium"],
            weights=[0.60, 0.40],
            k=1,
        )[0]

    if category == "Password Reset":
        return random.choices(
            ["High", "Medium", "Low"],
            weights=[0.25, 0.55, 0.20],
            k=1,
        )[0]

    if category == "Billing Question":
        return random.choices(
            ["Medium", "Low"],
            weights=[0.70, 0.30],
            k=1,
        )[0]

    return random.choices(
        ["Medium", "Low"],
        weights=[0.60, 0.40],
        k=1,
    )[0]


def _generate_status() -> str:
    """Generate ticket status."""

    return random.choices(
        ["Resolved", "In Progress", "Open"],
        weights=[0.72, 0.18, 0.10],
        k=1,
    )[0]


def _generate_resolved_date(
    created_at: datetime,
    status: str,
) -> str | None:
    """Generate resolved date."""

    if status != "Resolved":
        return None

    resolved = created_at + timedelta(
        days=random.randint(1, 14)
    )

    return resolved.strftime("%Y-%m-%d")


def _generate_feature_id(
    category: str,
    feature_id: str,
) -> str | None:
    """
    Some ticket categories are not tied to a specific feature.
    """

    if category in {
        "Password Reset",
        "Account Management",
    }:
        return None

    return feature_id


def _build_ticket_record(
    customer_id: str,
    feature_id: str,
    feature_name: str,
) -> dict:
    """Build a support ticket."""

    category = _generate_category(
        feature_name,
    )

    priority = _generate_priority(
        category,
    )

    status = _generate_status()

    created_at = _random_created_date()

    return {
        "customer_id": customer_id,
        "feature_id": _generate_feature_id(
            category,
            feature_id,
        ),
        "ticket_category": category,
        "priority": priority,
        "status": status,
        "assigned_team": TEAM_MAPPING[category],
        "description": random.choice(
            DESCRIPTION_LIBRARY[category]
        ),
        "created_at": created_at.strftime("%Y-%m-%d"),
        "resolved_at": _generate_resolved_date(
            created_at,
            status,
        ),
    }

def generate_support_tickets(
    customers_path: Path = CUSTOMERS_PATH,
    features_path: Path = FEATURES_PATH,
    usage_path: Path = PRODUCT_USAGE_PATH,
    output_path: Path = OUTPUT_PATH,
    seed: int = SEED,
) -> pd.DataFrame:
    """
    Generate support ticket records and save them to CSV.

    Args:
        customers_path: Path to customers.csv.
        features_path: Path to features.csv.
        usage_path: Path to product_usage.csv.
        output_path: Output CSV path.
        seed: Random seed.

    Returns:
        DataFrame containing generated support ticket records.
    """

    random.seed(seed)

    customers, features, usage = _load_reference_data(
        customers_path,
        features_path,
        usage_path,
    )

    customer_status = dict(
        zip(
            customers["customer_id"],
            customers["customer_status"],
        )
    )

    feature_lookup = dict(
        zip(
            features["feature_id"],
            features["feature_name"],
        )
    )

    records = []

    for _, row in usage.iterrows():

        feature_name = feature_lookup[row["feature_id"]]

        if not _should_create_ticket(
            feature_name,
            row["usage_count"],
            customer_status[row["customer_id"]],
        ):
            continue

        records.append(
            _build_ticket_record(
                customer_id=row["customer_id"],
                feature_id=row["feature_id"],
                feature_name=feature_name,
            )
        )

    tickets = pd.DataFrame(records)

    tickets.insert(
        0,
        "ticket_id",
        [
            _generate_ticket_id(i)
            for i in range(
                1,
                len(tickets) + 1,
            )
        ],
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    tickets.to_csv(
        output_path,
        index=False,
    )

    print(
        f"Generated {len(tickets)} support tickets -> {output_path}"
    )

    return tickets


if __name__ == "__main__":
    generate_support_tickets()