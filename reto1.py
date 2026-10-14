stack = []

def push(item, capacity):
    if not is_full(capacity):
        stack.append(item)
        return "Elemento apilado"
    return "Pila llena"

def is_empty():
    return not len(stack)

def is_full(capacity):
    return len(stack) == capacity

def peek():
    if not is_empty():
        return stack[-1]
    return "Pila vacia"

def pop():
    if not is_empty():
        return stack.pop()
    return "pila vacia"

def show():
    message = " "
    for item in reversed(stack):
        message += f"| {item :>6}|\n"
        message += f"└" + "─"*8 + "┘\n"
   
def stack_capacity():    
    capacity = int(input("Tamaño de la pila: "))
    while True:
        item = input("Dime un valor: ")
        print(push(item, capacity))
        answer = input("Desea ingresar otro dato [S | N]: ")
        if answer.lower() == "n":
            break

def unstack():
    while True:
        answer = input("Desea desapilar [S | N]: ")
        if answer.lower() == "s":
            print(pop())
        elif answer.lower() == "n":
            break
        else:
            print("Opcion invalida...")