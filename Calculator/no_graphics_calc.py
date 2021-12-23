text = """========================================
Enter \"quit\" as an expression to quit
========================================"""

print(text)
expression = input("Enter the math expression: ")
while expression != "quit":
    try:
        result = "Result is: " + str(eval(expression))
    except:
        result = "Expression format mistake or division by zero"
    print(result)
    expression = input("Enter the math expression: ")
