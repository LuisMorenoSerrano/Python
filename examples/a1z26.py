import sys
import argparse
import string

def encrypt_a1z26(message: str) -> str:
    message = message.upper()
    result = []

    for character in message:
        if character in string.ascii_uppercase:
            result.append(str(ord(character) - ord('A') + 1))
        elif character == ' ':
            result.append(' ')
        else:
            result.append(character)

    return '-'.join(result)

def decrypt_a1z26(message: str) -> str:
    parts = message.split('-')
    result = []

    for part in parts:
        if part.isdigit():
            num = int(part)
            if 1 <= num <= 26:
                result.append(chr(num + ord('A') - 1))
            else:
                result.append('?')
        elif part == ' ':
            result.append(' ')
        else:
            result.append(part)

    return ''.join(result)

def main():
    class CustomArgParser(argparse.ArgumentParser):
        def error(self, message):
            print(f"\nError: {message}\n")
            print("Correct usage: python a1z26.py (--c | --d) --m <Text>")
            print("\nOptions:")
            print("  --c       Encrypt the message")
            print("  --d       Decrypt the message")
            print("  --m <txt> Message to process\n")

            sys.exit(2)

    parser = CustomArgParser(
        description="A1Z26 encryption and decryption",
        usage="python a1z26.py (--c | --d) --m <Text>"
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--c", action="store_true", help="Encrypt the message")
    group.add_argument("--d", action="store_true", help="Decrypt the message")
    parser.add_argument("--m", required=True, help="Message to process")
    args = parser.parse_args()

    if args.c:
        print(encrypt_a1z26(args.m))
    elif args.d:
        print(decrypt_a1z26(args.m))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
