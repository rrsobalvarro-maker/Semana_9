historial = []
pagina_actual = ""

def registrar_pagina():
    global pagina_actual
    nueva_pagina = input("Ingrese la URL de la nueva página: ").strip()
    if nueva_pagina == "":
        print("La página no puede estar vacía.")
    else:
        if pagina_actual != "":
            historial.append(pagina_actual)
        pagina_actual = nueva_pagina
        print(f"Página actual: {pagina_actual}")

def regresar_pagina():
    global pagina_actual
    if len(historial) == 0:
        print("No hay páginas anteriores para regresar.")
    else:
        pagina_actual = historial.pop()
        print(f"Regresando a: {pagina_actual}")
        
def consultar_pagina():
    if pagina_actual == "":
        print("No hay ninguna página abierta.")
    else:
        print(f"Página actual: {pagina_actual}")


def mostrar_historial():
    if len(historial) == 0:
        print("No hay páginas anteriores en el historial.")
    else:
        print("\n--- Historial de retroceso ---")
        for pagina in reversed(historial):
            print(pagina)
    print(f"Páginas anteriores disponibles: {len(historial)}")


def menu():
    while True:
        print("=== Menú ===")
        print("1. Registrar página nueva")
        print("2. Regresar a la página anterior")
        print("3. Consultar página actual")
        print("4. Mostrar historial de retroceso")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            registrar_pagina()
        elif opcion == "2":
            regresar_pagina()
        elif opcion == "3":
            consultar_pagina()
        elif opcion == "4":
            mostrar_historial()
        elif opcion == "5":
            print("Cerrando el simulador...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

menu()