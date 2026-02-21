#!/usr/bin/env python3
"""
Generate fake user data for testing purposes.
Outputs JSON to stdout, allowing shell redirection.

Usage:
    python 00_faker.py 1000 > data/test_data.json
    python 00_faker.py 50000 | python 01_avro_writer.py
"""

import sys
import json
import random
import argparse
from faker import Faker


def generate_users(count: int, null_email_probability: float = 0.1) -> list[dict]:
    """
    Generate fake user data.

    Args:
        count: Number of user records to generate
        null_email_probability: Probability of email being null (0.0-1.0)

    Returns:
        List of user dictionaries
    """
    fake = Faker('es_ES')
    users = []

    for i in range(count):
        # Progress indicator to stderr (does not interfere with stdout)
        if (i + 1) % 10000 == 0:
            print(f"Generated {i + 1}/{count} records...", file=sys.stderr)

        users.append({
            "name": fake.name(),
            "age": random.randint(18, 90),
            "email": fake.email() if random.random() > null_email_probability else None
        })

    return users


def main():
    parser = argparse.ArgumentParser(
        description="Generate fake user data in JSON format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 1000                           # Generate 1,000 records to stdout
  %(prog)s 50000 > large_data.json        # Generate 50,000 records to file
  %(prog)s 100000 --null-rate 0.2         # 20%% of emails will be null
  %(prog)s 10000 | jq '.[0:5]'            # Generate and pipe to jq
        """
    )

    parser.add_argument(
        'count',
        type=int,
        help='Number of user records to generate'
    )

    parser.add_argument(
        '--null-rate',
        type=float,
        default=0.1,
        metavar='RATE',
        help='Probability of email being null (default: 0.1)'
    )

    parser.add_argument(
        '--compact',
        action='store_true',
        help='Output compact JSON (no indentation)'
    )

    args = parser.parse_args()

    # Validate arguments
    if args.count <= 0:
        parser.error("count must be a positive integer")

    if not 0.0 <= args.null_rate <= 1.0:
        parser.error("--null-rate must be between 0.0 and 1.0")

    # Inform user (to stderr)
    print(f"Generating {args.count:,} user records...", file=sys.stderr)

    # Generate data
    users = generate_users(args.count, args.null_rate)

    # Output to stdout
    indent = None if args.compact else 2
    json.dump(users, sys.stdout, ensure_ascii=False, indent=indent)

    print(f"\nDone! Generated {len(users):,} records", file=sys.stderr)


if __name__ == "__main__":
    main()
