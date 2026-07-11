"""Generate a realistic CustomerFeedback dataset for a SaaS BI platform."""

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
    / "customer_feedback.csv"
)

POSITIVE_COMMENTS = [
    "Very useful feature.",
    "Easy to use.",
    "Excellent experience.",
    "Saves me a lot of time.",
    "Works perfectly.",
    "Very intuitive interface.",
    "Really improves productivity.",
    "Great implementation.",
    "Excellent AI suggestions.",
    "Highly recommended.",
]

NEUTRAL_COMMENTS = [
    "Works as expected.",
    "Good overall.",
    "Satisfactory.",
    "Useful but could be improved.",
    "No major issues.",
    "Average experience.",
    "Acceptable performance.",
]

NEGATIVE_COMMENTS = [
    "Too slow.",
    "Sometimes crashes.",
    "Search results are inconsistent.",
    "Export fails occasionally.",
    "UI is confusing.",
    "Needs better performance.",
    "Expected more functionality.",
    "Response time is too long.",
]

FEATURE_REQUEST_COMMENTS = [
    "Would like more customization.",
    "Please add more filtering options.",
    "Needs additional export formats.",
    "Dark mode would be useful.",
    "Please improve AI responses.",
    "More integrations would help.",
]

CATEGORIES = [
    "Performance",
    "UI/UX",
    "Feature Request",
    "Bug",
    "Reliability",
    "General Satisfaction",
]

FEATURE_BIASES = {
    "AI Assistant Chat": {
        "positive": 0.80,
        "neutral": 0.15,
        "negative": 0.05,
    },
    "Natural Language Query": {
        "positive": 0.70,
        "neutral": 0.20,
        "negative": 0.10,
    },
    "Real-Time Analytics Dashboard": {
        "positive": 0.60,
        "neutral": 0.25,
        "negative": 0.15,
    },
    "Billing & Subscription Management": {
        "positive": 0.50,
        "neutral": 0.30,
        "negative": 0.20,
    },
}

DEFAULT_BIAS = {
    "positive": 0.65,
    "neutral": 0.25,
    "negative": 0.10,
}


def _load_reference_data(
    customers_path: Path,
    features_path: Path,
    usage_path: Path,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load customers, features and product usage datasets."""
    customers = pd.read_csv(customers_path)
    features = pd.read_csv(features_path)
    usage = pd.read_csv(usage_path)

    return customers, features, usage


def _generate_feedback_id(index: int) -> str:
    """Return formatted feedback ID."""
    return f"FB{index:03d}"


def _random_date() -> str:
    """Generate a random feedback date."""
    start = datetime(2026, 1, 1)
    end = datetime(2026, 6, 30)

    delta = (end - start).days

    return (
        start + timedelta(days=random.randint(0, delta))
    ).strftime("%Y-%m-%d")


def _should_leave_feedback(
    usage_count: int,
    customer_status: str,
) -> bool:
    """Determine whether a customer leaves feedback."""

    probability = min(0.25 + usage_count / 350, 0.85)

    if customer_status == "Inactive":
        probability *= 0.70

    elif customer_status == "Churned":
        probability *= 0.45

    return random.random() < probability

def _generate_rating(
    feature_name: str,
    customer_status: str,
) -> int:
    """Generate a realistic rating."""

    bias = FEATURE_BIASES.get(feature_name, DEFAULT_BIAS)

    positive = bias["positive"]
    neutral = bias["neutral"]
    negative = bias["negative"]

    if customer_status == "Churned":
        positive *= 0.55
        negative *= 2.00

    elif customer_status == "Inactive":
        positive *= 0.80
        negative *= 1.40

    total = positive + neutral + negative

    positive /= total
    neutral /= total
    negative /= total

    sentiment = random.choices(
        ["positive", "neutral", "negative"],
        weights=[positive, neutral, negative],
        k=1,
    )[0]

    if sentiment == "positive":
        return random.choice([4, 5])

    if sentiment == "neutral":
        return 3

    return random.choice([1, 2])


def _generate_sentiment(rating: int) -> str:
    """Generate sentiment from rating."""

    if rating >= 4:
        return "Positive"

    if rating == 3:
        return "Neutral"

    return "Negative"


def _generate_category(
    feature_name: str,
    rating: int,
) -> str:
    """Generate feedback category."""

    if rating <= 2:

        if feature_name == "Real-Time Analytics Dashboard":
            return random.choice(["Performance", "Bug"])

        if feature_name == "Billing & Subscription Management":
            return random.choice(["Reliability", "UI/UX"])

        return random.choice(
            [
                "Performance",
                "Bug",
                "UI/UX",
            ]
        )

    if feature_name == "Natural Language Query":
        if random.random() < 0.30:
            return "Feature Request"

    if feature_name == "AI Assistant Chat":
        if random.random() < 0.20:
            return "Feature Request"

    return random.choice(
        [
            "General Satisfaction",
            "UI/UX",
            "Reliability",
        ]
    )


def _generate_comment(
    rating: int,
    category: str,
) -> str:
    """Generate a realistic English comment."""

    if category == "Feature Request":
        return random.choice(FEATURE_REQUEST_COMMENTS)

    if rating >= 4:
        return random.choice(POSITIVE_COMMENTS)

    if rating == 3:
        return random.choice(NEUTRAL_COMMENTS)

    return random.choice(NEGATIVE_COMMENTS)


def _build_feedback_record(
    customer_id: str,
    feature_id: str,
    feature_name: str,
    customer_status: str,
) -> dict:
    """Build a feedback record."""

    rating = _generate_rating(
        feature_name,
        customer_status,
    )

    category = _generate_category(
        feature_name,
        rating,
    )

    return {
        "customer_id": customer_id,
        "feature_id": feature_id,
        "rating": rating,
        "feedback_category": category,
        "comment": _generate_comment(
            rating,
            category,
        ),
        "sentiment": _generate_sentiment(
            rating,
        ),
        "created_at": _random_date(),
    }

def generate_customer_feedback(
    customers_path: Path = CUSTOMERS_PATH,
    features_path: Path = FEATURES_PATH,
    usage_path: Path = PRODUCT_USAGE_PATH,
    output_path: Path = OUTPUT_PATH,
    seed: int = SEED,
) -> pd.DataFrame:
    """
    Generate customer feedback records and save them to CSV.

    Args:
        customers_path: Path to customers.csv.
        features_path: Path to features.csv.
        usage_path: Path to product_usage.csv.
        output_path: Output CSV path.
        seed: Random seed.

    Returns:
        DataFrame containing generated feedback records.
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

    feature_names = dict(
        zip(
            features["feature_id"],
            features["feature_name"],
        )
    )

    records = []

    for _, row in usage.iterrows():

        if not _should_leave_feedback(
            row["usage_count"],
            customer_status[row["customer_id"]],
        ):
            continue

        feature_name = feature_names[row["feature_id"]]

        records.append(
            _build_feedback_record(
                customer_id=row["customer_id"],
                feature_id=row["feature_id"],
                feature_name=feature_name,
                customer_status=customer_status[row["customer_id"]],
            )
        )

    feedback = pd.DataFrame(records)

    feedback.insert(
        0,
        "feedback_id",
        [
            _generate_feedback_id(i)
            for i in range(
                1,
                len(feedback) + 1,
            )
        ],
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    feedback.to_csv(
        output_path,
        index=False,
    )

    print(
        f"Generated {len(feedback)} customer feedback records -> {output_path}"
    )

    return feedback


if __name__ == "__main__":
    generate_customer_feedback()