from dataclasses import dataclass


@dataclass
class Node:
    name: str
    rang: int

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.name == other.name
