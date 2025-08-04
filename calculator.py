# 🧮 Basic addition-only Calculator Program

# Asks the user to input two numbers
num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))

# Asks the user to choose an operation
operation = input("Enter the operation (+): ")

# Performs the selected operation and display the result
if operation == "+":
    result = num1 + num2
    print(f"{num1} + {num2} = {result}")

else:
    print("Invalid operation. Please enter +.")
