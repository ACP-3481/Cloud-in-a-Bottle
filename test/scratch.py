x = 10

def modify_global():
    global x
    x = 20

print(x)  # Output: 10
modify_global()
print(x)  # Output: 20