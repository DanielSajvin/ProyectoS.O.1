class proceso(object):

    def __init__(self, id, rafaga, llegada):
        self.id = id
        self.rafaga = rafaga  # tiempo de consumo
        self.llegada = llegada  # tiempo de llegada
        self.rafagatmp = rafaga
        self.estado = "Listo"  # Listo, Ejecucion, Bloqueado, Finalizado
        self.base = 0
        self.limite = 0
        self.espera = 0
        self.retorno = 0
        self.finalizacion = 0
