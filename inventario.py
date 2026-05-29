"""
 Para desarrollar el problema del inventario.

 """

from MDPs import MDP, iteracion_valor
from math import exp, factorial


class Inventario(MDP):
    """
    MDP para el problema de inventario de Necroelectronica.

    Estados: inventario al final del dia, desde -max_backlog hasta capacidad
    Acciones: cuantas unidades pedir al proveedor (llegan al dia siguiente)
    """

    def __init__(self, gama, lambda_, capacidad=20, max_backlog=10,
                 precio=150, costo_unidad=80, costo_fijo=40,
                 costo_almacen=5, costo_backlog=15):
        self.lambda_ = lambda_
        self.capacidad = capacidad
        self.max_backlog = max_backlog
        self.precio = precio
        self.costo_unidad = costo_unidad
        self.costo_fijo = costo_fijo
        self.costo_almacen = costo_almacen
        self.costo_backlog = costo_backlog

        estados = tuple(range(-max_backlog, capacidad + 1))
        super().__init__(estados, gama)

    def acciones_legales(self, s):
        # se puede pedir desde 0 hasta llenar el almacen al maximo
        return list(range(0, self.capacidad - s + 1))

    def recompensa(self, s, a, s_):
        # TODO: Completar este método
        pass

    def _poisson_pmf(self, k):
        if k < 0:
            return 0.0
        return exp(-self.lambda_) * (self.lambda_ ** k) / factorial(k)

    def prob_transicion(self, s, a, s_):
        disponible = s + a  # inventario al inicio del dia tras recibir el pedido

        if s_ > -self.max_backlog:
            d = disponible - s_  # demanda implicita para llegar a s_
            if d < 0:
                return 0.0
            return self._poisson_pmf(d)
        else:
            # s_ == -max_backlog: la demanda fue tan alta que saturamos el backlog
            # P(D >= disponible + max_backlog)
            d_min = disponible + self.max_backlog
            if d_min <= 0:
                return 1.0
            prob_cola = 0.0
            for d in range(d_min, d_min + 60):
                p = self._poisson_pmf(d)
                prob_cola += p
                if p < 1e-10:
                    break
            return prob_cola

    def es_terminal(self, s):
        # el inventario no tiene estados terminales, opera indefinidamente
        return False


if __name__ == "__main__":

    inventario = Inventario(gama=0.95, lambda_=4)

    pi_star, V = iteracion_valor(inventario, epsilon=1e-4)

    print("-" * 60)
    print("Estado".center(20) + "Acción".center(20) + "Valor".center(20))
    print("-" * 60)
    for s in sorted(pi_star):
        print(f"{s:^20}{pi_star[s]:^20}{V[s]:^20.2f}")
    print("-" * 60)

"""
Contesta las preguntas aquí mismo (has espacio entre las preguntas):

1. ¿Cómo se comporta las transiciones y las ganancias para casos específicos de $s$ y $a$?
2. ¿Qué psa si hay mucho almacen?
3. ¿Que pasa si hay muy poco o estamos sin almacen?
4. ¿Existe un punto donde la ganancia sea máxima?
---
5. ¿Cómo se ve la política óptima? ¿Tiene sentido?
6. ¿Como se comporta la función de valor de estado V(s)?
7. ¿Cómo cambiaría la política si la variabilidad de la demanda (lambda) aumenta de 4 a 8?

"""
