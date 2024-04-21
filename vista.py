import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5 import uic
from PyQt5.QtCore import QTimer, QTime, pyqtSignal
from threading import Thread
import time


def obtener_hora(ventana):
    while True:
        hora_actual = QTime.currentTime().toString("hh:mm:ss")
        ventana.actualizar_hora.emit(hora_actual)
        time.sleep(1)


class VentanaPrincipal(QMainWindow):
    actualizar_hora = pyqtSignal(str)

    def __init__(self):
        super(VentanaPrincipal, self).__init__()
        uic.loadUi('interfaz.ui', self)

        # iniciar hilo para la hora
        self.hilo_hora = Thread(target=obtener_hora, args=(self,))
        self.hilo_hora.daemon = True  # se hace un hilo "demonio", se ejecuta en segundo plano y finaliza al cerrar
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
