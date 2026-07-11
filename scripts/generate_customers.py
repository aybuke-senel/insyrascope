"""Generate a realistic customer dataset for a SaaS platform."""

import random
import unicodedata
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from faker import Faker

SEED = 42
NUM_CUSTOMERS = 100
OUTPUT_PATH = (
    Path.home() / "Desktop" / "microsoft-project" / "data" / "raw" / "customers.csv"
)

COUNTRIES = [
    "Türkiye",
    "United States",
    "United Kingdom",
    "Germany",
    "Canada",
    "Netherlands",
    "Australia",
    "Singapore",
]
COUNTRY_WEIGHTS = [0.08, 0.35, 0.15, 0.12, 0.10, 0.06, 0.09, 0.05]
COUNTRY_LOCALES = {
    "Türkiye": "tr_TR",
    "United States": "en_US",
    "United Kingdom": "en_GB",
    "Germany": "de_DE",
    "Canada": "en_CA",
    "Netherlands": "nl_NL",
    "Australia": "en_AU",
    "Singapore": "en_US",
}

EMAIL_DOMAINS = ["gmail.com", "outlook.com", "hotmail.com", "yahoo.com"]

SUBSCRIPTION_PLANS = ["Basic", "Pro", "Enterprise"]
SUBSCRIPTION_WEIGHTS = [0.45, 0.35, 0.20]

CUSTOMER_STATUSES = ["Active", "Inactive", "Churned"]
STATUS_WEIGHTS = [0.70, 0.20, 0.10]

SIGNUP_START = datetime(2023, 1, 1)
SIGNUP_END = datetime(2026, 6, 30)


def _setup_seeds(seed: int) -> dict[str, Faker]:
    """Initialize random and Faker seeds for reproducibility."""
    random.seed(seed)
    Faker.seed(seed)
    locales = set(COUNTRY_LOCALES.values())
    return {locale: Faker(locale) for locale in locales}


def _generate_customer_id(index: int) -> str:
    """Return formatted customer ID (e.g. C001)."""
    return f"C{index:03d}"


def _normalize_for_email(text: str) -> str:
    """Convert a name to an ASCII-safe email local part."""
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    return ascii_text.lower().replace(" ", "")


def _generate_email(
    first_name: str, last_name: str, used_emails: set[str]
) -> str:
    """Generate a unique email address based on the customer's name."""
    base = f"{_normalize_for_email(first_name)}.{_normalize_for_email(last_name)}"
    domain = random.choice(EMAIL_DOMAINS)
    email = f"{base}@{domain}"
    suffix = 1
    while email in used_emails:
        email = f"{base}{suffix}@{random.choice(EMAIL_DOMAINS)}"
        suffix += 1
    used_emails.add(email)
    return email


def _random_signup_date() -> str:
    """Return a random signup date within the configured range."""
    day_range = (SIGNUP_END - SIGNUP_START).days
    signup = SIGNUP_START + timedelta(days=random.randint(0, day_range))
    return signup.strftime("%Y-%m-%d")


def _generate_name(
    country: str,
    fakers: dict[str, Faker],
    used_names: set[tuple[str, str]],
) -> tuple[str, str]:
    """Generate first and last names consistent with the customer's country."""
    locale = COUNTRY_LOCALES[country]
    fake = fakers[locale]
    for _ in range(50):
        first_name = fake.first_name()
        last_name = fake.last_name()
        if (first_name, last_name) not in used_names:
            used_names.add((first_name, last_name))
            return first_name, last_name
    first_name = fake.first_name()
    last_name = fake.last_name()
    used_names.add((first_name, last_name))
    return first_name, last_name


def generate_customers(
    num_customers: int = NUM_CUSTOMERS,
    seed: int = SEED,
    output_path: Path = OUTPUT_PATH,
) -> pd.DataFrame:
    """
    Generate customer records and save them to CSV.

    Args:
        num_customers: Number of unique customers to generate.
        seed: Seed value for reproducible output.
        output_path: Destination path for the CSV file.

    Returns:
        DataFrame containing the generated customer records.
    """
    fakers = _setup_seeds(seed)
    used_emails: set[str] = set()
    used_names: set[tuple[str, str]] = set()
    records = []

    for index in range(1, num_customers + 1):
        country = random.choices(COUNTRIES, weights=COUNTRY_WEIGHTS, k=1)[0]
        first_name, last_name = _generate_name(country, fakers, used_names)
        records.append(
            {
                "customer_id": _generate_customer_id(index),
                "first_name": first_name,
                "last_name": last_name,
                "email": _generate_email(first_name, last_name, used_emails),
                "country": country,
                "subscription_plan": random.choices(
                    SUBSCRIPTION_PLANS, weights=SUBSCRIPTION_WEIGHTS, k=1
                )[0],
                "customer_status": random.choices(
                    CUSTOMER_STATUSES, weights=STATUS_WEIGHTS, k=1
                )[0],
                "signup_date": _random_signup_date(),
            }
        )

    customers = pd.DataFrame(records)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    customers.to_csv(output_path, index=False)
    print(f"Generated {len(customers)} customers -> {output_path}")
    return customers


if __name__ == "__main__":
    generate_customers()
