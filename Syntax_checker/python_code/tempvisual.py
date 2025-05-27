import ast
import graphviz
import os

class ASTVisualizer(ast.NodeVisitor):
    def __init__(self):
        self.graph = graphviz.Digraph(format="png")
        self.graph.attr(rankdir="TB")  # Top-to-bottom for compact layout
        self.node_count = 0
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)  # Ensure output folder exists

    def get_label(self, node):
        """Generate human-readable labels for AST nodes."""
        if isinstance(node, ast.BinOp):
            return f"BinaryOp ({self.op_to_symbol(node.op)})"
        elif isinstance(node, ast.Call):
            return f"Call\n(Func: {self.get_func_name(node)})"
        elif isinstance(node, ast.FunctionDef):
            return f"Function\n(Name: {node.name})"
        elif isinstance(node, ast.Assign):
            return f"Assign\n(Var: {self.get_var_name(node)})"
        elif isinstance(node, ast.Compare):
            return f"Compare ({self.op_to_symbol(node.ops[0])})"
        elif isinstance(node, ast.If):
            return "If Condition"
        elif isinstance(node, ast.Return):
            return "Return"
        elif isinstance(node, ast.Name):
            return f"Var ({node.id})"
        elif isinstance(node, ast.Constant):
            return f"Const ({node.value})"
        return type(node).__name__

    def op_to_symbol(self, op):
        """Convert AST operator types to symbols."""
        symbols = {
            ast.Add: "+", ast.Sub: "-", ast.Mult: "*", ast.Div: "/",
            ast.Mod: "%", ast.Pow: "**", ast.Eq: "==", ast.NotEq: "!=",
            ast.Lt: "<", ast.LtE: "<=", ast.Gt: ">", ast.GtE: ">=",
            ast.And: "and", ast.Or: "or", ast.Not: "not"
        }
        return symbols.get(type(op), "?")

    def get_func_name(self, node):
        """Extract function name from a call node."""
        if isinstance(node.func, ast.Name):
            return node.func.id
        return "Unknown"

    def get_var_name(self, node):
        """Extract variable name from an assignment."""
        if isinstance(node.targets[0], ast.Name):
            return node.targets[0].id
        return "Unknown"

    def visit(self, node, parent_id=None):
        """Visit a node and add it to the graph."""
        node_id = str(self.node_count)
        label = self.get_label(node)

        color = self.get_node_color(node)
        self.graph.node(node_id, label, style="filled", fillcolor=color, shape="box")

        # Connect to the parent node if exists
        if parent_id is not None:
            self.graph.edge(parent_id, node_id)

        self.node_count += 1

        # Recursively visit child nodes
        for child in ast.iter_child_nodes(node):
            self.visit(child, node_id)

    def get_node_color(self, node):
        """Assign colors based on node types."""
        if isinstance(node, ast.FunctionDef):
            return "lightblue"
        elif isinstance(node, ast.BinOp):
            return "yellow"
        elif isinstance(node, ast.Call):
            return "pink"
        elif isinstance(node, ast.Assign):
            return "lightgreen"
        elif isinstance(node, ast.If):
            return "red"
        return "lightgray"

    def visualize(self, code):
        """Parse code and generate AST visualization."""
        tree = ast.parse(code)
        self.visit(tree)  # Start traversal from root
        file_path = os.path.join(self.output_dir, "ast_visualization")
        self.graph.render(file_path, view=True)  # Save and open the image

# Example usage
if __name__ == "__main__":
    code = """
def multiply(a, b):
    result = a * b
    if result > 10:
        return result
    return 0

y = multiply(4, 3)
"""
    visualizer = ASTVisualizer()
    visualizer.visualize(code)
