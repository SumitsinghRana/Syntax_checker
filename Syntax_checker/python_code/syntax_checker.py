import ast
import graphviz

class ASTVisualizer(ast.NodeVisitor):
    def __init__(self, friendly_labels=False):
        self.graph = graphviz.Digraph(format="svg")  # Generate SVG (for HTML)
        self.node_count = 0
        self.friendly_labels = friendly_labels  # Toggle mode

    def visit(self, node):
        """Visit a node and add it to the graph."""
        node_id = str(self.node_count)
        raw_label = type(node).__name__
        friendly_label = self.get_friendly_label(node)

        # Tooltip for explanation
        tooltip = f"Raw: {raw_label}\\nMeaning: {friendly_label}"

        # Display label based on mode
        label = raw_label if not self.friendly_labels else friendly_label

        self.graph.node(
            node_id,
            label=label,
            shape="box",
            style="filled",
            fillcolor=self.get_node_color(node),
            tooltip=tooltip
        )

        parent_id = self.node_count - 1 if self.node_count > 0 else None
        if parent_id is not None:
            self.graph.edge(str(parent_id), node_id)

        self.node_count += 1
        super().visit(node)

    def get_friendly_label(self, node):
        """Convert AST node names into readable explanations."""
        if isinstance(node, ast.Name):
            return f"Variable: {node.id}"
        elif isinstance(node, ast.BinOp):
            return "Math Operation (+, -, *, /)"
        elif isinstance(node, ast.Gt):
            return "Greater than (>)"
        elif isinstance(node, ast.Lt):
            return "Less than (<)"
        elif isinstance(node, ast.Eq):
            return "Equal (==)"
        elif isinstance(node, ast.Assign):
            return "Assignment (Variable = Value)"
        elif isinstance(node, ast.Call):
            return f"Function Call: {getattr(node.func, 'id', 'Unknown')}"
        elif isinstance(node, ast.Return):
            return "Return Statement"
        elif isinstance(node, ast.Constant):
            return f"Constant Value: {node.value}"
        elif isinstance(node, ast.If):
            return "If Condition"
        else:
            return type(node).__name__

    def get_node_color(self, node):
        """Assign colors based on node types."""
        if isinstance(node, ast.FunctionDef):
            return "lightblue"
        elif isinstance(node, ast.Assign):
            return "lightgreen"
        elif isinstance(node, ast.BinOp):
            return "yellow"
        elif isinstance(node, ast.Call):
            return "pink"
        elif isinstance(node, ast.If):
            return "red"
        elif isinstance(node, ast.Compare):
            return "orange"
        else:
            return "gray"

    def visualize(self, code):
        """Parse code and generate AST visualization."""
        tree = ast.parse(code)
        self.visit(tree)
        filename = "output/ast_visualization"
        self.graph.render(filename, view=False)  # Save as SVG

        # Generate HTML with interactive SVG
        self.generate_html(filename + ".svg")

    def generate_html(self, svg_file):
        """Create an interactive HTML file with tooltips and toggle switch."""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>AST Visualization</title>
            <style>
                body {{ text-align: center; font-family: Arial, sans-serif; }}
                .container {{ display: flex; flex-direction: column; align-items: center; }}
                button {{ margin: 10px; padding: 10px; font-size: 16px; cursor: pointer; }}
            </style>
            <script>
                function toggleLabels() {{
                    var svg = document.getElementById("ast-svg");
                    var friendly = svg.getAttribute("data-friendly") === "true";
                    svg.setAttribute("data-friendly", !friendly);
                    location.reload(); // Refresh to regenerate with new labels
                }}
            </script>
        </head>
        <body>
            <div class="container">
                <h2>Abstract Syntax Tree (AST) Visualization</h2>
                <button onclick="toggleLabels()">Toggle Labels</button>
                <embed id="ast-svg" src="{svg_file}" type="image/svg+xml" width="100%" />
            </div>
        </body>
        </html>
        """
        with open("output/ast_visualization.html", "w", encoding="utf-8") as f:
            f.write(html_content)

# Example usage
if __name__ == "__main__":
    code = """
def add(a, b):
    result = a + b
    return result

x = add(5, 10)
if x > 10:
    print("Greater")
"""
    visualizer = ASTVisualizer(friendly_labels=False)
    visualizer.visualize(code)
    print("Visualization generated: Open output/ast_visualization.html")
