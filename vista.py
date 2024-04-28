from PyQt5.QtCore import QTime, pyqtSignal
from roundRobin import proceso
from PyQt5.QtGui import QColor
from threading import Thread
from PyQt5 import uic
import threading
import time
import sys

from PyQt5.QtWidgets import (
    QTableWidgetItem,
    QApplication,
    QHeaderView,
    QMessageBox,
    QMainWindow,
)


def obtener_hora(ventana):
    while True:
        hora_actual = QTime.currentTime().toString("hh:mm:ss")
        ventana.actualizar_hora.emit(hora_actual)
        time.sleep(1)


class VentanaPrincipal(QMainWindow):
    actualizar_hora = pyqtSignal(str)

    def __init__(self):
        self.data = None
        self.time_start = None
        self.finished_process = []

        super(VentanaPrincipal, self).__init__()
        uic.loadUi("interfaz.ui", self)

        # iniciar hilo para la hora
        self.hilo_hora = Thread(target=obtener_hora, args=(self,))
        self.hilo_hora.daemon = True  # se hace un hilo "demonio", se ejecuta en segundo plano y finaliza al cerrar

        # inicializar widgets
        for row in range(2):
            self.tablaMemoria.setItem(row, 0, QTableWidgetItem("S.O."))
            self.tablaMemoria.item(row, 0).setBackground(QColor("skyblue"))

        self.tablaMemoria.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # la ventana principal
        self.hilo_hora.start()

        # interacciones de usuario
        self.pushButtonIniciar.clicked.connect(self.iniciar_procesos)
        self.botonEstablecer.clicked.connect(self.establecer_cantidad_procesos)

        # conectar hilo a la señal del método que sirve para actualizar la hora
        self.actualizar_hora.connect(self.actualizar_label_hora)

    def actualizar_label_hora(self, hora):
        # actualizar el label con la hora
        self.lblHora.setText(hora)

    def actualizar_tabla_memoria(self):
        # initializes on 2 because OS occupies 2 memory slots
        total_rows = 2
        self.data = sorted(self.data, key=lambda x: x.llegada)

        for data in self.data:
            for i in range(total_rows, int(data.rafaga) + total_rows):
                if total_rows <= 15:
                    self.tablaMemoria.setItem(i, 0, QTableWidgetItem(data.id))
                    self.tablaMemoria.item(i, 0).setBackground(QColor("skyblue"))

                    total_rows += 1

                else:
                    QMessageBox.critical(self, "Error", "La memoria está llena")

    def ejecutar_round_robin(self):
        # try:
        quantum = 2
        while self.data:
            for i in range(len(self.data)):
                # cada proceso se ejecutara un maximo de 2 seg (quantum)
                self.data[i].rafaga = max(0, int(self.data[i].rafaga) - quantum)

                # se actualiza line_edit 'Planificador', proceso en ejecucion
                self.lineEditPlanificador.setText(str(self.data[i].id))

                # cambia el color de la fila en 'tablaMemoria' el texto es igual a a 'id' de ejecucion
                rango = self.tablaMemoria.rowCount() - 1
                for row in range(rango):
                    item = self.tablaMemoria.item(row, 0)
                    if item:
                        self.tablaMemoria.item(row, 0).setBackground(
                            QColor("lightgreen")
                            if item.text() == str(self.data[i].id)
                            else QColor("skyblue")
                        )

                time.sleep(2)

                # si el proceso finalizo, se elimina de la lista
                if self.data[i].rafaga == 0:
                    self.data[i].finalizacion = QTime.currentTime()
                    self.finished_process.append(self.data[i])
                    self.data.pop(i)
                    break
        # except Exception as e:
        #     print(e)

    def actualizar_tabla_resultados(self):
        pass

    def iniciar_procesos(self):
        def check_tablaProcesos():
            for row in range(self.tablaProcesos.rowCount()):
                for column in range(self.tablaProcesos.columnCount()):
                    item = self.tablaProcesos.item(row, column)
                    if item is None or item.text() == "":
                        return False
            return True

        # verificar si tabla no esta vacia
        if check_tablaProcesos:
            self.data = []
            self.time_start = QTime.currentTime()

            for row in range(self.tablaProcesos.rowCount()):
                id = self.tablaProcesos.item(row, 0).text()
                rafaga = self.tablaProcesos.item(row, 2).text()
                llegada = self.tablaProcesos.item(row, 1).text()

                self.data.append(proceso(id, rafaga, llegada))

            self.tablaProcesos.setEnabled(False)
            self.pushButtonIniciar.setEnabled(False)

            self.actualizar_tabla_memoria()

            round_robin = threading.Thread(target=self.ejecutar_round_robin)
            round_robin.daemon = True
            round_robin.start()

    def establecer_cantidad_procesos(self):
        cantidad_procesos = int(self.inputCantidadP.text())

        self.tablaResultados.setRowCount(cantidad_procesos)
        self.tablaProcesos.setRowCount(cantidad_procesos)
        self.groupCantidadP.setEnabled(False)
        self.tablaMemoria.setEnabled(False)
        self.widget.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mi_app = VentanaPrincipal()
    mi_app.show()
    sys.exit(app.exec_())
