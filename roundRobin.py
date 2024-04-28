class proceso(object):

    def __init__(self, id, rafaga, llegada):
        self.id = id
        self.rafaga = rafaga  # tiempo de consumo
        self.llegada = llegada  # tiempo de llegada
        self.rafagatmp = rafaga
        self.estado = "Listo"  # Listo, Ejecucion, Bloqueado, Finalizado
        self.espera = 0
        self.retorno = 0
        self.finalizacion = 0


# print("Algoritmo Roun Robin")

# try:
#     # se pide al usuario que ingrese el número de procesos
#     print("Ingrese el numero de procesos")
#     nnumeros = int(input(">"))
#     if (nnumeros > 0):
#         listadeprocesos = []  # lista donde se almacenarán todos los procesos
#         for i in range(nnumeros):
#             tmpllegada = -1
#             # se pide al usuario que ingrese la información de cada proceso
#             print("### Proceso " + str(i + 1) + " ###")
#             while (tmpllegada < 0):
#                 print("Ingrese el tiempo de llegada del proceso")
#                 tmpllegada = int(input(">"))

#             rafagatmp = 0
#             while (rafagatmp < 1):
#                 print("Ingrese el tiempo de consumo del proceso>")
#                 rafagatmp = int(input(">"))
#             # en el arreglo el primer item es el "id del proceso", luego la rafaga(tiempo de llegada) y ultimo la llegada
#             listadeprocesos.append(proceso((i + 1), rafagatmp, tmpllegada))
#             print("### Fin del procesos ####\n\n\n")

#         print("Procesos creados con exito!!\n")

#         quantum = 0
#         swi = False
#         while (quantum < 1):
#             print("Ingrese el Quantum")
#             quantum = int(input(">"))
#         quantumtmp = quantum


#         # metodo para ordenar los procesos por tiempo de llegada
#         def ordenaInsersion(lista):
#             for i in range(1, len(lista)):
#                 j = i
#                 while j > 0 and lista[j].llegada < lista[j - 1].llegada:
#                     lista[j], lista[j - 1] = lista[j - 1], lista[j]
#                     j = j - 1
#             return lista


#         listadeprocesos = ordenaInsersion(listadeprocesos)  # lista reultante de ordenar por tiempo de llegada
#         print("[+] Se ordeno lista de procesos por tiempo de llegada")
#         procesosEspejo = len(listadeprocesos)  # es la variable que controla los procesos que hacen falta por terminar
#         tiempo = 0
#         procesosCola = []
#         procesoEjecusion = None  # variable que corresponde al proceso que actualmente se encuentra en ejecusion
#         nproceso = 0  # variable utilizada para pasar al siguiente
#         print("[+] Se establecieron varibles para el funcionamiento")
#         print("@ Incicio del Algortimo  @")
#         sw = True  # Variable de control
#         while (procesosEspejo > 0):
#             # se revisa si hay procesos nuevos que llegan y se agregan a la cola de listos
#             # se selecciona el próximo proceso de la cola y se ejecuta
#             # se ejecuta el proceso actual hasta que se complete su ráfaga(tiempo de consumo) o se alcance el quantum
#             # se actualizan los tiempos de finalización, retorno y espera del proceso
#             print("---------------- Tiempo [" + str(tiempo) + "]  ---------------")
#             if (len(listadeprocesos) > nproceso and tiempo >= listadeprocesos[nproceso].llegada):
#                 print("[+]El proceso " + str(listadeprocesos[nproceso].id) + " se ingreso a la cola de listos")
#                 procesosCola.append(listadeprocesos[nproceso])
#                 nproceso = nproceso + 1

#             else:
#                 if nproceso > 0 or len(procesosCola) > 0:
#                     if (procesoEjecusion == None):
#                         procesoEjecusion = procesosCola.pop(0)
#                         sw = True
#                         print("[+] Se saca el proceso " + str(procesoEjecusion.id) + " de la cola y se ejecuta.")
#                     else:
#                         if (sw):
#                             if (procesoEjecusion.rafagatmp >= quantum):
#                                 procesoEjecusion.rafagatmp = procesoEjecusion.rafagatmp - quantum
#                                 print("[+] Se resta " + str(quantum) + " al tiempo de consumo del proceso " + str(
#                                     procesoEjecusion.id))
#                                 tiempo = tiempo + quantum
#                                 print("[+] Se aumenta" + str(quantum) + " al tiempo")
#                             else:
#                                 tiempo = tiempo + procesoEjecusion.rafagatmp
#                                 print("[+] Se aumenta " + str(procesoEjecusion.rafagatmp) + " al tiempo")
#                                 print("[+] Se resta " + str(
#                                     procesoEjecusion.rafagatmp) + " al tiempo de consumo del proceso " + str(
#                                     procesoEjecusion.id))
#                                 procesoEjecusion.rafagatmp = 0

#                             if (procesoEjecusion.rafagatmp < 1):
#                                 print("---------------- Tiempo [" + str(tiempo) + "]  ---------------")
#                                 print("[+] El Proceso " + str(procesoEjecusion.id) + " finalizo.")
#                                 procesoEjecusion.finalizacion = tiempo
#                                 procesoEjecusion.retorno = procesoEjecusion.finalizacion - procesoEjecusion.llegada
#                                 procesoEjecusion.espera = procesoEjecusion.retorno - procesoEjecusion.rafaga
#                                 procesosEspejo = procesosEspejo - 1
#                                 procesoEjecusion = None

#                             else:
#                                 sw = False
#                         else:
#                             procesosCola.append(procesoEjecusion)
#                             print("[+] Se agrega el proceso " + str(
#                                 procesoEjecusion.id) + " que estaba en ejecusion a la cola de listos")
#                             procesoEjecusion = None
#                 else:
#                     tiempo = tiempo + 1
#         print("---- Algoritmo Finalizado ----\n\n\n")
#         print("!!!! Resultados !!!!\n")
#         totalretorno = 0
#         totalespera = 0
#         for proceso in listadeprocesos:
#             print("Proceso " + str(proceso.id) + ", Finalizo: " + str(proceso.finalizacion) + ", Espera: " + str(
#                 proceso.espera) + " Retorno: " + str(proceso.retorno))
#             totalretorno = totalretorno + proceso.retorno
#             totalespera = totalespera + proceso.espera

#         print("\nPromedio de retorno: " + str(totalretorno / len(listadeprocesos)))
#         print("Promedio de espera: " + str(totalespera / len(listadeprocesos)))
#     else:
#         print("No es valido")
# except Exception as e:
#     print(e)
