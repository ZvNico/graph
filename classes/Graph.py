from typing import List, Tuple

import graphviz
from prettytable import PrettyTable

from .Arc import Arc
from .Enum import *
from .Node import Node


class Graph:
    def __init__(self, filename: str = "graph/graph.txt"):
        self.nodes = []
        self.arcs = {}
        self.filename = filename
        self.historique = []
        self.parsing_txt_file(filename=filename)

    def __str__(self):
        chaine = "nodes:"
        for node in self.nodes:
            chaine += " " + node
        chaine += "\n"
        for arcs in self.arcs.values():
            for arc in arcs:
                chaine += f"{arc.start} ==({arc.dist})==> {arc.end}\n"
        return chaine

    def str_matrix(self, matrix):
        column_names = [node.name for node in self.nodes]
        row_names = [node.name for node in self.nodes]
        pt = PrettyTable()
        pt.field_names = ["Node"] + column_names
        for i in range(len(self.nodes)):
            pt.add_row(
                [row_names[i]] + [matrix[i][j] if matrix[i][j] is not None else "X" for j in range(len(self.nodes))])
        return str(pt)

    def adjacency_matrix(self) -> List[list]:
        matrix = []
        for i, node1 in enumerate(self.nodes):
            matrix.append([])
            for j, node2 in enumerate(self.nodes):
                matrix[i].append("V" if node2 in self.children(node1) else "F")
        return matrix

    def add_arc(self, x, y, value) -> None:
        if x not in self.arcs.keys():
            raise f"{x} not in arcs"
        self.arcs[x].append(Arc(self.find_node(x), self.find_node(y), value))

    def find_node(self, name: str):
        for node in self.nodes:
            if node.name == name:
                return node
        return -1

    def rank_compute(self, mode: RankComputeMode) -> int:
        if RankComputeMode.starting_node_elimination:
            graph = Graph("temp/temp.txt")
            r = 1
            while not self.are_all_nodes_ranked():
                entry_points = graph.entry_points()
                if len(entry_points) == 0:
                    for node in self.nodes:
                        node.rang = None
                    return -1
                for entry in entry_points:
                    graph.nodes.remove(entry)
                    graph.arcs[entry.name] = []
                    self.find_node(entry.name).rang = r
                r += 1
            del graph
            return 0

    def entry_points(self) -> List[Node]:
        entry_points = []
        for node in self.nodes:
            if len(self.parents(node)) == 0:
                entry_points.append(node)
        return entry_points

    def exit_points(self) -> List[Node]:
        exit_points = []
        for node in self.nodes:
            if len(self.children(node)) == 0:
                exit_points.append(node)
        return exit_points

    def unique_entry_point(self) -> bool:
        return len(self.entry_points()) == 1

    def unique_exit_point(self) -> bool:
        return len(self.exit_points()) == 1

    def are_all_nodes_ranked(self) -> bool:
        for node in self.nodes:
            if node.rang is None:
                return False
        return True

    def parents(self, node: Node) -> List[Node]:
        parents = []
        for arcs in self.arcs.values():
            for arc in arcs:
                if arc.end == node:
                    parents.append(arc.start)
        return parents

    def children(self, node: Node) -> Tuple[Node]:
        return tuple(arc.end for arc in self.arcs[node.name])

    def dist(self, x: str, y: str) -> int:
        if x not in self.arcs.keys():
            raise f"{x} not in arcs"
        for arc in self.arcs[x]:
            if arc.end == y:
                return arc.dist
        raise f"{y} not in {x} arcs"

    def render(self, path: str, filename: str, format: str = "png") -> None:
        gv = graphviz.Digraph(format=format)
        gv.attr(bgcolor="transparent")
        gv.attr(rankdir="LR")
        for node in self.nodes:
            if node.rang is not None:
                gv.node(node.name, xlabel=str(node.rang), shape="circle", style="filled",
                        fillcolor="white")
            else:
                gv.node(node.name, shape="circle", style="filled",
                        fillcolor="white")
        for arcs in self.arcs.values():
            for arc in arcs:
                gv.edge(arc.start.name, arc.end.name, label=arc.dist)
        gv.render(f"{path}{filename}")

    def write_txt_file(self, filename: str) -> None:
        with open(filename, "w") as graph_file:
            lines = [str(len(self.nodes)), str(len(self.arcs))]
            for arcs in self.arcs.values():
                for arc in arcs:
                    lines.append(f"{arc.start.name} {arc.end.name} {arc.dist}")
            for line in lines:
                graph_file.write(line + "\n")

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
                self.add_arc(line[0], line[1], line[2])
