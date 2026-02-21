#!/usr/bin/env python3
"""
Convert JSON user data to Avro binary format.

Usage:
    python 01_users_avro_writer.py
    python 01_users_avro_writer.py input.json -o output.avro
    python 01_users_avro_writer.py data.json --codec deflate
"""

import json
import sys
import argparse
from pathlib import Path
from fastavro import writer, parse_schema


def main():
    parser = argparse.ArgumentParser(
        description="Convert JSON user data to Avro binary format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                         # Use default input
  %(prog)s input.json -o custom_output.avro        # Custom output
  %(prog)s data.json --codec deflate               # With compression
  %(prog)s data.json -s custom_schema.avsc         # Custom schema
        """
    )

    parser.add_argument(
        'input_file',
        type=Path,
        nargs='?',
        default=None,
        help='Input JSON file with user data (default: data/users_data.json)'
    )

    parser.add_argument(
        '-o', '--output',
        type=Path,
        metavar='FILE',
        help='Output Avro file (default: data/users.avro)'
    )

    parser.add_argument(
        '-s', '--schema',
        type=Path,
        metavar='FILE',
        help='Avro schema file (default: data/user_schema.avsc)'
    )

    parser.add_argument(
        '--codec',
        choices=['null', 'deflate', 'snappy', 'bzip2', 'zstandard', 'lz4', 'xz'],
        default='zstandard',
        help='Compression codec (default: zstandard)'
    )

    args = parser.parse_args()

    # Setup paths
    script_dir = Path(__file__).parent
    data_dir = script_dir / "data"
    data_dir.mkdir(exist_ok=True)

    input_file = args.input_file if args.input_file else data_dir / "users_data.json"
    schema_file = args.schema if args.schema else data_dir / "user_schema.avsc"
    output_file = args.output if args.output else data_dir / "users.avro"

    # Validate input file exists
    if not input_file.exists():
        print(f"Error: Input file '{input_file}' not found", file=sys.stderr)
        sys.exit(1)

    if not schema_file.exists():
        print(f"Error: Schema file '{schema_file}' not found", file=sys.stderr)
        sys.exit(1)

    try:
        # 1. Load and parse the schema
        print(f"Loading schema from {schema_file}...")
        with open(schema_file, "r", encoding="utf-8") as f:
            schema_dict = json.load(f)
        parsed_schema = parse_schema(schema_dict)

        # 2. Load user data from JSON file
        print(f"Loading data from {input_file}...")
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        print(f"Loaded {len(data):,} user records")

        # 3. Write in Avro binary format
        print(f"Generating Avro file: {output_file}")
        print(f"Using codec: {args.codec}")

        with open(output_file, "wb") as out:
            writer(out, parsed_schema, data, codec=args.codec)

        # Show file size
        file_size = output_file.stat().st_size
        size_mb = file_size / (1024 * 1024)
        print("✓ Avro file created successfully!")
        print(f"  Size: {file_size:,} bytes ({size_mb:.2f} MB)")

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{input_file}': {e}", file=sys.stderr)
        sys.exit(1)
    except (FileNotFoundError, IOError, OSError) as e:
        print(f"Error: File operation failed: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: Invalid data or schema: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
