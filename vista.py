from PyQt5.QtCore import QTimer, QTime, pyqtSignal
from PyQt5.QtGui import QColor
from threading import Thread
from PyQt5 import uic
import time
import sys

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QHeaderView,
    QTableWidgetItem,
)


def obtener_hora(ventana):
    while True:
        hora_actual = QTime.currentTime().toString("hh:mm:ss")
        ventana.actualizar_hora.emit(hora_actual)
        time.sleep(1)


class VentanaPrincipal(QMainWindow):
    actualizar_hora = pyqtSignal(str)

    def __init__(self):
        super(VentanaPrincipal, self).__init__()
        uic.loadUi("interfaz.ui", self)

        # iniciar hilo para la hora
        self.hilo_hora = Thread(target=obtener_hora, args=(self,))
        self.hilo_hora.daemon = True  # se hace un hilo "demonio", se ejecuta en segundo plano y finaliza al cerrar

        # inicializar widgets
        for row in range(2):
            text = "S.O." if row == 0 else ""
            self.tablaMemoria.setItem(row, 0, QTableWidgetItem(text))
            self.tablaMemoria.item(row, 0).setBackground(QColor("skyblue"))

        self.tablaMemoria.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # la ventana principal
        self.hilo_hora.start()

        # conectar hilo a la señal del método que sirve para actualizar la hora
        self.actualizar_hora.connect(self.actualizar_label_hora)

    def actualizar_label_hora(self, hora):
        # actualizar el label con la hora
        self.lblHora.setText(hora)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mi_app = VentanaPrincipal()
    mi_app.show()
    sys.exit(app.exec_())
