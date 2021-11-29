from PyQt5.QtWidgets import QMainWindow, QMenu, QAction, QFileDialog, QStackedWidget, QMessageBox

from .Widgets import *


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Théorie des graphes")
        self.actions = {}
        self.menus = {}
        self._create_actions()
        self._create_menus()
        self.graph_list = GraphList(self.refresh)
        self.graph_list.add_graph("graph/graph.txt")
        self.stack = QStackedWidget()
        self.refresh_dependant_widget = []
        self.stack_item = {"Raw Graph": RawGraphWidget(self.graph_list.current),
                           "Matrix": MatrixWidget(self.graph_list.current),
                           "GraphViz": GraphVizWidget(self.graph_list.current)}
        for item in self.stack_item.values():
            self.stack.addWidget(item)
            self.refresh_dependant_widget.append(item)
        self.stack.setCurrentIndex(0)
        self.nav_widget = NavWidget(tuple(self.stack_item.keys()), self.show_stack_widget)
        self.operations_widget = OperationWidget(self.graph_list.current, self)
        self.output_widget = OutputWidget()
        self.refresh_dependant_widget.append(self.operations_widget)
        self.layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.layout.addWidget(self.graph_list)
        self.layout.addWidget(self.nav_widget)
        self.layout.addWidget(self.stack)
        self.layout.addWidget(self.operations_widget)
        self.layout.addWidget(self.output_widget)
        self.setCentralWidget(self.central_widget)
        self.refresh()
        self.showMaximized()

    def _create_menus(self):
        self.menubar = self.menuBar()
        self.menus["file"] = QMenu("&File", self)
        self.menubar.addMenu(self.menus["file"])
        self.menus["file"].addAction(self.actions["file"]["open"])
        self.menus["file"].addAction(self.actions["file"]["save"])
        self.menus["file"].addAction(self.actions["file"]["save_as"])
        self.menus["about"] = QMenu("&About", self)
        self.menubar.addMenu(self.menus["about"])
        self.menus["about"].addAction(self.actions["about"]["help"])

    def _create_actions(self):
        self.actions["about"] = {}
        self.actions["about"]["help"] = QAction("&Help", self)
        self.actions["about"]["help"].triggered.connect(self.help)
        self.actions["file"] = {}
        self.actions["file"]["open"] = QAction("&Open", self)
        self.actions["file"]["save"] = QAction("&Save", self)
        self.actions["file"]["save_as"] = QAction("&Save as", self)
        self.actions["file"]["open"].triggered.connect(self.open)
        self.actions["file"]["save"].triggered.connect(self.save)
        self.actions["file"]["save_as"].triggered.connect(self.save_as)

    def open(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Open a graph txt file", "graph/", "Txt Files (*.txt)",
                                                  options=options)
        if filename:
            self.graph_list.add_graph(filename)
            self.output_widget.print("")
            self.refresh()

    def save(self, filename=None):
        i = self.stack.currentIndex()
        graph = self.graph_list.current()
        if not filename:
            filename = graph.filename
        path = "/".join(filename.split("/")[:-1]) + "/"
        file = filename.split("/")[-1].split(".")[0]
        if i == 0:
            graph.write_txt_file(filename)
        elif i == 1:
            with open(f"{path}matrix_{file}.txt", "w") as f:
                f.write(graph.str_matrix(graph.adjacency_matrix()))
        elif i == 2:
            graph.render("renders/", file)

    def save_as(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        i = self.stack.currentIndex()
        if i == 0 or i == 1:
            starting_dir = "graph/"
        elif i == 2:
            starting_dir = "renders/"
        else:
            starting_dir = ""
        filename, _ = QFileDialog.getSaveFileName(self, "Save as", starting_dir, "All Files (*.*)",
                                                  options=options)
        if filename:
            self.save(filename)

    def help(self):
        msg = QMessageBox()
        msg.setText("Open or save a graph: File menu (top left corner)\n\n"
                    "Run an operation: Choose your operation in the bottom dropdown menu and click on '►' to run it\n\n"
                    "Navigate through your opened graph: choose a graph in the top dropdown menu\n\n"
                    "Navigate through differents views: click on one of the three button on the nav below the top "
                    "dropdown menu\n\n")
        msg.exec()

    def show_stack_widget(self, name: str):
        i = list(self.stack_item.keys()).index(name)
        self.stack.setCurrentIndex(i)
        self.stack_item[name].refresh()

    def refresh(self):
        for item in self.refresh_dependant_widget:
            item.refresh()
