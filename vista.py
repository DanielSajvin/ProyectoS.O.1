from PyQt5.QtCore import QTime, pyqtSignal
from proceso import proceso
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
    actualizar_memoria = pyqtSignal(int)
    actualizar_resultados = pyqtSignal(int)

    def __init__(self):
        self.data = None
        self.time_start = None
        self.data_display = None

        super(VentanaPrincipal, self).__init__()
        uic.loadUi("interfaz.ui", self)

        # iniciar hilo para la hora
        self.hilo_hora = Thread(target=obtener_hora, args=(self,))
        self.hilo_hora.daemon = True  # se hace un hilo "demonio", se ejecuta en segundo plano y finaliza al cerrar

        # inicializar widgets
        self.showMaximized()

        # set the memory size to 23
        self.tablaMemoria.setRowCount(23)
        for row in range(self.tablaMemoria.rowCount()):
            self.tablaMemoria.setVerticalHeaderItem(row, QTableWidgetItem(hex(row)))

        for row in range(2):
            self.tablaMemoria.setItem(row, 0, QTableWidgetItem("S.O."))
            self.tablaMemoria.item(row, 0).setBackground(QColor("skyblue"))

        self.tablaMemoria.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tablaProcesos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tablaResultados.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        # la ventana principal
        self.hilo_hora.start()

        # interacciones de usuario
        self.pushButtonIniciar.clicked.connect(self.iniciar_procesos)
        self.botonEstablecer.clicked.connect(self.establecer_cantidad_procesos)

        # conectar hilo a la señal del método que sirve para actualizar la hora
        self.actualizar_hora.connect(self.actualizar_label_hora)
        self.actualizar_memoria.connect(self.actualizar_tabla_memoria)
        self.actualizar_resultados.connect(self.actualizar_tabla_resultados)

    def actualizar_label_hora(self, hora):
        # actualizar el label con la hora
        self.lblHora.setText(hora)

    def actualizar_tabla_memoria(self, registry):
        # Change the color of the row in 'tablaMemoria' where the text equals the executing id
        rango = self.tablaMemoria.rowCount() - 1
        for row in range(rango):
            item = self.tablaMemoria.item(row, 0)
            if item and item.text() != "":
                self.tablaMemoria.item(row, 0).setBackground(
                    QColor("lightgreen")
                    if item.text() == str(self.data_display[registry].id)
                    else QColor("skyblue")
                )

                if (
                    item.text() == str(self.data_display[registry].id)
                    and self.data_display[registry].estado == "Finalizado"
                ):
                    self.tablaMemoria.item(row, 0).setBackground(QColor("white"))
                    self.tablaMemoria.item(row, 0).setText("")

    def actualizar_tabla_resultados(self, registry):
        self.tablaResultados.setItem(
            registry, 1, QTableWidgetItem(self.data_display[registry].estado)
        )

        if self.data_display[registry].estado == "Finalizado":
            self.tablaResultados.setItem(
                registry,
                3,
                QTableWidgetItem(self.data_display[registry].finalizacion),
            )

        self.tablaResultados.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

    def inicializar_tabla_memoria(self):
        # initializes on 2 because OS occupies 2 memory slots
        total_rows = 2

        for data in self.data:
            data.base = hex(total_rows)

            for i in range(total_rows, int(data.rafaga) + total_rows):
                if total_rows <= self.tablaMemoria.rowCount() - 1:
                    self.tablaMemoria.setItem(i, 0, QTableWidgetItem(data.id))
                    self.tablaMemoria.item(i, 0).setBackground(QColor("skyblue"))

                    total_rows += 1

                else:
                    QMessageBox.critical(self, "Error", "La memoria está llena")

            data.limite = hex(total_rows - 1)

    def inicializar_tabla_resultados(self):
        self.tablaResultados.setRowCount(len(self.data))

        for row, data in enumerate(self.data):
            self.tablaResultados.setItem(row, 0, QTableWidgetItem(str(data.id)))
            self.tablaResultados.setItem(row, 1, QTableWidgetItem(data.estado))
            self.tablaResultados.setItem(
                row,
                2,
                QTableWidgetItem(
                    self.time_start.addSecs(int(data.llegada)).toString("hh:mm:ss")
                ),
            )
            self.tablaResultados.setItem(row, 3, QTableWidgetItem("0"))

        self.tablaResultados.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

    def ejecutar_round_robin(self):
        try:
            quantum = 2
            while self.data:
                for i in range(len(self.data)):
                    # Process the task for a maximum of quantum units
                    self.data[i].rafaga = max(0, int(self.data[i].rafaga) - quantum)

                    program_counter = i + 1 if i + 1 < len(self.data) else 0

                    data_display_index = 0
                    for data_display in self.data_display:
                        if data_display.id == self.data[i].id:
                            break

                        data_display_index += 1

                    self.lineEditBase.setText(str(self.data[i].base))
                    self.lineEditLimite.setText(str(self.data[i].limite))
                    self.lineEditContadorP.setText(str(self.data[program_counter].base))
                    self.lineEditPlanificador.setText(str(self.data[i].id))
                    self.actualizar_memoria.emit(data_display_index)

                    self.data_display[data_display_index].estado = "Ejecucion"
                    self.actualizar_resultados.emit(data_display_index)

                    time.sleep(2)

                    self.data_display[data_display_index].estado = "Listo"
                    self.actualizar_resultados.emit(data_display_index)

                    # If the task is finished, remove it from the list
                    if self.data[i].rafaga == 0:
                        self.data_display[data_display_index].finalizacion = (
                            QTime.currentTime().toString("hh:mm:ss")
                        )
                        self.data_display[data_display_index].estado = "Finalizado"

                        self.actualizar_memoria.emit(data_display_index)
                        self.actualizar_resultados.emit(data_display_index)
                        self.data.pop(i)
                        break

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

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

            self.data = sorted(self.data, key=lambda x: x.llegada)
            self.data_display = self.data.copy()

            self.tablaProcesos.setEnabled(False)
            self.pushButtonIniciar.setEnabled(False)

            self.inicializar_tabla_memoria()
            self.inicializar_tabla_resultados()

            round_robin = threading.Thread(target=self.ejecutar_round_robin)
            round_robin.daemon = True
            round_robin.start()

    def establecer_cantidad_procesos(self):
        cantidad_procesos = int(self.inputCantidadP.text())

        self.tablaResultados.setRowCount(cantidad_procesos)
        self.tablaProcesos.setRowCount(cantidad_procesos)
        self.groupCantidadP.setEnabled(False)
        self.widget.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mi_app = VentanaPrincipal()
    mi_app.show()
    sys.exit(app.exec_())