import logging
import sys
import csv
import json
import os
import random
import time
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QCheckBox, QSpinBox, QPushButton, 
    QTextBrowser, QMessageBox, QFileDialog, QLineEdit, QInputDialog
)
from PyQt5.QtCore import QThread, pyqtSignal
import urllib.parse
from duckduckgo_search import DDGS
from googlesearch import search

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler('dork_recon.log', encoding='utf-8')]
)

class DorkSearchThread(QThread):
    search_complete = pyqtSignal(list)
    search_progress = pyqtSignal(str)

    def __init__(self, query, max_results=50, search_engine='duckduckgo', api_key=None):
        super().__init__()
        self.query = query
        self.max_results = max_results
        self.search_engine = search_engine
        self.api_key = api_key

    def perform_duckduckgo_search(self):
        results = []
        try:
            with DDGS() as ddgs:
                ddg_results = list(ddgs.text(self.query, max_results=self.max_results))
                for result in ddg_results:
                    results.append({
                        'title': result.get('title', 'No Title'),
                        'url': result.get('href', '')
                    })
            self.search_progress.emit(f"✅ Found {len(results)} results")
        except Exception as e:
            self.search_progress.emit(f"❌ DuckDuckGo Search Error: {str(e)}")
        return results

    def perform_serpapi_search(self):
        results = []
        if not self.api_key:
            self.search_progress.emit("SerpAPI requires an API key")
            return results

        try:
            # Use the search function from googlesearch
            for result in search(self.query, num_results=self.max_results):
                results.append({
                    'title': result.title,
                    'url': result.url
                })
            self.search_progress.emit(f"Found {len(results)} results")
        except Exception as e:
            self.search_progress.emit(f"SerpAPI Search Error: {str(e)}")
        return results

    def run(self):
        if self.search_engine == 'serpapi':
            results = self.perform_serpapi_search()
        else:
            results = self.perform_duckduckgo_search()
        self.search_complete.emit(results)

class DorkReconApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('DorkRecon')
        self.setGeometry(100, 100, 800, 600)
        self.results = []  # Store search results
        self.initUI()
        self.load_stylesheet()

    def load_stylesheet(self):
        with open('style.qss', 'r') as f:
            self.setStyleSheet(f.read())

    def initUI(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Dork input with load button
        dork_input_layout = QHBoxLayout()
        self.dork_input = QLineEdit()
        self.dork_input.setPlaceholderText('Enter Google Dork Query')
        dork_input_layout.addWidget(self.dork_input)
        
        load_dorks_button = QPushButton('Load Dorks')
        load_dorks_button.clicked.connect(self.load_dorks_from_file)
        dork_input_layout.addWidget(load_dorks_button)
        
        main_layout.addLayout(dork_input_layout)
        
        # Search engine selection
        search_engine_layout = QHBoxLayout()
        self.duckduckgo_radio = QCheckBox('DuckDuckGo')
        self.serpapi_radio = QCheckBox('SerpAPI')
        search_engine_layout.addWidget(self.duckduckgo_radio)
        search_engine_layout.addWidget(self.serpapi_radio)
        self.duckduckgo_radio.setChecked(True)
        main_layout.addLayout(search_engine_layout)
        
        # SerpAPI Key input
        serpapi_key_layout = QHBoxLayout()
        self.serpapi_key_input = QLineEdit()
        self.serpapi_key_input.setPlaceholderText('Enter SerpAPI Key (Optional)')
        serpapi_key_layout.addWidget(self.serpapi_key_input)
        main_layout.addLayout(serpapi_key_layout)
        
        self.results_spin = QSpinBox()
        self.results_spin.setRange(10, 200)
        self.results_spin.setValue(50)
        main_layout.addWidget(self.results_spin)
        
        search_button = QPushButton('Search')
        search_button.clicked.connect(self.perform_dork_search)
        main_layout.addWidget(search_button)
        
        self.status_text = QTextBrowser()
        main_layout.addWidget(self.status_text)
        
        self.results_text = QTextBrowser()
        main_layout.addWidget(self.results_text)
        
        export_csv_button = QPushButton('Export CSV')
        export_csv_button.clicked.connect(self.export_to_csv)
        main_layout.addWidget(export_csv_button)
        
        export_json_button = QPushButton('Export JSON')
        export_json_button.clicked.connect(self.export_to_json)
        main_layout.addWidget(export_json_button)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def load_dorks_from_file(self):
        dorks_path = os.path.join(os.path.dirname(__file__), 'dorks.txt')
        try:
            with open(dorks_path, 'r', encoding='utf-8') as f:
                dorks = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            if not dorks:
                QMessageBox.warning(self, 'No Dorks', 'The dorks.txt file is empty!')
                return
            
            dork, ok = QInputDialog.getItem(self, 'Select Dork', 'Choose a dork:', dorks, 0, False)
            if ok and dork:
                self.dork_input.setText(dork)
        
        except FileNotFoundError:
            QMessageBox.critical(self, 'File Not Found', 'dorks.txt was not found! Create the file first.')

    def perform_dork_search(self):
        query = self.dork_input.text().strip()
        max_results = self.results_spin.value()
        
        if not query:
            QMessageBox.warning(self, 'Invalid Query', 'Please enter a valid search query.')
            return
        
        # Clear previous results
        self.results = []
        self.results_text.clear()
        self.status_text.clear()
        
        # Determine search engine
        if self.serpapi_radio.isChecked():
            api_key = self.serpapi_key_input.text().strip()
            if not api_key:
                QMessageBox.warning(self, 'API Key Required', 'Please enter a SerpAPI key.')
                return
            search_engine = 'serpapi'
        else:
            api_key = None
            search_engine = 'duckduckgo'
        
        self.search_thread = DorkSearchThread(query, max_results, search_engine, api_key)
        self.search_thread.search_complete.connect(self.display_search_results)
        self.search_thread.search_progress.connect(self.update_status)
        self.search_thread.start()

    def update_status(self, message):
        self.status_text.append(message)

    def display_search_results(self, results):
        self.results = results  # Store the results
        for result in results:
            self.results_text.append(f"Title: {result['title']}\nURL: {result['url']}\n---")

    def export_to_csv(self):
        if not self.results:
            QMessageBox.warning(self, 'No Results', 'No search results to export.')
            return
        
        filename, _ = QFileDialog.getSaveFileName(self, 'Export Results', '', 'CSV Files (*.csv)')
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=['title', 'url'])
                    writer.writeheader()
                    writer.writerows(self.results)
                QMessageBox.information(self, 'Export Successful', f'Results exported to {filename}')
            except Exception as e:
                QMessageBox.critical(self, 'Export Error', f'Failed to export results: {str(e)}')

    def export_to_json(self):
        if not self.results:
            QMessageBox.warning(self, 'No Results', 'No search results to export.')
            return
        
        filename, _ = QFileDialog.getSaveFileName(self, 'Export Results', '', 'JSON Files (*.json)')
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as jsonfile:
                    json.dump(self.results, jsonfile, indent=4)
                QMessageBox.information(self, 'Export Successful', f'Results exported to {filename}')
            except Exception as e:
                QMessageBox.critical(self, 'Export Error', f'Failed to export results: {str(e)}')

def main():
    app = QApplication(sys.argv)
    dork_recon = DorkReconApp()
    dork_recon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
