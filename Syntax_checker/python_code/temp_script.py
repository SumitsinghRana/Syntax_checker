
arr = [1, 2, 3]
print(arr[5])  # IndexError (out of bounds)
    
def test():
    x = 5 / 0  # ZeroDivisionError
    if True:
        print("This condition is always true!")  # Logical error
    return

test()
