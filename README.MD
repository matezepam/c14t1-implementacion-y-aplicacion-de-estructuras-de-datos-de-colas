# C14T1 · Implementación y aplicación de estructuras de datos de colas

Cuatro ejercicios en Python sobre colas FIFO, circulares y de prioridad. Las demostraciones tienen datos definidos para poder repetir y comparar los resultados; no necesitan ingresar información por teclado. Puedes cambiar esos datos en la función `demostracion()` de cada archivo.

## Instalación

Instala Python 3.

## Ejecución

Clona el repositorio y entra a su carpeta:

```bash
git clone https://github.com/matezepam/c14t1-implementacion-y-aplicacion-de-estructuras-de-datos-de-colas.git
cd c14t1-implementacion-y-aplicacion-de-estructuras-de-datos-de-colas
```

Ejecuta el problema que quieras revisar:

```bash
python "PROBLEMA 1 - COLA BASICA.py"
python "PROBLEMA 2 - COLA CIRCULAR.py"
python "PROBLEMA 3 - COLA EMERGENCIAS.py"
python "PROBLEMA 4 - SISTEMA DE IMPRESORAS.py"
```

Mantén todos los archivos en la misma carpeta y conserva las comillas al ejecutar los nombres con espacios.

```text
PROBLEMA 1 - COLA BASICA.py              Demostración de la cola enlazada
PROBLEMA 2 - COLA CIRCULAR.py            Planificación Round Robin
PROBLEMA 3 - COLA EMERGENCIAS.py         Atención por urgencia y llegada
PROBLEMA 4 - SISTEMA DE IMPRESORAS.py    Distribución e impresión de trabajos
COLA.py                              Estructuras compartidas entre problemas
PRUEBAS.py                           Pruebas de métodos y simulaciones
README.MD                            Ejecución, ejemplos y análisis
```

## Problema 1 - Cola básica

`Cola` utiliza nodos con un elemento y una referencia al siguiente. Conserva referencias al frente y al final para insertar y retirar sin recorrer la lista. Un contador permite consultar el tamaño directamente.

| Método | Función |
| --- | --- |
| `enqueue(elemento)` | Añade al final |
| `dequeue()` | Retira y devuelve el primer elemento |
| `front()` | Consulta el primero sin retirarlo |
| `is_empty()` | Indica si está vacía |
| `size()` | Devuelve la cantidad de elementos |
| `en_orden()` | Devuelve una lista para mostrar el contenido sin extraerlo |

La entrada de ejemplo es Documento A, Documento B y Documento C, en ese orden. Parte de la salida:

```text
Después de enqueue: ['Documento A', 'Documento B', 'Documento C']
Front sin extraer: Documento A
Tamaño después de front: 3
Dequeue: Documento A | Restantes: 2
Dequeue: Documento B | Restantes: 1
Dequeue: Documento C | Restantes: 0
Extracción en cola vacía: La cola está vacía
Cola reutilizada: ['Documento D']
```

`front()` y `dequeue()` lanzan `IndexError` cuando no hay elementos. Al retirar el último nodo también se limpia el final, de modo que la cola pueda reutilizarse correctamente.

## Problema 2 - Cola circular y Round Robin

`ColaCircular` utiliza una lista de capacidad fija, índices de frente y final y un contador. Los índices avanzan con módulo para reutilizar las posiciones liberadas, sin desplazar procesos. Además de los métodos básicos, incluye `is_full()`, `agregar_proceso(nombre, tiempo)` y `ejecutar_turno()`.

La simulación comienza con cinco procesos: P1 necesita 5 unidades, P2 necesita 8, P3 necesita 2, P4 necesita 6 y P5 necesita 4. Todos llegan al inicio. El quantum es **3 unidades**: se retira el primero, se consume como máximo ese tiempo y, si todavía necesita CPU, vuelve al final. Un proceso que necesita menos de tres unidades consume solamente su tiempo restante.

La salida muestra la cola después de cada ejecución. Por ejemplo, el primer turno produce:

```text
P1: ejecuta 3 | resta 2 | reloj 3
Cola restante: [('P2', 8), ('P3', 2), ('P4', 6), ('P5', 4), ('P1', 2)]
```

Después de diez turnos:

```text
Orden de finalización: ['P3', 'P1', 'P4', 'P5', 'P2']
Tiempo total: 25
```

Se rechazan capacidades, tiempos y quantum que no sean enteros positivos. Insertar en una cola llena lanza `OverflowError`; consultar o retirar de una vacía lanza `IndexError`. El contador permite distinguir llena y vacía aunque los índices coincidan.

## Problema 3 - Emergencias

`ColaEmergencias` registra nombre, urgencia y turno de llegada. `agregar_paciente()` incorpora al paciente, `atender_paciente()` devuelve y retira al siguiente y `mostrar_espera()` muestra el orden actual sin modificarlo. La urgencia debe ser un entero entre 1 y 5; **1 es la más urgente**.

La clase reutiliza `ColaPrioridad`, definida en `COLA.py`. Esta mantiene una lista ordenada y coloca cada nueva llegada antes de los empates dentro del almacenamiento. Como la extracción se realiza desde el final, sale primero la urgencia más alta y, entre iguales, quien llegó antes. Compartir esa regla con las impresoras evita duplicar código.

Entrada de la demostración:

```text
Ana 3, Luis 1, Marta 2, Pedro 1,
Sofía 5, Diego 3, Elena 2, Carla 4
```

Salida de atención:

```text
Atendido: Luis | Urgencia 1
Atendido: Pedro | Urgencia 1
Atendido: Marta | Urgencia 2
Atendido: Elena | Urgencia 2
Atendido: Ana | Urgencia 3
Atendido: Diego | Urgencia 3
Atendido: Carla | Urgencia 4
Atendido: Sofía | Urgencia 5
No hay pacientes esperando
```

Luis conserva su turno antes que Pedro, aunque ambos tengan urgencia 1. Los nombres vacíos y las urgencias inválidas se rechazan antes de avanzar el número de turno.

## Problema 4 - Impresoras en red

Se implementa la opción A con dos tipos de colas: una **cola de prioridad** para los trabajos pendientes de asignación y una **cola FIFO enlazada** en cada impresora para los trabajos ya asignados.

`SistemaImpresion.enviar_trabajo()` recibe usuario, tipo, páginas y prioridad. Valida los datos y rechaza documentos que ninguna impresora admite. `distribuir_trabajos()` toma primero los más urgentes, respetando la llegada en los empates, y escoge la impresora compatible con menos páginas pendientes. Si hay empate de carga, prefiere la que admite menos tipos de documento para reservar la más flexible.

Cada llamada a `ejecutar_turno()` representa una unidad de tiempo: todas las impresoras avanzan una página de su trabajo frontal. `front()` permite mantener ese trabajo hasta terminarlo y `dequeue()` lo retira después de imprimir la última página. La simulación no usa hilos ni esperas reales.

Hay dos impresoras: Texto admite texto y Multifunción admite texto e imagen. La entrada contiene seis trabajos:

| ID | Usuario | Tipo | Páginas | Prioridad |
| --- | --- | --- | --- | --- |
| 1 | Ana | texto | 4 | 2 |
| 2 | Luis | imagen | 3 | 1 |
| 3 | Marta | texto | 2 | 1 |
| 4 | Pedro | texto | 1 | 3 |
| 5 | Sofía | imagen | 2 | 2 |
| 6 | Diego | texto | 2 | 2 |

Parte de la salida esperada:

```text
Trabajo rechazado: No existe una impresora compatible con plano

ASIGNACIÓN POR PRIORIDAD
Trabajo 2 de Luis -> Multifunción
Trabajo 3 de Marta -> Texto
Trabajo 1 de Ana -> Texto
Trabajo 5 de Sofía -> Multifunción
Trabajo 6 de Diego -> Multifunción
Trabajo 4 de Pedro -> Texto
Texto | Cola: [(3, 2), (1, 4), (4, 1)] | Páginas pendientes: 7
Multifunción | Cola: [(2, 3), (5, 2), (6, 2)] | Páginas pendientes: 7
```

Las 14 páginas terminan en **7 turnos**, utilizando ambas impresoras. La salida también indica cuándo finaliza cada trabajo y muestra las colas vacías al terminar.

El ejemplo distribuye un lote recibido antes de comenzar la impresión. La prioridad se aplica al asignar trabajos pendientes; los que ya están en una impresora conservan FIFO y no se interrumpen por nuevas llegadas. Elegir la menor carga es una regla sencilla para repartir trabajo, aunque no garantiza la mejor planificación posible para cualquier combinación de documentos e impresoras.

## Comparación de las implementaciones

`n` es la cantidad de elementos almacenados y `C` la capacidad reservada de la cola circular.

| Operación | Simple enlazada | Circular con arreglo fijo | Prioridad con lista ordenada |
| --- | --- | --- | --- |
| Insertar | O(1) | O(1), si hay espacio | O(n) |
| Retirar | O(1) | O(1) | O(1) amortizado |
| Consultar frente | O(1) | O(1) | O(1) |
| Consultar tamaño o vacío | O(1) | O(1) | O(1) |
| Obtener contenido en orden | O(n) | O(n) | O(n) |
| Memoria de la estructura | O(n) | O(C) | O(n) |

La cola enlazada crece según la cantidad de elementos y no desplaza los restantes al retirar. Cada nodo necesita una referencia adicional, por lo que resulta adecuada para turnos o trabajos cuyo número cambia durante la ejecución.

La circular reserva O(C) posiciones al crearse y reutiliza ese espacio. Conviene para buffers y procesos con una capacidad conocida. Su límite debe elegirse de antemano y puede reservar posiciones que no se utilicen.

La de prioridad permite atender primero lo urgente, conservando FIFO en empates. La lista ordenada es sencilla de comprender, pero insertar requiere buscar la posición y puede desplazar elementos. Retirar desde el final evita el desplazamiento de una extracción en el índice cero; `pop()` tiene coste amortizado constante en Python. Es útil en emergencias y trabajos con distinta importancia. Si llegan continuamente elementos urgentes, los de menor prioridad pueden esperar mucho tiempo.

### Coste de las simulaciones

- **Cola básica:** insertar y retirar `n` elementos cuesta O(n) en total y ocupa O(n) memoria.
- **Round Robin:** si `T` es la suma de los turnos necesarios por proceso, planificar cuesta O(T), además de O(C) para crear el arreglo. Mostrar hasta `p` procesos después de cada turno añade O(Tp) en el peor caso. La memoria es O(C + p), contando la lista de nombres finalizados.
- **Emergencias:** insertar `n` pacientes cuesta O(n²) en el peor caso; atenderlos a todos cuesta O(n). Consultar la lista de espera cuesta O(n) y la memoria utilizada es O(n).
- **Impresoras:** para `J` trabajos, `I` impresoras y `T` turnos, las inserciones en prioridad cuestan O(J²) en el peor caso, la distribución O(JI) y la impresión O(TI). Mostrar las colas cuesta O(J + I). La memoria es O(J + I), considerando una cantidad fija de tipos admitidos por impresora.

Las listas devueltas para mostrar información requieren espacio temporal proporcional a su contenido. Estos costes incluyen los recorridos de presentación: mostrar una cola completa no es una operación constante.

## Pruebas

```bash
python PRUEBAS.py
```

Las 28 pruebas revisan FIFO, consultas sin extracción, colas vacías y llenas, reutilización de nodos y posiciones circulares, validación de datos, empates de prioridad, los cinco procesos de Round Robin, los ocho pacientes y la compatibilidad y finalización de los trabajos de impresión. También comparan secuencias de operaciones intercaladas con resultados de referencia.

El resultado correcto termina en:

```text
Ran 28 tests in ...s

OK
```
