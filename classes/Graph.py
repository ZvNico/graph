import graphviz
from .Enum import *
from .Arc import Arc
from .Node import Node
from typing import List, Tuple
from prettytable import PrettyTable


class Graph:
    def __init__(self, filename: str = "graph/graph1.txt"):
        self.nodes = []
        self.arcs = {}
        self.filename = filename
        if filename.endswith('.txt'):
            self.parsing_txt_file(filename=filename)
        # self.render()
        print(self.str_matrix(self.adjacency_matrix()))

    def __str__(self):
        chaine = "nodes:"
        for node in self.nodes:
            chaine += " " + node
        chaine += "\n"
        for node, arcs in self.arcs.items():
            for arc in arcs:
                chaine += f"{node} ==({arc[0]})==> {arc[1]}\n"
        return chaine

    def str_matrix(self, matrix):
        column_names = [node for node in self.nodes]
        row_names = [node for node in self.nodes]
        pt = PrettyTable()
        pt.field_names = ["Node"] + column_names
        for i in range(len(self.nodes)):
            pt.add_row(
                [row_names[i]] + [matrix[i][j] if matrix[i][j] is not None else "X" for j in range(len(self.nodes))])
        return pt

    def adjacency_matrix(self) -> List[list]:
        matrix = []
        for i, node1 in enumerate(self.nodes):
            matrix.append([])
            for j, node2 in enumerate(self.nodes):
                matrix[i].append(self.dist(node1, node2) if node2 in self.children(node1) else None)
        return matrix

    def add_arc(self, x, y, value) -> None:
        if x not in self.arcs.keys():
            raise f"{x} not in arcs"
        self.arcs[x].append((y, value))

    def rank_compute(self, mode: RankComputeMode) -> list:
        pass

    def parents(self, node: str) -> List[str]:
        parents = []
        for key, arc in self.arcs.items():
            if node in value:
                parents.append(key)
        return parents

    def children(self, node: str) -> Tuple[str]:
        return tuple(arc.end for arc in self.arcs[node])

    def dist(self, x: str, y: str) -> int:
        if x not in self.arcs.keys():
            raise f"{x} not in arcs"
        for arc in self.arcs[x]:
            if arc[1] == y:
                return arc[0]
        raise f"{y} not in {x} arcs"

    def render(self, format: str = "png") -> None:
        gv = graphviz.Digraph(format=format)
        gv.graph_attr['rankdir'] = 'LR'
        for start, value in self.arcs.items():
            for node in value:
                gv.edge(start, node)
        gv.render(f'renders/{self.filename.split("/")[-1].replace(".txt", "")}.gv')

    def parsing_txt_file(self, filename: str) -> None:
        with open(filename, "r") as graph_file:
            lines = graph_file.readlines()
            lines = list(map(lambda x: x.replace("\n", ""), lines))
            for node in range(int(lines[0])):
                node = str(node)
                self.nodes.append(Node(node, None))
                self.arcs[node] = []
            for i in range(int(lines[1])):
                line = lines[2 + i].split(" ")
                self.add_arc(line[0], line[2], line[1])
