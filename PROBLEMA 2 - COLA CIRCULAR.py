# PROBLEMA 2 - COLA CIRCULAR Y ROUND ROBIN
# El arreglo conserva su capacidad y reutiliza sus posiciones mediante módulo,
# volviendo a colocar al final los procesos que todavía necesitan tiempo de CPU.

QUANTUM = 3


class ColaCircular:
    def __init__(self, capacidad):
        if type(capacidad) is not int or capacidad <= 0:
            raise ValueError("La capacidad debe ser un entero positivo")
        self._datos = [None] * capacidad
        self._capacidad = capacidad
        self._frente = 0
        self._final = 0
        self._cantidad = 0

    # Inserta donde indica el final y avanza con módulo. Al alcanzar el último
    # índice vuelve a cero, reutilizando posiciones libres sin mover los procesos.
    # La comprobación de capacidad evita sobrescribir un elemento pendiente.
    def enqueue(self, elemento):
        if self.is_full():
            raise OverflowError("La cola circular está llena")
        self._datos[self._final] = elemento
        self._final = (self._final + 1) % self._capacidad
        self._cantidad += 1

    # Retira el frente y libera su celda antes de avanzar circularmente.
    # El contador distingue vacía de llena aunque ambos índices coincidan,
    # evitando confundir una cola completa con una que ya no tiene procesos.
    def dequeue(self):
        if self.is_empty():
            raise IndexError("La cola circular está vacía")
        elemento = self._datos[self._frente]
        self._datos[self._frente] = None
        self._frente = (self._frente + 1) % self._capacidad
        self._cantidad -= 1
        return elemento

    def front(self):
        if self.is_empty():
            raise IndexError("La cola circular está vacía")
        return self._datos[self._frente]

    def is_empty(self):
        return self._cantidad == 0

    def is_full(self):
        return self._cantidad == self._capacidad

    def size(self):
        return self._cantidad

    # La consulta sigue el orden lógico de atención y no el orden físico del
    # arreglo, que puede tener elementos al final y al inicio después de circular.
    def en_orden(self):
        return [self._datos[(self._frente + i) % self._capacidad]
                for i in range(self._cantidad)]

    # Valida los datos antes de encolar para que un tiempo inválido no ocupe
    # una posición ni produzca turnos que no puedan avanzar.
    def agregar_proceso(self, nombre, tiempo):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El proceso necesita un nombre")
        if type(tiempo) is not int or tiempo <= 0:
            raise ValueError("El tiempo de ejecución debe ser un entero positivo")
        self.enqueue({"nombre": nombre.strip(), "restante": tiempo})

    # Ejecuta como máximo el quantum y devuelve nombre, consumo y tiempo restante.
    # Si el proceso no terminó, lo coloca al final para dar turno a los demás.
    # Usar el menor tiempo evita consumir tres unidades cuando sólo necesita una.
    def ejecutar_turno(self, quantum=QUANTUM):
        if type(quantum) is not int or quantum <= 0:
            raise ValueError("El quantum debe ser un entero positivo")
        proceso = self.dequeue()
        consumido = min(quantum, proceso["restante"])
        proceso["restante"] -= consumido
        if proceso["restante"] > 0:
            self.enqueue(proceso)
        return proceso["nombre"], consumido, proceso["restante"]


def demostracion():
    cola = ColaCircular(5)
    procesos = [("P1", 5), ("P2", 8), ("P3", 2), ("P4", 6), ("P5", 4)]
    for nombre, tiempo in procesos:
        cola.agregar_proceso(nombre, tiempo)
    print("PROBLEMA 2 - ROUND ROBIN")
    print("Entrada:", procesos, "| Quantum:", QUANTUM)
    print("Cola llena al comenzar:", cola.is_full())
    reloj = 0
    finalizados = []
    while not cola.is_empty():
        print("\nSiguiente proceso:", cola.front()["nombre"])
        nombre, consumido, restante = cola.ejecutar_turno()
        reloj += consumido
        print(f"{nombre}: ejecuta {consumido} | resta {restante} | reloj {reloj}")
        print("Cola restante:", [(p["nombre"], p["restante"]) for p in cola.en_orden()])
        if restante == 0:
            finalizados.append(nombre)
    print("\nOrden de finalización:", finalizados)
    print("Tiempo total:", reloj)


if __name__ == "__main__":
    demostracion()
