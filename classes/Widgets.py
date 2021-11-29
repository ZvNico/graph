from typing import Tuple, Callable

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QWidget, QComboBox, QHBoxLayout, QVBoxLayout, QPushButton, QLabel

from .Enum import RankComputeMode
from .Graph import Graph


class GraphList(QWidget):
    def __init__(self, refresh: Callable):
        super().__init__()
        self.refresh = refresh
        self.graphs = {}
        layout = QHBoxLayout()
        self.dropdown = QComboBox()
        self.dropdown.activated[str].connect(self.on_change)
        layout.addWidget(self.dropdown)
        self.setLayout(layout)

    def add_graph(self, filename: str):
        self.dropdown.addItem(filename.split("/")[-1])
        self.graphs[filename.split("/")[-1]] = Graph(filename)
        self.dropdown.setCurrentText(filename.split("/")[-1])

    def on_change(self, text):
        self.refresh()

    def current(self) -> Graph:
        return self.graphs[self.dropdown.currentText()]


class NavWidget(QWidget):
    def __init__(self, pages: Tuple[str], show_widget: Callable):
        super().__init__()
        self.show_widget = show_widget
        self.layout = QHBoxLayout()
        self.current = 0
        self.pages = pages[:]
        self.buttons = []
        for i in range(len(self.pages)):
            self.buttons.append(QPushButton(self.pages[i], self))
            self.buttons[i].clicked.connect(lambda checked, x=i: self.on_click(x))
            self.layout.addWidget(self.buttons[i])
        self.buttons[0].setEnabled(False)
        self.setLayout(self.layout)

    def on_click(self, i):
        self.buttons[self.current].setEnabled(True)
        self.current = i
        self.buttons[self.current].setEnabled(False)
        self.show_widget(self.pages[i])


class RawGraphWidget(QWidget):
    def __init__(self, current: Callable):
        super().__init__()
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.current = current
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def refresh(self):
        graph = self.current()
        graph.write_txt_file("temp/temp.txt")
        with open("temp/temp.txt", "r") as graph_txt:
            self.label.setText(graph_txt.read())


class MatrixWidget(QWidget):
    def __init__(self, current: Callable):
        super().__init__()
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Courier", 11))
        self.current = current
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def refresh(self):
        graph = self.current()
        self.label.setText(graph.str_matrix(graph.adjacency_matrix()))


class GraphVizWidget(QWidget):
    def __init__(self, current: Callable):
        super().__init__()
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.current = current
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def refresh(self):
        self.current().render("temp/", "temp")
        pixmap = QPixmap("temp/temp.png")
        self.label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())


class OperationWidget(QWidget):
    def __init__(self, current: Callable, parent):
        super().__init__()
        self.button = QPushButton("►")
        self.button.clicked.connect(lambda checked: self.run())
        self.operations = {}
        self.current = current
        self.parent = parent
        self.dropdown = QComboBox()
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.dropdown, 1)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def run(self):
        operation = self.dropdown.currentText()
        if operation in self.operations.keys():
            print(operation)
            args = []
            if operation == "calculer le rang":
                args.append(RankComputeMode.starting_node_elimination)
            res = self.operations[operation](*args)
            if operation == "calculer le rang":
                if res == - 1:
                    self.parent.output_widget.print("Circuit détecter -> interruption du calcul")
                elif res == 0:
                    self.parent.output_widget.print("Pas de circuit détecté -> le calcul a été effectué")
            elif operation == "verifier point d'entrée unique" or operation == "verifier point de sortie unique":
                if res:
                    self.parent.output_widget.print("Vrai")
                else:
                    self.parent.output_widget.print("Faux")
            self.parent.refresh()

    def refresh(self):
        self.operations["calculer le rang"] = self.current().rank_compute
        self.operations["verifier point de sortie unique"] = self.current().unique_entry_point
        self.operations["verifier point d'entrée unique"] = self.current().unique_exit_point
        self.dropdown.clear()
        for operation in self.operations.keys():
            self.dropdown.addItem(operation)


class OutputWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.label1 = QLabel("Output: ")
        self.label2 = QLabel()
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.label2, 1)
        self.setLayout(self.layout)

    def print(self, text: str):
        self.label2.setText(text)
