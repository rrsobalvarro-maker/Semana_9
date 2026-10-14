pila = []

def apilar():
    codigo = input("Ingrese el código de la caja: ").strip()

    if codigo == "":
        print("El código no puede estar vacío.")
    elif codigo in pila:
        print("El código ya existe en la pila.")
    else:
        pila.append(codigo)
        print("Caja apilada correctamente.")

def desapilar():
    if len(pila) == 0:
        print("No hay cajas para retirar.")
    else:
        caja = pila.pop()
        print(f"Caja retirada: {caja}")

def consultar_tope():
    if len(pila) == 0:
        print("La pila está vacía.")
    else:
        print(f"Caja en el tope: {pila[-1]}")
        
def mostrar_pila():
    if len(pila) == 0:
        print("La pila está vacía.")
    else:
        mensaje = " "
        for caja in reversed(pila):
            mensaje += f"| {caja :>6}|\n"
            mensaje += f"└" + "─"*7 + "┘\n"
        print(mensaje)
            
def menu():
    while True:
        print("=== Menú ===")
        print("1. Apilar")
        print("2. Desapilar")
        print("3. Consultar Tope")
        print("4. Mostrar Pila")
        print("5. Salir")
        opcion = int(input("Digite su opcion (#): "))
        if opcion == 1:
            apilar()
        elif opcion == 2:
            desapilar()
        elif opcion == 3:
            consultar_tope()
        elif opcion == 4:
            mostrar_pila()
        elif opcion == 5:
            print("Saliendo...")
            break
        else: 
            print("Opcion Invalida")
            
menu()