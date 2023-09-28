from PyQt5.QtWidgets import QTabWidget, QVBoxLayout, QMainWindow, QApplication, QPlainTextEdit, QPushButton, QLabel, QTableWidget, QFileDialog, QComboBox, QTableWidgetItem
from PyQt5.QtChart import QChartView, QChart, QPieSeries, QPieSlice
from PyQt5.QtGui import QBrush, QColor, QIcon
from PyQt5 import uic
from classifier import classify, classify_with_model, get_food_from_text
from marketScraper import get_prices_from_markets
import numpy as np
import joblib
import sys
import os
from PyQt5.QtWidgets import QApplication
import csv


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("interfaces/MainWindow.ui", self)
        self.setWindowIcon(QIcon('assets/icon.png'))
        self.setWindowTitle("Shop2Cook")
        self.trained_models = {}
        # Widgets
        # Entramiento
        self.tab_widget = self.findChild(QTabWidget, "tabWidget")
        self.tab_widget.setTabText(0, "Entrenamiento")
        self.tab_widget.setTabText(1, "Clasificacion")
        self.tab_widget.setTabText(2, "Comparador")
        self.textfolders_button = self.findChild(QPushButton, "pushButton")
        self.textfolders_qte = self.findChild(QPlainTextEdit, "plainTextEdit")
        self.save_model_qte = self.findChild(QPlainTextEdit, "plainTextEdit_5")
        self.cb = self.findChild(QComboBox, "comboBox")
        self.cb.addItem("Decision Tree")
        self.cb.addItem("Random Forest")
        self.cb.addItem("Bayes")
        self.cb.addItem("Support Vector Machine")
        self.cb.addItem("K-Nearest-Neighbor")
        self.cb.activated[str].connect(self.on_changed)
        
        self.lblejem_carne = self.findChild(QLabel, "label_14")
        self.lblejem_cereales = self.findChild(QLabel, "label_15")
        self.lblejem_leche = self.findChild(QLabel, "label_16")
        self.lblejem_legumbres = self.findChild(QLabel, "label_17")
        self.lblejemTotal = self.findChild(QLabel, "label_18")

        self.textfolders_button.clicked.connect((lambda: self.select_path(self.textfolders_qte)))

        self.run_training_button = self.findChild(QPushButton, "pushButton_5")
        self.run_training_button.clicked.connect((lambda: self.run_model(str(self.cb.currentText()))))
        
        # Clasificacion
        self.training_table = self.findChild(QTableWidget, "tableWidget")
        self.save_model_button = self.findChild(QPushButton, "pushButton_6")
        self.save_model_button.clicked.connect((lambda: self.save_model(self.trained_models[str(self.cb.currentText())])))
        self.ejem_vertical_layout = self.findChild(QVBoxLayout, "verticalLayout")
        self.results_vertical_layout = self.findChild(QVBoxLayout, "verticalLayout_2")
        self.class_text_folders_button = self.findChild(QPushButton, "cpushButton")
        self.class_text_folders_qte = self.findChild(QPlainTextEdit, "cplainTextEdit")
        self.class_model_button = self.findChild(QPushButton, "cpushButton_2")
        self.class_model_qte = self.findChild(QPlainTextEdit, "cplainTextEdit_2")
        self.class_text_folders_button.clicked.connect((lambda: self.select_class_text_path(self.class_text_folders_qte)))
        self.class_model_button.clicked.connect((lambda: self.select_file(self.class_model_qte)))
        self.class_run_button = self.findChild(QPushButton, "cpushButton_3")
        self.class_run_button.clicked.connect((lambda: self.load_model(self.class_model_qte.toPlainText())))
        self.classification_table = self.findChild(QTableWidget, "ctableWidget")
        self.class_save_results_qte = self.findChild(QPlainTextEdit, "cplainTextEdit_3")
        self.class_save_results_button = self.findChild(QPushButton, "cpushButton_4")
        self.class_save_results_button.clicked.connect(self.save_results_csv)
        self.clicked_text_qte = self.findChild(QPlainTextEdit, "cplainTextEdit_4")
                
        # Comparador
        self.prices_table = self.findChild(QTableWidget, "stableWidget")
        self.comp_text_qte = self.findChild(QPlainTextEdit, "splainTextEdit")
        self.comp_text_button = self.findChild(QPushButton, "spushButton")
        self.comp_text_button.clicked.connect((lambda: self.select_file(self.comp_text_qte)))
        self.compare_run_button = self.findChild(QPushButton, "spushButton_2")
        self.compare_run_button.clicked.connect((lambda: self.compare_prices()))
        self.min_price_label = self.findChild(QLabel, "label_20")
        self.best_market_label = self.findChild(QLabel, "label_22")
        self.show()
    
    def save_results_csv(self):
        file = QFileDialog.getSaveFileName(self, "Save File", "")[0]
        if file:
            print(file)
            self.class_save_results_qte.setPlainText(file)
            with open(file + ".csv", "w", encoding='UTF8', newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["nombre_archivo", "clasificacion"])
                for i in range(self.classification_table.rowCount()):
                    row = []
                    row.append(self.classification_table.item(i, 0).text())
                    row.append(self.classification_table.item(i, 1).text())
                    writer.writerow(row)
    
    # Obteniene la lista de alimentos a partir de la localizacion del texto introducido
    # y compara los precios de los productos en varios supermecardos
    def compare_prices(self):
        if self.comp_text_qte.toPlainText() != "":
            food_list = get_food_from_text(self.comp_text_qte.toPlainText())
            print(food_list)
            prices = get_prices_from_markets(food_list)
            for i in range(len(prices["carrefour"])):
                self.prices_table.insertRow(i)
                #self.prices_table.setItem(i, 0, QTableWidgetItem(str(prices["mercadona"][i])))
                self.prices_table.setItem(i, 0, QTableWidgetItem(str(prices["carrefour"][i])))
                self.prices_table.setItem(i, 1, QTableWidgetItem(str(prices["dia"][i])))
                
                #self.prices_table.item(i, col).setBackground(QColor(118, 191, 105))
                #self.prices_table.item(i, j).setBackground(QColor(255, 117, 107))
            #markets = ["mercadona", "carrefour", "dia"]
            markets = ["carrefour", "dia"]
            sum_all_low = 0
            for i in range(len(prices["carrefour"])):
                low = 99999
                col = 0
                for j in range(len(prices)):
                    if prices[markets[j]][i] != 0 and prices[markets[j]][i] < low:
                        low = prices[markets[j]][i]
                        col = j
                    if prices[markets[j]][i] == 0:
                        self.prices_table.item(i, j).setBackground(QColor(255, 160, 77)) # rojo
                    else:
                        self.prices_table.item(i, j).setBackground(QColor(255, 117, 107)) # naranja
                sum_all_low += prices[markets[col]][i]
                self.prices_table.item(i, col).setBackground(QColor(118, 191, 105)) #verde
            self.min_price_label.setText(str(sum_all_low))
            self.prices_table.insertRow(len(prices["carrefour"]))
            #total_prices = {"Mercadona": 0, "Carrefour": 0, "Dia": 0}
            total_prices = {"Carrefour": 0, "Dia": 0}
            for i in range(len(prices["carrefour"])):
                if prices[markets[0]][i] != 0:
                    #total_prices["Mercadona"] += prices[markets[0]][i]
                    total_prices["Carrefour"] += prices[markets[0]][i]
                    total_prices["Dia"] += prices[markets[1]][i]
            #self.prices_table.setItem(len(prices["mercadona"]), 0, QTableWidgetItem(str(total_prices["Mercadona"])))
            self.prices_table.setItem(len(prices["carrefour"]), 0, QTableWidgetItem(str(total_prices["Carrefour"])))
            self.prices_table.setItem(len(prices["carrefour"]), 1, QTableWidgetItem(str(total_prices["Dia"])))
            self.best_market_label.setText(str(min(total_prices, key=total_prices.get)))
            food_list.append("Total")
            self.prices_table.setVerticalHeaderLabels(food_list)


    # Crea una pie chart con la cantidad de textos de cada categoria
    def setup_pie_chart_labels(self):
        # Limpiamos el layout
        for i in reversed(range(self.ejem_vertical_layout.count())): 
            self.ejem_vertical_layout.itemAt(i).widget().setParent(None)
        series = QPieSeries()
        series.append("Carnes", int(self.lblejem_carne.text()))
        series.append("Cereal", int(self.lblejem_cereales.text()))
        series.append("Leche", int(self.lblejem_leche.text()))
        series.append("Legumbres", int(self.lblejem_legumbres.text()))
 
        slices = QPieSlice()
        slices = series.slices()
        for sl in slices:
            sl.setExploded(True)
            sl.setLabelVisible(True)
 
        chart = QChart()
        chart.legend().hide()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setBackgroundBrush(QBrush(QColor("transparent")))

        chartview = QChartView(chart)
 
        self.ejem_vertical_layout.addWidget(chartview)
        
    # Crea una pie chart con los resultados positivos y negativos tras entrenar el modelo
    def setup_pie_chart_results(self, matrix):
        for i in reversed(range(self.results_vertical_layout.count())): 
            self.results_vertical_layout.itemAt(i).widget().setParent(None)
        rows = len(matrix)
        positives = 0
        negatives = 0
        for i in range(rows):
            for j in range(rows):
                if i == j:
                    positives += matrix[i][j]
                else:
                    negatives += matrix[i][j]
        series = QPieSeries()
        series.append("Positivos", positives)
        series.append("Negativos", negatives)
 
        slices = QPieSlice()
        slices = series.slices()
        for sl in slices:
            sl.setExploded(True)
            sl.setLabelVisible(True)
 
        chart = QChart()
        chart.legend().hide()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setBackgroundBrush(QBrush(QColor("transparent")))

        chartview = QChartView(chart)
 
        self.results_vertical_layout.addWidget(chartview)
    
    
    def select_class_text_path(self, qte):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if file:
            qte.setPlainText(file)
    # Abre el explorador de archivos para seleccionar una ruta y aplica
    # la ruta a la label pasada por referencia
    def select_path(self, qte):
        self.lblejem_carne.setText("0")
        self.lblejem_cereales.setText("0")
        self.lblejem_leche.setText("0")
        self.lblejem_legumbres.setText("0")
        self.lblejemTotal.setText("0")
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if file:
            qte.setPlainText(file)
            folders = os.listdir(file)
            count = 1
            for folder in folders:
                _, _, files = next(os.walk(file + "/" + folder))
                file_count = len(files)
                if count == 1:
                    self.lblejem_carne.setText(str(file_count))
                elif count == 2:
                    self.lblejem_cereales.setText(str(file_count))
                elif count == 3:
                    self.lblejem_leche.setText(str(file_count))
                else:
                    self.lblejem_legumbres.setText(str(file_count))
                self.lblejemTotal.setText(str(int(self.lblejemTotal.text()) + file_count))
                count += 1
        self.setup_pie_chart_labels()
        
    # Imprime por consola el nuevo valor de la combobox
    def on_changed(self, text):
        print(text)
        
    # Ejecuta el entrenamiento a los textos seleccionados, guarda el modelo en una
    # variable y rellena la tabla creando una matriz de confusion de los resultados
    def run_model(self, algorithm):
        if self.textfolders_qte.toPlainText() != "":
            model = classify(self.textfolders_qte.toPlainText(), algorithm)
            matrix = model["Matrix"]
            self.trained_models[algorithm] = model[algorithm]
            for i in range(np.size(matrix, 0)):
                for j in range(np.size(matrix, 1)):
                    self.training_table.item(i, j).setText(str(matrix[i][j]))
                    if i == j:
                        self.training_table.item(i, j).setBackground(QColor(118, 191, 105))
                    else:
                        self.training_table.item(i, j).setBackground(QColor(255, 117, 107))

                        
            self.setup_pie_chart_results(matrix)
            
    # Abre el explorador de archivos para guardar tanto el modelo clasificador con el
    # vectorizador tdidf (ambos necesitados para volver a ejecutar el modelo posteriormente)
    def save_model(self, model):
        file = QFileDialog.getSaveFileName(self, "Save File", "modelos/")[0]
        if file:
            print(file)
            self.save_model_qte.setPlainText(file)
            joblib.dump(model["Tfidf"], file+"_tfidf.joblib")
            joblib.dump(model["Classifier"], file+"_classifier.joblib")

    # Carga tanto el modelo clasificador como el vectorizador tfidf a partir
    # de la ruta pasada por referencia y ejecuta el clasificador
    def load_model(self, file):
        print(file)
        if file != "" and self.class_text_folders_qte.toPlainText() != "":
            if "classifier" in file:
                loaded_classifier = joblib.load(file)
                tfidf_file = file.replace("classifier", "tfidf")
                loaded_tfidf = joblib.load(tfidf_file)
            else:
                loaded_tfidf = joblib.load(file)
                classifier_file = file.replace("tfidf", "classifier")
                loaded_classifier = joblib.load(classifier_file)
            
            print(self.class_text_folders_qte.toPlainText())
            y_pred = classify_with_model(self.class_text_folders_qte.toPlainText(), loaded_tfidf, loaded_classifier)
            self.show_results(y_pred)
            
    # A partir del array de predicciones pasado por referencia, lo transforma
    # a un formato legible y lo muestra en una tabla
    def show_results(self, y_pred):
        while self.classification_table.rowCount() > 0:
            self.classification_table.removeRow(0);
        labeled_y_pred = []
        for p in y_pred:
            if (p == 0):
                labeled_y_pred.append("Carnes, pescados y verduras")
            elif (p == 1):
                labeled_y_pred.append("Cereales y derivados")
            elif (p == 2):
                labeled_y_pred.append("Leche, huevo y derivados")
            else:
                labeled_y_pred.append("Legumbres")
        print(self.class_text_folders_qte.toPlainText())
        text_names = os.listdir(self.class_text_folders_qte.toPlainText() + "/" + os.listdir(self.class_text_folders_qte.toPlainText())[0])
        for i in range(len(y_pred)):
            self.classification_table.insertRow(i)
            self.classification_table.setItem(i, 0, QTableWidgetItem(str(text_names[i])))
            self.classification_table.setItem(i, 1, QTableWidgetItem(str(labeled_y_pred[i])))
            text_view_button = QPushButton("Ver")
            text_view_button.clicked.connect(lambda *args, row=i: self.view_text_clicked(row))
            self.classification_table.setCellWidget(i, 2, text_view_button)
    
    # Imprime el contenido de la receta seleccionada
    def view_text_clicked(self, row):
        text = self.classification_table.item(row, 0).text()
        path_to_text = self.class_text_folders_qte.toPlainText() + "/" + os.listdir(self.class_text_folders_qte.toPlainText())[0]
        text_to_open = path_to_text + "/" + text
        print(text_to_open)
        with open(text_to_open, "r", encoding="latin1") as f:
            self.clicked_text_qte.setPlainText(f.read())
            
    # Abre el explorador de archivos y permite seleccionar un archivo y
    # aplica la ruta de este a la label pasada por referencia
    def select_file(self, qte):
        file = QFileDialog.getOpenFileName(self, "Open file")[0]
        if file:
            qte.setPlainText(file)
               
if (__name__ == '__main__'):
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()