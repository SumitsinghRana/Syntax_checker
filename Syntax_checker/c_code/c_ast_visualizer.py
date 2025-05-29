from pycparser import c_parser, c_ast
import graphviz
import os  

class CASTVisualizer:
    def __init__(self):
        self.graph = graphviz.Digraph(format="png")
        self.graph.attr(rankdir="TB")
        self.node_count = 0
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)

    def get_label(self, node):
        """Generate human-readable labels for C AST nodes."""
        if isinstance(node, c_ast.ID):
            return f"ID ({node.name})"
        elif isinstance(node, c_ast.Constant):
            return f"Const ({node.value})"
        elif isinstance(node, c_ast.FuncDef):
            return f"FuncDef ({node.decl.name})"
        elif isinstance(node, c_ast.Decl):
            return f"Decl ({node.name})"
        elif isinstance(node, c_ast.BinaryOp):
            return f"BinaryOp ({node.op})"
        elif isinstance(node, c_ast.If):
            return "If Statement"
        elif isinstance(node, c_ast.Return):
            return "Return"
        return type(node).__name__

    def get_node_color(self, node):
        """Assign colors based on node types."""
        if isinstance(node, c_ast.FuncDef):
            return "lightblue"
        elif isinstance(node, c_ast.Decl):
            return "lightgreen"
        elif isinstance(node, c_ast.BinaryOp):
            return "yellow"
        elif isinstance(node, c_ast.If):
            return "red"
        return "lightgray"

    def visit(self, node, parent_id=None):
        node_id = str(self.node_count)
        label = self.get_label(node)
        color = self.get_node_color(node)
        self.graph.node(node_id, label, style="filled", fillcolor=color, shape="box")

        if parent_id is not None:
            self.graph.edge(parent_id, node_id)

        self.node_count += 1

        for child_name, child in node.children():
            self.visit(child, node_id)

    def visualize(self, code):
        parser = c_parser.CParser()
        try:
            ast_tree = parser.parse(code)
        except Exception as e:
            return f"❌ Syntax Error: {e}"

        self.visit(ast_tree)
        file_path = os.path.join(self.output_dir, "c_ast_visualization")
        self.graph.render(file_path)
        return file_path + ".png"

# Example usage
if __name__ == "__main__":
    c_code = """
    int main() {
        int a = 5;
        if (a > 2) {
            a = a + 1;
        }
        return a;
    }
    """
    visualizer = CASTVisualizer()
    result = visualizer.visualize(c_code)
    if result.endswith(".png"):
        print("C AST visualization saved at:", result)
    else:
        print(result)
