class Node:
    def __init__(self, node_type, name, text):
        self.node_type = node_type
        self.name = name
        self.text = text
        self.connections = []

    def add_connection(self, node):
        self.connections.append(node)

    def __str__(self):
        return f"{self.name}=>{self.node_type}: {self.text}"


class Flowchart:
    def __init__(self, name):
        self.name = name
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def __str__(self):
        return '\n'.join(str(node) for node in self.nodes)


class DSL:
    @staticmethod
    def generate_flowchart_dsl(flowchart):
        return str(flowchart)


def translate_pseudocode_to_dsl(pseudocode):
    flowchart = Flowchart("main")
    current_node = None

    for line in pseudocode.split('\n'):
        line = line.strip()
        if line.startswith("if"):
            condition = line.split("if")[1].strip()
            node = Node("condition", f"cond{len(flowchart.nodes)}", condition)
            flowchart.add_node(node)
            if current_node:
                current_node.add_connection(node)
            current_node = node
        elif line.startswith("else"):
            node = Node("operation", f"op{len(flowchart.nodes)}", "else")
            flowchart.add_node(node)
            if current_node:
                current_node.add_connection(node)
            current_node = node
        elif line.startswith("for"):
            operation = line.split("for")[1].strip()
            node = Node("operation", f"op{len(flowchart.nodes)}", operation)
            flowchart.add_node(node)
            if current_node:
                current_node.add_connection(node)
            current_node = node
        elif line.startswith("return"):
            operation = line.split("return")[1].strip()
            node = Node("end", f"e{len(flowchart.nodes)}", operation)
            flowchart.add_node(node)
            if current_node:
                current_node.add_connection(node)
            current_node = None
        elif line:
            node = Node("subroutine", f"sub{len(flowchart.nodes)}", line)
            flowchart.add_node(node)
            if current_node:
                current_node.add_connection(node)
            current_node = node

    return DSL.generate_flowchart_dsl(flowchart)


# Example usage:
pseudocode = """
if a > b:
    print("a is greater than b")
else:
    print("b is greater than a")
return "done"
"""

dsl_representation = translate_pseudocode_to_dsl(pseudocode)
print(dsl_representation)
