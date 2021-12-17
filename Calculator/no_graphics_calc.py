text = """========================================
Enter \"quit\" as an expression to quit
========================================"""

print(text)
expression = input("Enter the math expression: ")
while expression != "quit":
    try:
        result = str(eval(expression))
    except:
        result = "Expression format mistake or division by zero"
    print("Result is: " + result)
    expression = input("Enter the math expression: ")
