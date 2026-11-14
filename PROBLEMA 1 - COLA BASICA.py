# PROBLEMA 1 - COLA BÁSICA CON LISTA ENLAZADA
# Importa la cola enlazada que también utilizan las impresoras. Compartirla
# evita repetir los enlaces y permite comprobar una misma implementación FIFO.

from COLA import Cola


def demostracion():
    cola = Cola()
    print("PROBLEMA 1 - COLA BÁSICA")
    print("Vacía al comenzar:", cola.is_empty())
    for elemento in ("Documento A", "Documento B", "Documento C"):
        cola.enqueue(elemento)
    print("Después de enqueue:", cola.en_orden())
    # Consultar el frente debe conservar el tamaño y dejar al primer documento
    # disponible para la siguiente extracción.
    print("Front sin extraer:", cola.front())
    print("Tamaño después de front:", cola.size())
    while not cola.is_empty():
        print("Dequeue:", cola.dequeue(), "| Restantes:", cola.size())
    try:
        cola.dequeue()
    except IndexError as error:
        print("Extracción en cola vacía:", error)
    # Volver a insertar tras vaciarla comprueba que frente y final se restauran.
    cola.enqueue("Documento D")
    print("Cola reutilizada:", cola.en_orden())


if __name__ == "__main__":
    demostracion()
