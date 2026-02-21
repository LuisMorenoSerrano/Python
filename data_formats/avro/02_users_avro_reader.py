#!/usr/bin/env python3
"""
Read and display Avro binary user data.

Usage:
    python 02_users_avro_reader.py data/users.avro
    python 02_users_avro_reader.py data/large_users.avro --limit 10
    python 02_users_avro_reader.py input.avro --no-header
"""

import sys
import argparse
from typing import Any, cast
from pathlib import Path
from fastavro import reader

# Column width constants
NAME_WIDTH = 40
AGE_WIDTH = 6
TOTAL_WIDTH = 80


def _format_field(rec: dict[str, Any], field: str, default: str = "[MISS]") -> str:
    """Format a field value, handling missing and null cases."""
    if field not in rec:
        return default

    value = rec[field]
    return "-" if value is None else str(value)


def _format_user_row(rec: dict[str, Any], name_width: int, age_width: int) -> str:
    """Format a user record as a table row."""
    name = _format_field(rec, "name")
    age = _format_field(rec, "age")

    # Handle email specially (null vs missing)
    if "email" not in rec:
        email = "[MISS]"
    elif rec["email"] is None:
        email = "-"
    else:
        email = str(rec["email"])

    # Truncate name if too long
    if len(name) > name_width:
        name = name[:name_width-3] + "..."

    return f"{name.ljust(name_width)} │ {age.rjust(age_width)} │ {email}"


def display_users(
    avro_file: Path,
    limit: int | None = None,
    show_header: bool = True,
    name_width: int = NAME_WIDTH,
    age_width: int = AGE_WIDTH
) -> None:
    """
    Read and display users from an Avro file.

    Args:
        avro_file: Path to the Avro file
        limit: Maximum number of records to display (None = all)
        show_header: Whether to show table header
        name_width: Width for name column
        age_width: Width for age column
    """
    with open(avro_file, "rb") as fo:
        avro_reader = reader(fo)

        if (schema := avro_reader.writer_schema) and isinstance(schema, dict):
            print(f"Schema: {schema.get('name', 'Unknown')}\n")

        separator = "─" * TOTAL_WIDTH

        if show_header:
            print(separator)
            print(f"👤 {'NAME'.ljust(name_width-3)} │ 🎂 {'AGE'.center(age_width-3)} │ 📧 EMAIL")
            print(separator)

        count = 0

        for record in avro_reader:
            if limit and count >= limit:
                print(separator)
                print(f"... showing first {limit} of many records")
                break

            rec = cast(dict[str, Any], record)
            print(_format_user_row(rec, name_width, age_width))
            count += 1

        if show_header:
            print(separator)

        print(f"\nTotal records displayed: {count:,}")


def main():
    parser = argparse.ArgumentParser(
        description="Read and display Avro binary user data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s data/users.avro                      # Read default file
  %(prog)s data/large_users.avro --limit 50     # Show first 50 records
  %(prog)s input.avro --no-header               # Without table header
  %(prog)s data/users.avro -l 100               # Show first 100 records
        """
    )

    parser.add_argument(
        'input_file',
        type=Path,
        nargs='?',
        default=None,
        help='Input Avro file (default: data/users.avro)'
    )

    parser.add_argument(
        '-l', '--limit',
        type=int,
        metavar='N',
        help='Display only first N records'
    )

    parser.add_argument(
        '--no-header',
        action='store_true',
        help='Do not display table header'
    )

    args = parser.parse_args()

    # Setup paths
    script_dir = Path(__file__).parent
    data_dir = script_dir / "data"

    # Use provided file or default
    input_file = args.input_file if args.input_file else data_dir / "users.avro"

    # Validate file exists
    if not input_file.exists():
        print(f"Error: File '{input_file}' not found", file=sys.stderr)

        if not args.input_file:
            print("Hint: Run the writer first or specify a valid Avro file", file=sys.stderr)

        sys.exit(1)

    # Validate limit
    if args.limit is not None and args.limit <= 0:
        parser.error("--limit must be a positive integer")

    # Use constant column widths
    name_width = NAME_WIDTH
    age_width = AGE_WIDTH

    print(f"Reading data from {input_file}...\n")

    try:
        display_users(
            input_file,
            limit=args.limit,
            show_header=not args.no_header,
            name_width=name_width,
            age_width=age_width
        )
    except (OSError, IOError) as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
    except (ValueError, KeyError) as e:
        print(f"Error processing Avro data: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
