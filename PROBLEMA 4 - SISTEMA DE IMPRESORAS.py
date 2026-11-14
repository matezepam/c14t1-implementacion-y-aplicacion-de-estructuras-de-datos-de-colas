# PROBLEMA 4 - GESTIÓN DE IMPRESORAS EN RED
# Los trabajos esperan según prioridad y cada impresora utiliza una cola FIFO
# con los que ya recibió, conservando compatibilidad y orden de asignación.

from COLA import Cola, ColaPrioridad


class Impresora:
    def __init__(self, nombre, tipos):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("La impresora necesita un nombre")
        if not isinstance(tipos, (list, tuple)) or not tipos:
            raise ValueError("La impresora necesita nombre y tipos de documento")
        if any(not isinstance(tipo, str) or not tipo.strip() for tipo in tipos):
            raise ValueError("Los tipos de documento deben ser textos no vacíos")
        self.nombre = nombre.strip()
        self.tipos = tuple(tipo.strip().lower() for tipo in tipos)
        self.cola = Cola()
        self.carga = 0

    def acepta(self, tipo):
        return tipo in self.tipos

    # Comprueba la compatibilidad y guarda una copia con sus páginas restantes.
    # Esto permite registrar el avance sin modificar el documento original ni
    # asignarlo a una impresora que no admita su tipo.
    def agregar_trabajo(self, trabajo):
        if not self.acepta(trabajo["tipo"]):
            raise ValueError("La impresora no admite ese tipo de documento")
        if type(trabajo["paginas"]) is not int or trabajo["paginas"] <= 0:
            raise ValueError("Las páginas deben ser un entero positivo")
        self.cola.enqueue(dict(trabajo, restante=trabajo["paginas"]))
        self.carga += trabajo["paginas"]

    # Avanza una página del trabajo frontal y reduce la carga pendiente.
    # front permite mantenerlo en su turno hasta terminar; dequeue lo retira
    # sólo al completar la última página, conservando FIFO en esa impresora.
    def imprimir_pagina(self):
        if self.cola.is_empty():
            return None
        trabajo = self.cola.front()
        trabajo["restante"] -= 1
        self.carga -= 1
        if trabajo["restante"] == 0:
            terminado = self.cola.dequeue()
            return terminado["id"]
        return None


class SistemaImpresion:
    def __init__(self, impresoras):
        if not impresoras:
            raise ValueError("Se necesita al menos una impresora")
        self.impresoras = list(impresoras)
        self.pendientes = ColaPrioridad()
        self._siguiente_id = 1

    # Valida usuario, páginas y compatibilidad antes de encolar. Un documento
    # que ninguna impresora admite se rechaza para evitar una espera indefinida;
    # el ID aumenta únicamente después de aceptar el trabajo.
    def enviar_trabajo(self, usuario, tipo, paginas, prioridad):
        if not isinstance(usuario, str) or not usuario.strip():
            raise ValueError("El trabajo necesita un usuario")
        if not isinstance(tipo, str) or not tipo.strip():
            raise ValueError("El documento necesita un tipo")
        tipo = tipo.strip().lower()
        if type(paginas) is not int or paginas <= 0:
            raise ValueError("Las páginas deben ser un entero positivo")
        if not any(impresora.acepta(tipo) for impresora in self.impresoras):
            raise ValueError(f"No existe una impresora compatible con {tipo}")
        trabajo = {"id": self._siguiente_id, "usuario": usuario.strip(),
                   "tipo": tipo, "paginas": paginas, "prioridad": prioridad}
        self.pendientes.enqueue(trabajo, prioridad)
        self._siguiente_id += 1
        return trabajo["id"]

    # Extrae el lote por prioridad y busca la impresora compatible menos cargada.
    # Si empatan, prefiere la que admite menos tipos para reservar la más flexible.
    # Así reparte las páginas sin enviar documentos a equipos incompatibles.
    def distribuir_trabajos(self):
        asignaciones = []
        while not self.pendientes.is_empty():
            trabajo = self.pendientes.dequeue()
            compatibles = [i for i in self.impresoras if i.acepta(trabajo["tipo"])]
            elegida = min(compatibles, key=lambda i: (i.carga, len(i.tipos)))
            elegida.agregar_trabajo(trabajo)
            asignaciones.append((trabajo["id"], trabajo["usuario"], elegida.nombre))
        return asignaciones

    def hay_trabajos(self):
        return not self.pendientes.is_empty() or any(not i.cola.is_empty() for i in self.impresoras)

    # Cada unidad simulada permite imprimir una página a todas las impresoras.
    # El ciclo representa su avance en paralelo sin hilos ni esperas reales y
    # devuelve los trabajos completados para informar el resultado del turno.
    def ejecutar_turno(self):
        if not self.pendientes.is_empty():
            self.distribuir_trabajos()
        completados = []
        for impresora in self.impresoras:
            identificador = impresora.imprimir_pagina()
            if identificador is not None:
                completados.append((impresora.nombre, identificador))
        return completados

    def mostrar_colas(self):
        for impresora in self.impresoras:
            trabajos = [(t["id"], t["restante"]) for t in impresora.cola.en_orden()]
            print(f"{impresora.nombre} | Cola: {trabajos} | Páginas pendientes: {impresora.carga}")


def demostracion():
    sistema = SistemaImpresion([
        Impresora("Texto", ("texto",)),
        Impresora("Multifunción", ("texto", "imagen")),
    ])
    trabajos = [("Ana", "texto", 4, 2), ("Luis", "imagen", 3, 1),
                ("Marta", "texto", 2, 1), ("Pedro", "texto", 1, 3),
                ("Sofía", "imagen", 2, 2), ("Diego", "texto", 2, 2)]
    print("PROBLEMA 4 - IMPRESORAS EN RED")
    print("Entrada: usuario, tipo, páginas y prioridad")
    for trabajo in trabajos:
        identificador = sistema.enviar_trabajo(*trabajo)
        print("Trabajo", identificador, ":", trabajo)
    try:
        sistema.enviar_trabajo("Eva", "plano", 1, 1)
    except ValueError as error:
        print("Trabajo rechazado:", error)
    print("\nASIGNACIÓN POR PRIORIDAD")
    for identificador, usuario, impresora in sistema.distribuir_trabajos():
        print(f"Trabajo {identificador} de {usuario} -> {impresora}")
    sistema.mostrar_colas()
    turno = 0
    while sistema.hay_trabajos():
        turno += 1
        for impresora, identificador in sistema.ejecutar_turno():
            print(f"Turno {turno}: {impresora} completó el trabajo {identificador}")
    print("Turnos de impresión:", turno)
    sistema.mostrar_colas()


if __name__ == "__main__":
    demostracion()
