# COLAS COMPARTIDAS: FIFO ENLAZADA Y COLA DE PRIORIDAD
# El frente conserva el siguiente elemento que saldrá y el final permite
# agregar uno nuevo sin recorrer los nodos que ya están esperando.


class Nodo:
    def __init__(self, elemento):
        self.elemento = elemento
        self.siguiente = None


class Cola:
    def __init__(self):
        self._frente = None
        self._final = None
        self._cantidad = 0

    # Conecta el nuevo nodo al final para conservar el orden FIFO. Mantener
    # una referencia al último evita recorrer la cola en cada inserción; si está
    # vacía, el nuevo nodo también se convierte en el frente.
    def enqueue(self, elemento):
        nuevo = Nodo(elemento)
        if self.is_empty():
            self._frente = nuevo
        else:
            self._final.siguiente = nuevo
        self._final = nuevo
        self._cantidad += 1

    # Retira y devuelve el frente sin desplazar los demás elementos. Al sacar
    # el último nodo se limpia también el final, evitando conservar una referencia
    # retirada cuando la cola vuelva a utilizarse.
    def dequeue(self):
        if self.is_empty():
            raise IndexError("La cola está vacía")
        primero = self._frente
        self._frente = primero.siguiente
        primero.siguiente = None
        self._cantidad -= 1
        if self.is_empty():
            self._final = None
        return primero.elemento

    # Consulta el próximo elemento sin cambiar enlaces ni cantidad de registros.
    def front(self):
        if self.is_empty():
            raise IndexError("La cola está vacía")
        return self._frente.elemento

    def is_empty(self):
        return self._cantidad == 0

    # El contador evita recorrer toda la lista cada vez que se pregunta su tamaño.
    def size(self):
        return self._cantidad

    # Recorre los nodos para consultar el orden de atención. La lista resultante
    # sirve para mostrar los datos sin desencolar ni modificar sus enlaces.
    def en_orden(self):
        elementos = []
        actual = self._frente
        while actual is not None:
            elementos.append(actual.elemento)
            actual = actual.siguiente
        return elementos


# Esta cola de prioridad se comparte con emergencias e impresoras para conservar
# la misma regla: 1 es la prioridad más alta y los empates mantienen su llegada.
class ColaPrioridad:
    def __init__(self):
        self._elementos = []

    # Guarda pares de prioridad y elemento, ordenados de mayor a menor número.
    # La nueva llegada se inserta antes de los empates: al retirar desde el final,
    # sale primero la prioridad 1 y, entre iguales, quien llegó antes.
    def enqueue(self, elemento, prioridad):
        if type(prioridad) is not int or not 1 <= prioridad <= 5:
            raise ValueError("La prioridad debe ser un entero entre 1 y 5")
        posicion = 0
        while posicion < len(self._elementos) and self._elementos[posicion][0] > prioridad:
            posicion += 1
        self._elementos.insert(posicion, (prioridad, elemento))

    # Extraer desde el final evita desplazar los registros que siguen esperando.
    # El par retirado contiene prioridad y elemento; se devuelve sólo el elemento
    # para que emergencias e impresoras trabajen directamente con sus datos.
    def dequeue(self):
        if self.is_empty():
            raise IndexError("La cola de prioridad está vacía")
        return self._elementos.pop()[1]

    def front(self):
        if self.is_empty():
            raise IndexError("La cola de prioridad está vacía")
        return self._elementos[-1][1]

    def is_empty(self):
        return not self._elementos

    def size(self):
        return len(self._elementos)

    def en_orden(self):
        return [elemento for prioridad, elemento in reversed(self._elementos)]
