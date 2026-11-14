# PROBLEMA 3 - ATENCIÓN DE EMERGENCIAS
# La urgencia determina el orden y las llegadas con igual nivel conservan FIFO,
# utilizando una cola de prioridad compartida en lugar de repetir su implementación.

from COLA import ColaPrioridad


class ColaEmergencias:
    def __init__(self):
        self._cola = ColaPrioridad()
        self._siguiente_turno = 1

    # Registra nombre, urgencia y turno de llegada para identificar los empates.
    # La cola valida la urgencia antes de avanzar el contador, de modo que un
    # registro rechazado no cambie los turnos de los pacientes válidos.
    def agregar_paciente(self, nombre, urgencia):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El paciente necesita un nombre")
        paciente = {"turno": self._siguiente_turno, "nombre": nombre.strip(), "urgencia": urgencia}
        self._cola.enqueue(paciente, urgencia)
        self._siguiente_turno += 1
        return paciente["turno"]

    # Retira al paciente más urgente; ante igual urgencia, sale el que llegó
    # primero. Reutiliza la regla compartida para no repetir la ordenación.
    def atender_paciente(self):
        return self._cola.dequeue()

    def front(self):
        return self._cola.front()

    def is_empty(self):
        return self._cola.is_empty()

    def size(self):
        return self._cola.size()

    # Devuelve turno, nombre y urgencia en el orden de atención sin extraerlos.
    # Las tuplas separan la consulta de los diccionarios internos para que mostrar
    # la lista de espera no cambie los datos ni consuma turnos.
    def lista_espera(self):
        return [(p["turno"], p["nombre"], p["urgencia"]) for p in self._cola.en_orden()]

    def mostrar_espera(self):
        if self.is_empty():
            print("No hay pacientes esperando")
        else:
            for turno, nombre, urgencia in self.lista_espera():
                print(f"Turno {turno} | {nombre} | Urgencia {urgencia}")


def demostracion():
    cola = ColaEmergencias()
    pacientes = [("Ana", 3), ("Luis", 1), ("Marta", 2), ("Pedro", 1),
                 ("Sofía", 5), ("Diego", 3), ("Elena", 2), ("Carla", 4)]
    print("PROBLEMA 3 - EMERGENCIAS")
    print("Entrada:", pacientes)
    for nombre, urgencia in pacientes:
        cola.agregar_paciente(nombre, urgencia)
    print("\nLISTA DE ESPERA")
    cola.mostrar_espera()
    print("Próximo paciente sin extraer:", cola.front()["nombre"])
    print("Pacientes pendientes:", cola.size())
    print("\nATENCIÓN")
    while not cola.is_empty():
        paciente = cola.atender_paciente()
        print(f"Atendido: {paciente['nombre']} | Urgencia {paciente['urgencia']}")
    cola.mostrar_espera()


if __name__ == "__main__":
    demostracion()
