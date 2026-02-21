largest_number = -999999999
number         = largest_number

while number != -1:
    if number > largest_number:
        largest_number = number

    number = int(input("Enter a number or type -1 to stop: "))

print("The largest number is:", largest_number)
