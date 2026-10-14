stack = []

def push(page):
    stack.append(page)
    return f"Visitar: {page}"
    
def peek():
    return f"Mostrar actual {stack[-1]}"

def pop():
    return f"Regresar > {stack.pop()}"
    
def show():
    message = " "
    for page in reversed(stack):
        message += f"| {page :>6}|\n"
        message += f"└" + "─"*8 + "┘\n"
    
    