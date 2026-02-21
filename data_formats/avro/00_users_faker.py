#!/usr/bin/env python3
"""
Generate fake user data for testing purposes.
Outputs JSON to stdout, allowing shell redirection.
Uses constant memory O(1) through streaming generation.

Usage:
    python 00_faker.py 1000 > data/test_data.json
    python 00_faker.py 50000 --progress --compact > data/large.json
    python 00_faker.py 50000 | python 01_avro_writer.py
"""

import sys
import json
import random
import argparse
from typing import Iterator
from faker import Faker


def draw_progress_bar(current: int, total: int, bar_width: int = 40) -> None:
    """
    Draw a progress bar with percentage in the middle.

    Args:
        current: Current progress count
        total: Total count
        bar_width: Width of the progress bar in characters
    """
    percentage = int((current / total) * 100)
    filled = int((current / total) * bar_width)

    # Format the percentage text
    percent_text = f"{percentage}%"

    # Calculate position to center the percentage text
    text_len = len(percent_text)
    text_start = (bar_width // 2) - (text_len // 2)
    text_end = text_start + text_len

    # Build the progress bar character by character
    progress_bar_str = ""

    for i in range(bar_width):
        if text_start <= i < text_end:  # Display percentage text
            text_idx = i - text_start

            if text_idx < len(percent_text):
                progress_bar_str += percent_text[text_idx]
        elif i < filled:  # Filled portion
            progress_bar_str += "█"
        else:  # Empty portion
            progress_bar_str += "░"

    # Print with carriage return to overwrite previous line
    print(
        f"\r[{progress_bar_str}] ({current}/{total}) records",
        end="",
        file=sys.stderr,
        flush=True,
    )


def generate_users_stream(
    count: int, null_email_probability: float = 0.1, show_progress: bool = False
) -> Iterator[dict]:
    """
    Generate fake user data as an iterator (streaming mode).
    Uses constant memory O(1) regardless of count.

    Args:
        count: Number of user records to generate
        null_email_probability: Probability of email being null (0.0-1.0)
        show_progress: Show progress bar to stderr

    Yields:
        User dictionaries one at a time
    """
    fake = Faker("es_ES")

    # Determine update interval based on count (same logic as Rust version)
    if count < 1000:
        update_interval = 100
    elif count < 10000:
        update_interval = 500
    else:
        update_interval = 1000

    for i in range(count):
        # Progress indicator to stderr
        if show_progress and ((i + 1) % update_interval == 0 or (i + 1) == count):
            draw_progress_bar(i + 1, count, 40)

        user = {
            "name": fake.name(),
            "age": random.randint(18, 90),
            "email": fake.email() if random.random() > null_email_probability else None,
        }

        yield user

    if show_progress:
        print(file=sys.stderr)  # New line after progress bar


def main():
    parser = argparse.ArgumentParser(
        description="Generate fake user data in JSON format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 1000                           # Generate 1,000 records to stdout
  %(prog)s 50000 > large_data.json        # Generate 50,000 records to file
  %(prog)s 100000 --null-rate 0.2         # 20%% of emails will be null
  %(prog)s 10000 --progress               # Show progress bar
  %(prog)s 500000 --progress --compact    # Progress bar with compact output
  %(prog)s 10000 | jq '.[0:5]'            # Generate and pipe to jq
        """,
    )

    parser.add_argument("count", type=int, help="Number of user records to generate")

    parser.add_argument(
        "--null-rate",
        type=float,
        default=0.1,
        metavar="RATE",
        help="Probability of email being null (default: 0.1)",
    )

    parser.add_argument(
        "--compact", action="store_true", help="Output compact JSON (no indentation)"
    )

    parser.add_argument(
        "--progress", action="store_true", help="Show progress bar (to stderr)"
    )

    args = parser.parse_args()

    # Validate arguments
    if args.count <= 0:
        parser.error("count must be a positive integer")

    if not 0.0 <= args.null_rate <= 1.0:
        parser.error("--null-rate must be between 0.0 and 1.0")

    # Inform user (to stderr) only if progress is enabled
    if args.progress:
        print(f"Generating {args.count:,} user records...", file=sys.stderr)

    # Generate and stream data directly to stdout (constant memory usage)
    indent_str = "" if args.compact else "  "

    # Start JSON array
    sys.stdout.write("[")

    # Generate and write users one at a time
    for i, user in enumerate(
        generate_users_stream(args.count, args.null_rate, args.progress)
    ):
        # Add comma before every element except the first
        if i > 0:
            sys.stdout.write(",")

        # Add newline for pretty-print mode
        if not args.compact:
            sys.stdout.write("\n")
            sys.stdout.write(indent_str)

        # Serialize and write the user object
        json.dump(user, sys.stdout, ensure_ascii=False)

        # Flush periodically to enable streaming to pipes
        if (i + 1) % 1000 == 0:
            sys.stdout.flush()

    # Close JSON array
    if not args.compact:
        sys.stdout.write("\n")
    sys.stdout.write("]\n")
    sys.stdout.flush()

    # Final message only if progress is enabled
    if args.progress:
        print(f"Done! Generated {args.count:,} records", file=sys.stderr)


if __name__ == "__main__":
    main()
