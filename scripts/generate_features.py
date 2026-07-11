"""Generate the Feature dataset for a SaaS BI & AI Decision Support platform."""

from pathlib import Path

import pandas as pd

OUTPUT_PATH = (
    Path.home() / "Desktop" / "microsoft-project" / "data" / "raw" / "features.csv"
)

FEATURES = [
    {"feature_name": "User Dashboard", "module": "Core"},
    {"feature_name": "Data Import & Export", "module": "Core"},
    {"feature_name": "AI Assistant Chat", "module": "AI"},
    {"feature_name": "Predictive Insights", "module": "AI"},
    {"feature_name": "Natural Language Query", "module": "AI"},
    {"feature_name": "Custom Reports Builder", "module": "Analytics"},
    {"feature_name": "Real-Time Analytics Dashboard", "module": "Analytics"},
    {"feature_name": "KPI Scorecards", "module": "Analytics"},
    {"feature_name": "Team Workspaces", "module": "Collaboration"},
    {"feature_name": "Shared Annotations", "module": "Collaboration"},
    {"feature_name": "Single Sign-On (SSO)", "module": "Security"},
    {"feature_name": "Role-Based Access Control", "module": "Security"},
    {"feature_name": "Audit Log Viewer", "module": "Security"},
    {"feature_name": "User Management", "module": "Administration"},
    {"feature_name": "Billing & Subscription Management", "module": "Administration"},
    {"feature_name": "Task Boards", "module": "Project Management"},
    {"feature_name": "Milestone Tracking", "module": "Project Management"},
    {"feature_name": "API Connectors", "module": "Integration"},
    {"feature_name": "Webhook Automation", "module": "Integration"},
    {"feature_name": "System Health Monitor", "module": "Monitoring"},
]


def _generate_feature_id(index: int) -> str:
    """Return formatted feature ID (e.g. F001)."""
    return f"F{index:03d}"


def generate_features(output_path: Path = OUTPUT_PATH) -> pd.DataFrame:
    """
    Generate feature records and save them to CSV.

    Args:
        output_path: Destination path for the CSV file.

    Returns:
        DataFrame containing the generated feature records.
    """
    records = [
        {
            "feature_id": _generate_feature_id(index),
            "feature_name": feature["feature_name"],
            "module": feature["module"],
            "is_active": True,
        }
        for index, feature in enumerate(FEATURES, start=1)
    ]

    features = pd.DataFrame(records)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    features.to_csv(output_path, index=False)
    print(f"Generated {len(features)} features -> {output_path}")
    return features


if __name__ == "__main__":
    generate_features()
