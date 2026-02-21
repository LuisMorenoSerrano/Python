#
# Simple calc
#

# Define integer input function
def input_number(msg):
    while True:
        try:
            user_input = int(input(msg))
        except ValueError:
            print("Not an integer! Try again.")
        else:
            break

    return user_input

# Inquire two numbers and sum both
x       = input_number("Enter the first number.: ")
y       = input_number("Enter the second number: ")
result  = x + y

# Show result
print(str(x) + " + " + str(y) + " = " + str(result))
