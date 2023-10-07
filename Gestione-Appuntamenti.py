# Name: Gestione Appuntamenti
# Author: Bocaletto Luca Aka Elektronoide
# Importazioni dei moduli necessari
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QDialog, QMessageBox, QCalendarWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor

import sqlite3

# Definizione di una finestra di dialogo "About"
class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("About")  # Imposta il titolo della finestra
        self.setGeometry(100, 100, 400, 200)  # Imposta le dimensioni della finestra

        layout = QVBoxLayout()  # Crea un layout verticale per la finestra

        about_label = QLabel("Gestore Appuntamenti v0.5 - By Bocaletto Luca")  # Etichetta con le informazioni sull'app
        layout.addWidget(about_label)  # Aggiungi l'etichetta al layout

        ok_button = QPushButton("OK")  # Crea un pulsante "OK"
        ok_button.clicked.connect(self.accept)  # Collega la pressione del pulsante alla chiusura della finestra

        layout.addWidget(ok_button)  # Aggiungi il pulsante al layout

        self.setLayout(layout)  # Imposta il layout per la finestra

# Definizione della classe principale dell'app
class AppuntamentiApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestione Appuntamenti")  # Imposta il titolo della finestra principale
        self.setGeometry(100, 100, 800, 600)  # Imposta le dimensioni della finestra

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Aggiungi un titolo colorato
        title_label = QLabel("Gestione Appuntamenti")  # Titolo dell'app
        title_label.setFont(QFont("Arial", 24))  # Imposta il carattere e la dimensione del titolo
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centra il titolo
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 102, 204))  # Imposta il colore del testo
        title_label.setPalette(palette)
        layout.addWidget(title_label)

        # Creazione di elementi del modulo di input
        self.nome_label = QLabel("Nome:")
        self.nome_entry = QLineEdit()
        self.data_label = QLabel("Data:")
        self.data_calendar = QCalendarWidget()
        self.descrizione_label = QLabel("Descrizione:")
        self.descrizione_entry = QLineEdit()

        form_layout = QVBoxLayout()
        form_layout.addWidget(self.nome_label)
        form_layout.addWidget(self.nome_entry)
        form_layout.addWidget(self.data_label)
        form_layout.addWidget(self.data_calendar)
        form_layout.addWidget(self.descrizione_label)
        form_layout.addWidget(self.descrizione_entry)

        button_layout = QHBoxLayout()
        self.inserisci_button = QPushButton("Inserisci")
        self.elimina_button = QPushButton("Elimina")
        button_layout.addWidget(self.inserisci_button)
        button_layout.addWidget(self.elimina_button)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        # Collega i pulsanti alle rispettive funzioni
        self.inserisci_button.clicked.connect(self.inserisci_appuntamento)
        self.elimina_button.clicked.connect(self.elimina_appuntamento)

        # Creazione di una tabella per visualizzare gli appuntamenti
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "Data", "Descrizione"])
        layout.addWidget(self.table)

        # Connessione al database SQLite
        self.conn = sqlite3.connect("appuntamenti.db")
        self.cursor = self.conn.cursor()

        # Creazione della tabella se non esiste
        self.crea_tabella_appuntamenti()

        # Elenco degli appuntamenti nella tabella
        self.elenca_appuntamenti()

        # Aggiungi il pulsante "About" alla barra dei menu
        about_action = self.menuBar().addAction("About")
        about_action.triggered.connect(self.mostra_about)

    def crea_tabella_appuntamenti(self):
        # Crea la tabella nel database se non esiste
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS appuntamenti (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                data DATE NOT NULL,
                descrizione TEXT
            )
        ''')
        self.conn.commit()

    def inserisci_appuntamento(self):
        # Ottieni i dati dall'input e inseriscili nel database
        nome = self.nome_entry.text()
        data = self.data_calendar.selectedDate().toString("yyyy-MM-dd")
        descrizione = self.descrizione_entry.text()
        if nome and data:
            self.cursor.execute("INSERT INTO appuntamenti (nome, data, descrizione) VALUES (?, ?, ?)",
                                (nome, data, descrizione))
            self.conn.commit()
            self.elenca_appuntamenti()  # Aggiorna la tabella degli appuntamenti
            self.nome_entry.clear()  # Cancella l'input del nome
            self.descrizione_entry.clear()  # Cancella l'input della descrizione
        else:
            QMessageBox.warning(self, "Attenzione", "Nome e Data sono campi obbligatori.")

    def elimina_appuntamento(self):
        # Elimina un appuntamento dalla tabella
        riga_selezionata = self.table.currentRow()
        if riga_selezionata >= 0:
            id_selezionato = self.table.item(riga_selezionata, 0).text()
            self.cursor.execute("DELETE FROM appuntamenti WHERE id=?", (id_selezionato,))
            self.conn.commit()
            self.elenca_appuntamenti()  # Aggiorna la tabella degli appuntamenti

    def elenca_appuntamenti(self):
        # Ottieni gli appuntamenti dal database e visualizzali nella tabella
        self.cursor.execute("SELECT * FROM appuntamenti")
        appuntamenti = self.cursor.fetchall()
        self.table.setRowCount(0)  # Cancella tutte le righe attuali dalla tabella
        for i, appuntamento in enumerate(appuntamenti):
            self.table.insertRow(i)  # Inserisci una nuova riga nella tabella
            for j, col in enumerate(appuntamento):
                item = QTableWidgetItem(str(col))
                item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)  # Impedisce la modifica diretta dei dati
                self.table.setItem(i, j, item)

    def mostra_about(self):
        about_dialog = AboutDialog()
        about_dialog.exec()

def main():
    app = QApplication(sys.argv)
    window = AppuntamentiApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
