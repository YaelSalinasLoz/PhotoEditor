import sys # sirve para importar modulos de otros archivos .py
from PyQt6.uic import loadUi # sirve para cargar el archivo .ui
from PyQt6 import QtWidgets # sirve para cargar la aplicacion
from PyQt6.QtWidgets import * # sirve para cargar los widgets
from PyQt6.QtSql import * # sirve para cargar la base de datos 
from PyQt6.QtCore import * # sirve para cargar los hilos
from PyQt6.QtGui import * # sirve para cargar los iconos
from os import getcwd # sirve para obtener la ruta del archivo
import cv2 as cv # sirve para cargar la libreria de opencv
import numpy as np # sirve para cargar la libreria de numpy
import matplotlib.pyplot as plt  # sirve para cargar la libreria de matplotlib
import os # sirve para cargar la libreria de os

# Variable global para saber si hay una imagen cargada 
imagen_cargada_global = False
hay_histograma_global = False

class WelcomeScreen(QMainWindow): # Clase para la ventana de bienvenida
    def __init__(self):
        super(WelcomeScreen, self).__init__() # Inicializa la clase padre
        loadUi("VentanaInicio.ui", self) # Carga la ventana de inicio
        self.pushButton_2.clicked.connect(self.gotoEditor) # Boton para ir al editor
        self.pushButton_3.clicked.connect(self.exit) # Boton para salir
        self.pushButton.clicked.connect(self.gotoHowToUse) # Boton para ir a como usar
        #Eliminar barra de titulo
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)


    def gotoEditor(self): # Funcion para ir al editor
        editor = Editor() # Crea una instancia de la clase Editor
        widget.addWidget(editor) # Agrega la instancia a la lista de widgets
        widget.setCurrentIndex(widget.currentIndex() + 1) # Cambia el widget actual
    
    def exit(self): # Funcion para salir
        sys.exit() # Cierra la aplicacion

    def gotoHowToUse(self): # Funcion para ir a como usar
        howToUse = HowToUse() # Crea una instancia de la clase HowToUse
        widget.addWidget(howToUse) # Agrega la instancia a la lista de widgets
        widget.setCurrentIndex(widget.currentIndex() + 1) # Cambia el widget actual


class Editor(QMainWindow): # Clase para la ventana del editor
    def __init__(self): # Constructor de la clase
        super(Editor, self).__init__() # Inicializa la clase padre
        loadUi("Editor_ventana.ui", self) # Carga la ventana del editor
        self.salir_boton.clicked.connect(self.exit) # Boton para salir
        self.selecc_boton.clicked.connect(self.seleccionar) # Boton para seleccionar una imagen
        self.eliminar_boton.clicked.connect(self.eliminar) # Boton para eliminar una imagen
        self.ByN_boton.clicked.connect(self.BlancoYNegro) # Boton para convertir a blanco y negro
        self.negativo_boton.clicked.connect(self.negativo) # Boton para convertir a negativo
        self.sepia_boton.clicked.connect(self.sepia) # Boton para convertir a sepia
        self.blur_boton.clicked.connect(self.blur) # Boton para aplicar blur
        self.guardar_boton.clicked.connect(self.guardar) # Boton para guardar la imagen
        self.Rotarm90_boton.clicked.connect(self.rotar90) # Boton para rotar 90 grados
        self.circulo_boton.clicked.connect(self.circulo) # Boton para aplicar filtro de circulo
        self.eliminar_filtros_boton.clicked.connect(self.eliminarFiltros) # Boton para eliminar filtros
        self.eliminar_ruido_boton.clicked.connect(self.eliminarRuido) # Boton para eliminar ruido
        self.mejorar_boton.clicked.connect(self.mejorar) # Boton para trazar la imagen

    def eliminarRuido(self):
        global imagen_cargada_global # Variable global para saber si hay una imagen cargada
        if imagen_cargada_global == False: 
            QMessageBox.warning(self, "Error", "No se ha seleccionado ninguna imagen") # Si no hay imagen cargada, muestra un mensaje de error
        else:
            self.imagen = cv.imread("imagenEditada.jpg") # Lee la imagen
            self.imagen = cv.medianBlur(self.imagen, 5) # Aplica el filtro de ruido
            cv.imwrite("imagenEditada.jpg", self.imagen) # Guarda la imagen
            self.pixmap = QPixmap("imagenEditada.jpg") # Crea un pixmap con la imagen
            self.pixmap = self.pixmap.scaled(600, 600, Qt.AspectRatioMode.KeepAspectRatio) # Escala la imagen
            self.imagen_label.setPixmap(self.pixmap) # Muestra la imagen en el label
            Editor.mostrarHistograma(self, self.imagen) # Muestra el histograma de la imagen

    def rotar90(self):
        global imagen_cargada_global
        if imagen_cargada_global == False:
            QMessageBox.warning(self, "Error", "No se ha seleccionado ninguna imagen")
        else:
            #Rotar imagen 90 grados
            self.imagen = cv.imread("imagenEditada.jpg")
            self.imagen = cv.rotate(self.imagen, cv.ROTATE_90_CLOCKWISE) # Aplica la rotacion
            cv.imwrite("imagenEditada.jpg", self.imagen) 
            self.pixmap = QPixmap("imagenEditada.jpg") 
            self.pixmap = self.pixmap.scaled(600, 600, Qt.AspectRatioMode.KeepAspectRatio)
            self.imagen_label.setPixmap(self.pixmap)
            Editor.mostrarHistograma(self, self.imagen)


    #Deshacer filtros aplicados
    def eliminarFiltros(self):
        global imagen_cargada_global
        if imagen_cargada_global == False:
            QMessageBox.warning(self, "Error", "No se ha seleccionado ninguna imagen") 
        else:
            self.pixmap = QPixmap(self.ruta)
            self.pixmap = self.pixmap.scaled(600, 600, Qt.AspectRatioMode.KeepAspectRatio)
            self.imagen_label.setPixmap(self.pixmap)
            self.imagen = cv.imread(self.ruta) # Lee la imagen ya ingresada por el usuario (como si la volviera a cargar)
            cv.imwrite("imagenEditada.jpg", self.imagen)
            Editor.mostrarHistograma(self, self.imagen)

    def limpiarHistogramaLabel(self):
        self.histograma_label.clear() # Limpia el label del histograma
        os.remove("histograma.png") # Elimina el archivo del histograma para que no se acumulen en la carpeta del proyecto (ya que se sobreescribe cada vez que se crea uno nuevo)
    
    #Funcion para crear una mascara circular a la imagen seleccionada
    def circulo(self):
        global imagen_cargada_global
        if imagen_cargada_global == False:
            QMessageBox.warning(self, "Error", "No se ha seleccionado ninguna imagen")
        else:
            #Crear mascara circular
            self.imagen = cv.imread("imagenEditada.jpg")
            self.mask = np.zeros(self.imagen.shape[:2], dtype="uint8") # Crea una mascara de ceros
            self.cX, self.cY = (self.imagen.shape[1] // 2, self.imagen.shape[0] // 2) # Obtiene el centro de la imagen
            self.r = min(self.imagen.shape[0], self.imagen.shape[1]) // 2 # Obtiene el radio de la imagen
            cv.circle(self.mask, (self.cX, self.cY), self.r, 255, -1) # Crea un circulo en la mascara
            self.masked = cv.bitwise_and(self.imagen, self.imagen, mask=self.mask) # Aplica la mascara a la imagen
            cv.imwrite("imagenEditada.jpg", self.masked) # Guarda la imagen con la mascara aplicada 
            self.pixmap = QPixmap("imagenEditada.jpg") 
            self.pixmap = self.pixmap.scaled(600, 600, Qt.AspectRatioMode.KeepAspectRatio)
            self.imagen_label.setPixmap(self.pixmap)
            Editor.mostrarHistograma(self, self.imagen)

    def mostrarHistograma(self, imagen):
        global hay_histograma_global
        if hay_histograma_global == True:
            #borrar figura guardada
            plt.close() # Cierra la figura del histograma anterior para que no se acumulen en la memoria
        #Mostrar histograma de la imagen
        histograma = plt.hist(imagen.ravel(), 256, [0, 256]) # Crea el histograma
        #Imprimir histograma en histograma_label
        plt.savefig("histograma.png") # Guarda el histograma en un archivo
        self.pixmap = QPixmap("histograma.png") 
        self.pixmap = self.pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio)
        self.histograma_label.setPixmap(self.pixmap)
        
        hay_histograma_global = True # Cambia el valor de la variable global a True para que sepa que hay un histograma en la memoria
        

    def eliminar(self):
        global imagen_cargada_global
        if imagen_cargada_global == False:
            QMessageBox.warning(self, "Error", "Aún no se ha cargado ninguna imagen")
        else:
            #eliminar foto seleccionada
            Editor.limpiarHistogramaLabel(self) # Limpia el label del histograma
            imagen_cargada_global = False # Cambia el valor de la variable global a False para que sepa que no hay una imagen en la memoria
            self.imagen_label.clear() # Limpia el label de la imagen

    def seleccionar(self):
        global imagen_cargada_global 
        #Comprobar si hay una imagen cargada
        if imagen_cargada_global == True:
            QMessageBox.warning(self, "Error", "Ya se ha cargado una imagen. Elimínela primero")
        else:
            #funcion para seleccionar una imagen del explorador de archivos
            self.ruta = "" # Variable para guardar la ruta de la imagen seleccionada
            self.ruta = QFileDialog.getOpenFileName(self, 'Seleccionar imagen', getcwd(), 'Image files (*.jpg *.png)')[0] # Abre el explorador de archivos para seleccionar una imagen
            #escalar imagen
            self.pixmap = QPixmap(self.ruta) # Carga la imagen seleccionada
            self.pixmap = self.pixmap.scaled(600, 600, Qt.AspectRatioMode.KeepAspectRatio) # Escala la imagen para que se ajuste al label
            self.imagen_label.setPixmap(self.pixmap) # Muestra la imagen en el label
            imagen_cargada_global = True # Cambia el valor de la variable global a True para que sepa que hay una imagen en la memoria
            #Nombrar la imagen cargada como imagenEditada.jpg
            self.imagen = cv.imread(self.ruta)
            cv.imwrite("imagenEditada.jpg", self.imagen) # Guarda la imagen en un archivo con el nombre "imagenEditada.jpg" para que se pueda editar y mostrar el histograma

    
    #funcion para convertir la imagen a blanco y negro
    def BlancoYNegro(self):
        #Validación para saber si hay una imagen cargada
        if imagen_cargada_global == False:
            QMessageBox.warning(self, "Error", "No se ha seleccionado ninguna imagen")
        else:
            #Convertir la imagen a blanco y negro
            self.imagen = cv.imread("imagenEditada.jpg")
            self.imagen = cv.cvtColor(self.imagen, cv.COLOR_BGR2GRAY) # Convierte la imagen a escala de grises
            cv.imwrite("imagenEditada.jpg", self.imagen) 
            #Mostrar la imagen en el label
            self.pixmap = QPixmap("imagenEditada.jpg")
            self.pixmap = self.pixmap.scaled(600, 600, Qt.AspectRatioMode.KeepAspectRatio)
            self.imagen_label.setPixmap(self.pixmap)
            Editor.mostrarHistograma(self, self.imagen)
    
    #funcion para convertir la imagen a negativo
    def negativo(self):
        #Validación para saber si hay una imagen cargada
        if imagen_cargada_global == False:
            QMessageBox.warning(self, "Error", "No se ha seleccionado ninguna imagen")
        else:
            
            #Convertir la imagen a negativo
            self.imagen = cv.imread("imagenEditada.jpg")
            self.imagen = cv.bitwise_not(self.imagen) # Convierte la imagen a negativo
            cv.imwrite("imagenEditada.jpg", self.imagen) 
            #Mostrar la imagen en el label
            self.pixmap = QPixmap("imagenEditada.jpg")
            self.pixmap = self.pixmap.scaled(600, 600, Qt.AspectRatioMode.KeepAspectRatio)
            self.imagen_label.setPixmap(self.pixmap)
            Editor.mostrarHistograma(self, self.imagen)

    #funcion para convertir la imagen a sepia
    def sepia(self):
        #Validación para saber si hay una imagen cargada
        if imagen_cargada_global == False:
            QMessageBox.warning(self, "Error", "No se ha seleccionado ninguna imagen")
        else:
            
            #Convertir la imagen a sepia
            self.imagen = cv.imread("imagenEditada.jpg")
            self.imagen = cv.cvtColor(self.imagen, cv.COLOR_BGR2RGB) # Convierte la imagen a RGB
            self.imagen = cv.cvtColor(self.imagen, cv.COLOR_RGB2HSV) # Convierte la imagen a HSV
            self.imagen = cv.cvtColor(self.imagen, cv.COLOR_HSV2RGB) # Convierte la imagen a RGB
            cv.imwrite("imagenEditada.jpg", self.imagen)
            #Mostrar la imagen en el label
            self.pixmap = QPixmap("imagenEditada.jpg")
            self.pixmap = self.pixmap.scaled(600, 600, Qt.AspectRatioMode.KeepAspectRatio)
            self.imagen_label.setPixmap(self.pixmap)
            Editor.mostrarHistograma(self, self.imagen)

    #funcion para aplicar el filtro blur
    def blur(self):
        #Validación para saber si hay una imagen cargada
        if imagen_cargada_global == False:
            QMessageBox.warning(self, "Error", "No se ha seleccionado ninguna imagen")
        else:
            #Verificar si existe la imagen histograma.png
            
            #Aplicar el filtro blur
            self.imagen = cv.imread("imagenEditada.jpg")
            self.imagen = cv.blur(self.imagen, (20,20)) # Aplica el filtro blur
            cv.imwrite("imagenEditada.jpg", self.imagen) 
            #Mostrar la imagen en el label
            self.pixmap = QPixmap("imagenEditada.jpg")
            self.pixmap = self.pixmap.scaled(600, 600, Qt.AspectRatioMode.KeepAspectRatio)
            self.imagen_label.setPixmap(self.pixmap)
            Editor.mostrarHistograma(self, self.imagen)

    def guardar(self):
        global imagen_cargada_global
        if imagen_cargada_global == False:
            QMessageBox.warning(self, "Error", "No se ha seleccionado ninguna imagen")
        else:
            #Guardar la imagen ya editada
            self.ruta = QFileDialog.getSaveFileName(self, 'Guardar imagen', getcwd(), 'Image files (*.jpg *.png)')[0] # Guarda la imagen en la ruta especificada
            self.imagen = cv.imread("imagenEditada.jpg") # Lee la imagen editada
            cv.imwrite(self.ruta, self.imagen) # Guarda la imagen en la ruta especificada
            imagen_cargada_global = False # Cambia el valor de la variable global a False para que se pueda cargar otra imagen
            self.histograma_label.clear() # Limpia el label del histograma
            self.imagen_label.clear() # Limpia el label de la imagen
            #Borrar la imagen editada
            os.remove("imagenEditada.jpg") # Borra la imagen editada al cerrar la aplicación o al cargar otra imagen para que no se acumulen en la carpeta del proyecto

     #Funcion para añadir efecto trazado a la imagen
    def mejorar(self):
        global imagen_cargada_global
        if imagen_cargada_global == False:
            QMessageBox.warning(self, "Error", "No se ha seleccionado ninguna imagen")
        else:
            #Cargar la imagen
            self.imagen = cv.imread("imagenEditada.jpg")
            #Convertir la imagen a escala de grises
            self.imagen = cv.cvtColor(self.imagen, cv.COLOR_BGR2GRAY)
            #Aplicar el filtro blur
            self.imagen = cv.medianBlur(self.imagen, 5)
            #Detectar los bordes
            self.imagen = cv.Laplacian(self.imagen, cv.CV_8U, ksize=5)
            #Convertir la imagen a blanco 
            self.imagen = cv.cvtColor(self.imagen, cv.COLOR_GRAY2BGR)
            #Aplicar el filtro blur
            self.imagen = cv.medianBlur(self.imagen, 5)
            #Guardar la imagen
            cv.imwrite("imagenEditada.jpg", self.imagen)
            #Mostrar la imagen en el label
            self.pixmap = QPixmap("imagenEditada.jpg")
            self.pixmap = self.pixmap.scaled(600, 600, Qt.AspectRatioMode.KeepAspectRatio)
            self.imagen_label.setPixmap(self.pixmap)
            Editor.mostrarHistograma(self, self.imagen)


    def exit(self): # Función para cerrar la aplicación
        sys.exit() # Cierra la aplicación

class HowToUse(QMainWindow): # Clase para la ventana de como usar la aplicación
    def __init__(self):
        super(HowToUse, self).__init__() # Inicializa la clase
        loadUi("VentanaComoUsar.ui", self) # Carga la interfaz de la ventana
        self.regresar_boton.clicked.connect(self.gotoWelcomeScreen) # Conecta el botón de regresar con la función gotoWelcomeScreen

    
    def gotoWelcomeScreen(self): # Función para regresar a la ventana de bienvenida
        welcomeScreen = WelcomeScreen()     # Crea un objeto de la clase WelcomeScreen
        widget.addWidget(welcomeScreen)    # Agrega el objeto a la lista de widgets
        widget.setCurrentIndex(widget.currentIndex() + 1) # Cambia el widget actual a la ventana de bienvenida

# Main
app = QApplication(sys.argv) # Crea la aplicación de PyQt
welcome = WelcomeScreen() # Crea un objeto de la clase WelcomeScreen para la ventana de bienvenida
widget = QtWidgets.QStackedWidget() # Crea un objeto de la clase QStackedWidget para manejar las ventanas de la aplicación
widget.addWidget(welcome) # Agrega el objeto a la lista de widgets 
widget.show() # Muestra la ventana de bienvenida
try: # Intenta ejecutar el código
    sys.exit(app.exec()) # Cierra la aplicación al cerrar la ventana
except: # Si ocurre un error
    print("Saliendo") # Imprime el mensaje en la consola