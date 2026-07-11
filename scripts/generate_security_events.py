"""Generate a realistic SecurityEvent dataset for a SaaS BI platform."""

import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

SEED = 42

CUSTOMERS_PATH = (
    Path.home() / "Desktop" / "microsoft-project" / "data" / "raw" / "customers.csv"
)

OUTPUT_PATH = (
    Path.home()
    / "Desktop"
    / "microsoft-project"
    / "data"
    / "raw"
    / "security_events.csv"
)

EVENT_WEIGHTS = {
    "Successful Login": 0.45,
    "Failed Login": 0.20,
    "Password Reset Attempt": 0.10,
    "Login From New Device": 0.08,
    "Login From New Country": 0.05,
    "Session Timeout": 0.05,
    "MFA Enabled": 0.03,
    "MFA Failed": 0.02,
    "Suspicious IP": 0.015,
    "Account Locked": 0.005,
}

DESCRIPTION_LIBRARY = {
    "Successful Login": [
        "User logged in successfully.",
        "Successful authentication.",
        "Login completed successfully.",
    ],
    "Failed Login": [
        "Invalid password entered.",
        "Authentication failed.",
        "Incorrect credentials provided.",
    ],
    "Password Reset Attempt": [
        "Password reset requested.",
        "User initiated password reset.",
        "Password recovery process started.",
    ],
    "Login From New Device": [
        "Login detected from a new device.",
        "New browser/device identified.",
        "First login from this device.",
    ],
    "Login From New Country": [
        "Login detected from another country.",
        "Unexpected country detected.",
        "Foreign login attempt identified.",
    ],
    "Session Timeout": [
        "Session expired due to inactivity.",
        "Automatic logout after timeout.",
        "Inactive session terminated.",
    ],
    "MFA Enabled": [
        "Multi-factor authentication enabled.",
        "MFA activated successfully.",
        "Security settings updated.",
    ],
    "MFA Failed": [
        "MFA verification failed.",
        "Incorrect verification code.",
        "Second factor authentication failed.",
    ],
    "Suspicious IP": [
        "Login attempt from suspicious IP.",
        "Potential malicious IP detected.",
        "Untrusted IP address identified.",
    ],
    "Account Locked": [
        "Account locked after repeated failures.",
        "Security policy locked the account.",
        "Too many failed login attempts.",
    ],
}


def _load_customers(
    customers_path: Path,
) -> pd.DataFrame:
    """Load customers dataset."""

    return pd.read_csv(customers_path)


def _generate_event_id(index: int) -> str:
    """Return formatted event ID."""

    return f"E{index:03d}"


def _random_event_time() -> datetime:
    """Generate random event time."""

    start = datetime(2026, 1, 1)
    end = datetime(2026, 6, 30)

    return start + timedelta(
        days=random.randint(0, (end - start).days),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )


def _select_event_type() -> str:
    """Select event type."""

    return random.choices(
        population=list(EVENT_WEIGHTS.keys()),
        weights=list(EVENT_WEIGHTS.values()),
        k=1,
    )[0]

def _generate_severity(
    event_type: str,
) -> str:
    """Generate event severity."""

    if event_type == "Successful Login":
        return "Low"

    if event_type == "Session Timeout":
        return "Low"

    if event_type == "MFA Enabled":
        return "Low"

    if event_type == "Password Reset Attempt":
        return random.choices(
            ["Low", "Medium"],
            weights=[0.70, 0.30],
            k=1,
        )[0]

    if event_type == "Login From New Device":
        return random.choices(
            ["Low", "Medium"],
            weights=[0.60, 0.40],
            k=1,
        )[0]

    if event_type == "Failed Login":
        return random.choices(
            ["Low", "Medium"],
            weights=[0.45, 0.55],
            k=1,
        )[0]

    if event_type == "MFA Failed":
        return random.choices(
            ["Medium", "High"],
            weights=[0.80, 0.20],
            k=1,
        )[0]

    if event_type == "Login From New Country":
        return random.choices(
            ["Medium", "High"],
            weights=[0.70, 0.30],
            k=1,
        )[0]

    if event_type == "Suspicious IP":
        return random.choices(
            ["Medium", "High"],
            weights=[0.35, 0.65],
            k=1,
        )[0]

    if event_type == "Account Locked":
        return "High"

    return "Low"


def _generate_status(
    severity: str,
) -> str:
    """Generate event status."""

    if severity == "High":
        return random.choices(
            ["Investigating", "Resolved"],
            weights=[0.40, 0.60],
            k=1,
        )[0]

    return random.choices(
        ["Resolved", "Ignored"],
        weights=[0.85, 0.15],
        k=1,
    )[0]


def _build_security_record(
    customer_id: str,
) -> dict:
    """Build a security event."""

    event_type = _select_event_type()

    severity = _generate_severity(
        event_type,
    )

    status = _generate_status(
        severity,
    )

    event_time = _random_event_time()

    return {
        "customer_id": customer_id,
        "event_type": event_type,
        "severity": severity,
        "description": random.choice(
            DESCRIPTION_LIBRARY[event_type]
        ),
        "status": status,
        "event_time": event_time.strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
    }

def generate_security_events(
    customers_path: Path = CUSTOMERS_PATH,
    output_path: Path = OUTPUT_PATH,
    seed: int = SEED,
) -> pd.DataFrame:
    """
    Generate security event records and save them to CSV.

    Args:
        customers_path: Path to customers.csv.
        output_path: Output CSV path.
        seed: Random seed.

    Returns:
        DataFrame containing generated security event records.
    """

    random.seed(seed)

    customers = _load_customers(
        customers_path,
    )

    records = []

    for _, row in customers.iterrows():

        customer_id = row["customer_id"]

        # Most customers only have normal security activity.
        event_count = random.choices(
            [1, 2, 3],
            weights=[0.70, 0.25, 0.05],
            k=1,
        )[0]

        # Around 15% of customers experience additional security events.
        if random.random() < 0.15:
            event_count += random.randint(2, 4)

        for _ in range(event_count):
            records.append(
                _build_security_record(
                    customer_id,
                )
            )

    events = pd.DataFrame(records)

    events.insert(
        0,
        "event_id",
        [
            _generate_event_id(i)
            for i in range(
                1,
                len(events) + 1,
            )
        ],
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    events.to_csv(
        output_path,
        index=False,
    )

    print(
        f"Generated {len(events)} security events -> {output_path}"
    )

    return events


if __name__ == "__main__":
    generate_security_events()