import json
import heapq

# MODELO
class Transmetro:
    def __init__(self):
        self.grafo = {}

    def agregar(self, origen, destino, tiempo, tipo, transbordo=0):
        self.grafo.setdefault(origen, []).append({
            "destino": destino,
            "tiempo": tiempo,
            "tipo": tipo,
            "transbordo": transbordo
        })

        self.grafo.setdefault(destino, []).append({
            "destino": origen,
            "tiempo": tiempo,
            "tipo": tipo,
            "transbordo": transbordo
        })


# BASE DE CONOCIMIENTO
class BC:
    def __init__(self):
        self.reglas = []

    def add(self, r):
        self.reglas.append(r)

    def evaluar(self, d):
        return sum(r(d) for r in self.reglas)


# REGLAS
def r_tiempo(d):
    return d["tiempo"]

def r_transbordo(d):
    return d.get("transbordo", 0) * 10

def r_tipo(d):
    return -3 if d["tipo"] == "troncal" else 3


# MOTOR
def ruta_optima(tm, bc, inicio, fin):
    cola = [(0, inicio, [])]
    visitados = set()

    while cola:
        costo, nodo, ruta = heapq.heappop(cola)

        if nodo in visitados:
            continue

        ruta = ruta + [nodo]

        if nodo == fin:
            return ruta, costo

        visitados.add(nodo)

        for vecino in tm.grafo.get(nodo, []):
            nuevo = costo + bc.evaluar(vecino)

            heapq.heappush(
                cola,
                (nuevo, vecino["destino"], ruta)
            )

    return None, float("inf")


# DATOS DESDE JSON

def cargar_datos(archivo):
    tm = Transmetro()

    with open(archivo, "r", encoding="utf-8") as f:
        data = json.load(f)

        for c in data["conexiones"]:
            tm.agregar(
                c["origen"],
                c["destino"],
                c["tiempo"],
                c["tipo"],
                c.get("transbordo", 0)
            )

    return tm


# MENÚ INTERACTIVO
def mostrar_estaciones(tm):
    estaciones = list(tm.grafo.keys())
    for i, est in enumerate(estaciones):
        print(f"{i+1}. {est}")
    return estaciones


def seleccionar_estacion(estaciones, mensaje):
    while True:
        try:
            opcion = int(input(mensaje))
            if 1 <= opcion <= len(estaciones):
                return estaciones[opcion - 1]
        except:
            pass
        print("❌ Opción inválida, intenta de nuevo.")


# PROGRAMA PRINCIPAL
def main():
    tm = cargar_datos("datos.json")

    bc = BC()
    bc.add(r_tiempo)
    bc.add(r_transbordo)
    bc.add(r_tipo)

    print("\n🚍 SISTEMA TRANSMETRO - RUTAS INTELIGENTES\n")

    estaciones = mostrar_estaciones(tm)

    inicio = seleccionar_estacion(estaciones, "\nSeleccione punto de inicio: ")
    fin = seleccionar_estacion(estaciones, "Seleccione destino: ")

    ruta, costo = ruta_optima(tm, bc, inicio, fin)

    if ruta:
        print("\n✅ Ruta óptima:")
        print(" → ".join(ruta))
        print("Costo:", costo)
    else:
        print("❌ No se encontró ruta.")


if __name__ == "__main__":
    main()