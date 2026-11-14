# Las pruebas comparan el orden de atención y el estado después de cada cambio,
# incluyendo vacíos, límites y empates que no siempre se observan en la demostración.

from collections import deque
from contextlib import redirect_stdout
from pathlib import Path
import io
import random
import runpy
import unittest

from COLA import Cola, ColaPrioridad

RAIZ = Path(__file__).resolve().parent
# run_path permite cargar los archivos con espacios sin ejecutar sus demostraciones.
ColaCircular = runpy.run_path(str(RAIZ / "PROBLEMA 2 - COLA CIRCULAR.py"))["ColaCircular"]
ColaEmergencias = runpy.run_path(str(RAIZ / "PROBLEMA 3 - COLA EMERGENCIAS.py"))["ColaEmergencias"]
impresion = runpy.run_path(str(RAIZ / "PROBLEMA 4 - SISTEMA DE IMPRESORAS.py"))
Impresora = impresion["Impresora"]
SistemaImpresion = impresion["SistemaImpresion"]


class PruebasCola(unittest.TestCase):
    def test_vacia(self):
        cola = Cola()
        self.assertTrue(cola.is_empty())
        self.assertEqual(cola.size(), 0)
        with self.assertRaises(IndexError):
            cola.front()
        with self.assertRaises(IndexError):
            cola.dequeue()

    # Consultar el frente no debe contar como una atención ni cambiar el orden.
    def test_fifo_y_front(self):
        cola = Cola()
        for elemento in ("A", "B", "C"):
            cola.enqueue(elemento)
        self.assertEqual(cola.front(), "A")
        self.assertEqual(cola.size(), 3)
        self.assertEqual([cola.dequeue() for _ in range(3)], ["A", "B", "C"])

    def test_reutilizar_despues_del_ultimo(self):
        cola = Cola()
        cola.enqueue("Único")
        self.assertEqual(cola.dequeue(), "Único")
        self.assertIsNone(cola._frente)
        self.assertIsNone(cola._final)
        cola.enqueue("Nuevo")
        self.assertEqual(cola.front(), "Nuevo")
        self.assertEqual(cola.size(), 1)

    def test_elementos_y_consulta_independiente(self):
        cola = Cola()
        for elemento in (None, 0, False, ""):
            cola.enqueue(elemento)
        vista = cola.en_orden()
        vista.clear()
        self.assertEqual(cola.size(), 4)
        self.assertEqual([cola.dequeue() for _ in range(4)], [None, 0, False, ""])

    # La cola de referencia sólo se usa como comparación, la implementación
    # evaluada conserva sus propios nodos y referencias de frente y final.
    def test_operaciones_intercaladas(self):
        cola, referencia = Cola(), deque()
        generador = random.Random(14)
        for _ in range(500):
            if not referencia or generador.random() < 0.6:
                valor = generador.randrange(100)
                cola.enqueue(valor)
                referencia.append(valor)
            else:
                self.assertEqual(cola.dequeue(), referencia.popleft())
            self.assertEqual(cola.en_orden(), list(referencia))
            self.assertEqual(cola.size(), len(referencia))
            if referencia:
                self.assertEqual(cola.front(), referencia[0])


class PruebasPrioridad(unittest.TestCase):
    def test_orden_y_empates(self):
        cola = ColaPrioridad()
        for nombre, prioridad in (("A", 3), ("B", 1), ("C", 2), ("D", 1), ("E", 3)):
            cola.enqueue(nombre, prioridad)
        self.assertEqual(cola.front(), "B")
        self.assertEqual(cola.en_orden(), ["B", "D", "C", "A", "E"])
        self.assertEqual([cola.dequeue() for _ in range(5)], ["B", "D", "C", "A", "E"])

    def test_vacia(self):
        cola = ColaPrioridad()
        self.assertTrue(cola.is_empty())
        with self.assertRaises(IndexError):
            cola.front()
        with self.assertRaises(IndexError):
            cola.dequeue()

    def test_prioridades_invalidas(self):
        cola = ColaPrioridad()
        for prioridad in (0, 6, -1, True, 1.5, "1"):
            with self.assertRaises(ValueError):
                cola.enqueue("Paciente", prioridad)
        self.assertEqual(cola.size(), 0)

    def test_nuevas_llegadas(self):
        cola = ColaPrioridad()
        cola.enqueue("Primero", 2)
        cola.enqueue("Segundo", 2)
        self.assertEqual(cola.dequeue(), "Primero")
        cola.enqueue("Urgente", 1)
        cola.enqueue("Tercero", 2)
        self.assertEqual(cola.en_orden(), ["Urgente", "Segundo", "Tercero"])

    def test_prioridades_con_llegadas_variadas(self):
        generador = random.Random(15)
        cola, entradas = ColaPrioridad(), []
        for turno in range(200):
            prioridad = generador.randint(1, 5)
            cola.enqueue(turno, prioridad)
            entradas.append((prioridad, turno))
        esperado = [turno for prioridad, turno in sorted(entradas)]
        self.assertEqual([cola.dequeue() for _ in entradas], esperado)


class PruebasCircular(unittest.TestCase):
    def test_capacidad_invalida(self):
        for capacidad in (0, -1, True, 2.5, "3"):
            with self.assertRaises(ValueError):
                ColaCircular(capacidad)

    def test_vacia_y_llena(self):
        cola = ColaCircular(2)
        with self.assertRaises(IndexError):
            cola.front()
        with self.assertRaises(IndexError):
            cola.dequeue()
        cola.enqueue("A")
        cola.enqueue("B")
        self.assertTrue(cola.is_full())
        with self.assertRaises(OverflowError):
            cola.enqueue("C")
        self.assertEqual(cola.en_orden(), ["A", "B"])

    # Después de circular, el orden lógico debe continuar en B, C y D aunque
    # parte de esos elementos haya vuelto a las primeras posiciones del arreglo.
    def test_reutilizacion_circular(self):
        cola = ColaCircular(3)
        for elemento in ("A", "B", "C"):
            cola.enqueue(elemento)
        self.assertEqual(cola.dequeue(), "A")
        cola.enqueue("D")
        self.assertEqual(cola.en_orden(), ["B", "C", "D"])
        self.assertEqual([cola.dequeue() for _ in range(3)], ["B", "C", "D"])
        self.assertEqual(cola._datos, [None, None, None])

    def test_capacidad_uno(self):
        cola = ColaCircular(1)
        for valor in (None, 0, "Proceso"):
            cola.enqueue(valor)
            self.assertTrue(cola.is_full())
            self.assertEqual(cola.front(), valor)
            self.assertEqual(cola.dequeue(), valor)
            self.assertTrue(cola.is_empty())

    def test_vueltas_intercaladas(self):
        cola, referencia = ColaCircular(7), deque()
        generador = random.Random(16)
        for _ in range(500):
            if not referencia or len(referencia) < 7 and generador.random() < 0.6:
                valor = generador.randrange(100)
                cola.enqueue(valor)
                referencia.append(valor)
            else:
                self.assertEqual(cola.dequeue(), referencia.popleft())
            self.assertEqual(cola.en_orden(), list(referencia))
            self.assertEqual(cola.size(), len(referencia))
            self.assertEqual(cola.is_full(), len(referencia) == 7)

    def test_round_robin_cinco_procesos(self):
        cola = ColaCircular(5)
        for nombre, tiempo in (("P1", 5), ("P2", 8), ("P3", 2), ("P4", 6), ("P5", 4)):
            cola.agregar_proceso(nombre, tiempo)
        turnos, finalizados, total = [], [], 0
        while not cola.is_empty():
            nombre, consumo, restante = cola.ejecutar_turno()
            self.assertTrue(1 <= consumo <= 3)
            self.assertGreaterEqual(restante, 0)
            turnos.append(nombre)
            total += consumo
            if restante == 0:
                finalizados.append(nombre)
        self.assertEqual(turnos, ["P1", "P2", "P3", "P4", "P5", "P1", "P2", "P4", "P5", "P2"])
        self.assertEqual(finalizados, ["P3", "P1", "P4", "P5", "P2"])
        self.assertEqual(total, 25)

    def test_validacion_sin_perder_procesos(self):
        cola = ColaCircular(1)
        for tiempo in (0, -1, True, 1.5):
            with self.assertRaises(ValueError):
                cola.agregar_proceso("P1", tiempo)
        cola.agregar_proceso("P1", 2)
        for quantum in (0, -1, True, 1.5):
            with self.assertRaises(ValueError):
                cola.ejecutar_turno(quantum)
            self.assertEqual(cola.front()["restante"], 2)
        self.assertEqual(cola.ejecutar_turno(), ("P1", 2, 0))
        with self.assertRaises(IndexError):
            cola.ejecutar_turno()


class PruebasEmergencias(unittest.TestCase):
    def crear_ejemplo(self):
        cola = ColaEmergencias()
        for paciente in (("Ana", 3), ("Luis", 1), ("Marta", 2), ("Pedro", 1),
                         ("Sofía", 5), ("Diego", 3), ("Elena", 2), ("Carla", 4)):
            cola.agregar_paciente(*paciente)
        return cola

    def test_ocho_pacientes(self):
        cola = self.crear_ejemplo()
        self.assertEqual(cola.size(), 8)
        self.assertEqual(cola.front()["nombre"], "Luis")
        nombres = [cola.atender_paciente()["nombre"] for _ in range(8)]
        self.assertEqual(nombres, ["Luis", "Pedro", "Marta", "Elena", "Ana", "Diego", "Carla", "Sofía"])

    def test_mostrar_no_extrae(self):
        cola = self.crear_ejemplo()
        antes = cola.lista_espera()
        salida = io.StringIO()
        with redirect_stdout(salida):
            cola.mostrar_espera()
        self.assertEqual(cola.lista_espera(), antes)
        self.assertIn("Turno 2 | Luis | Urgencia 1", salida.getvalue())

    def test_validacion_y_turnos(self):
        cola = ColaEmergencias()
        with self.assertRaises(ValueError):
            cola.agregar_paciente(" ", 1)
        with self.assertRaises(ValueError):
            cola.agregar_paciente("Ana", 6)
        self.assertEqual(cola.agregar_paciente("Ana", 3), 1)
        self.assertEqual(cola.agregar_paciente("Luis", 3), 2)
        self.assertEqual(cola.atender_paciente()["turno"], 1)
        self.assertEqual(cola.atender_paciente()["turno"], 2)

    def test_vacia(self):
        cola = ColaEmergencias()
        self.assertTrue(cola.is_empty())
        with self.assertRaises(IndexError):
            cola.atender_paciente()
        with self.assertRaises(IndexError):
            cola.front()
        salida = io.StringIO()
        with redirect_stdout(salida):
            cola.mostrar_espera()
        self.assertIn("No hay pacientes", salida.getvalue())


class PruebasImpresoras(unittest.TestCase):
    def crear_sistema(self):
        return SistemaImpresion([
            Impresora("Texto", ("texto",)),
            Impresora("Multifunción", ("texto", "imagen")),
        ])

    def test_impresoras_invalidas(self):
        for tipos in ((), "texto", ("",)):
            with self.assertRaises(ValueError):
                Impresora("Impresora", tipos)
        with self.assertRaises(ValueError):
            SistemaImpresion([])

    def test_rechazos_sin_encolar(self):
        sistema = self.crear_sistema()
        for usuario, tipo, paginas, prioridad in (
            ("Ana", "plano", 1, 1), ("", "texto", 1, 1),
            ("Ana", "texto", 0, 1), ("Ana", "texto", 1, 6),
        ):
            with self.assertRaises(ValueError):
                sistema.enviar_trabajo(usuario, tipo, paginas, prioridad)
        self.assertEqual(sistema.pendientes.size(), 0)
        self.assertEqual(sistema.enviar_trabajo("Ana", "texto", 1, 1), 1)

    def test_desempate_reserva_flexibilidad(self):
        sistema = self.crear_sistema()
        sistema.enviar_trabajo("Ana", "texto", 2, 1)
        sistema.enviar_trabajo("Luis", "imagen", 2, 1)
        self.assertEqual(sistema.distribuir_trabajos(), [(1, "Ana", "Texto"), (2, "Luis", "Multifunción")])

    # Las colas de las impresoras conservan la asignación y el tipo compatible,
    # mientras las páginas pendientes permiten comprobar el reparto de la carga.
    def test_lote_y_compatibilidad(self):
        sistema = self.crear_sistema()
        for trabajo in (("Ana", "texto", 4, 2), ("Luis", "imagen", 3, 1),
                        ("Marta", "texto", 2, 1), ("Pedro", "texto", 1, 3),
                        ("Sofía", "imagen", 2, 2), ("Diego", "texto", 2, 2)):
            sistema.enviar_trabajo(*trabajo)
        asignados = sistema.distribuir_trabajos()
        self.assertEqual([a[0] for a in asignados], [2, 3, 1, 5, 6, 4])
        self.assertEqual([i.carga for i in sistema.impresoras], [7, 7])
        for impresora in sistema.impresoras:
            self.assertTrue(all(impresora.acepta(t["tipo"]) for t in impresora.cola.en_orden()))
        completados, turnos = [], 0
        while sistema.hay_trabajos():
            turnos += 1
            completados.extend(sistema.ejecutar_turno())
        self.assertEqual(turnos, 7)
        self.assertEqual(sorted(t for nombre, t in completados), [1, 2, 3, 4, 5, 6])
        self.assertTrue(all(i.carga == 0 and i.cola.is_empty() for i in sistema.impresoras))

    def test_frente_se_conserva_hasta_terminar(self):
        impresora = Impresora("Texto", ("texto",))
        trabajo = {"id": 1, "usuario": "Ana", "tipo": "texto", "paginas": 2, "prioridad": 1}
        impresora.agregar_trabajo(trabajo)
        impresora.agregar_trabajo(dict(trabajo, id=2, paginas=1))
        self.assertIsNone(impresora.imprimir_pagina())
        self.assertEqual(impresora.cola.front()["id"], 1)
        self.assertEqual(impresora.imprimir_pagina(), 1)
        self.assertEqual(impresora.imprimir_pagina(), 2)
        self.assertIsNone(impresora.imprimir_pagina())
        self.assertNotIn("restante", trabajo)

    def test_turno_distribuye_pendientes(self):
        sistema = self.crear_sistema()
        sistema.enviar_trabajo("Ana", "texto", 1, 1)
        self.assertEqual(sistema.ejecutar_turno(), [("Texto", 1)])
        self.assertFalse(sistema.hay_trabajos())
        self.assertEqual(sistema.ejecutar_turno(), [])

    def test_consulta_no_avanza_impresion(self):
        sistema = self.crear_sistema()
        sistema.enviar_trabajo("Ana", "texto", 2, 1)
        sistema.distribuir_trabajos()
        with redirect_stdout(io.StringIO()):
            sistema.mostrar_colas()
        self.assertEqual(sistema.impresoras[0].carga, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
