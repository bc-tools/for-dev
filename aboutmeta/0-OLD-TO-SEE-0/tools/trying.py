from rich.tree import Tree
from rich.console import Console

data = {
    "docs": {
        "intro.md": None,
        "install.md": None
    },
    "src": {
        "main.py": None,
        "utils": {
            "math.py": None,
            "string.py": None
        }
    },
    "README.md": None
}

def build_tree(data: dict, tree: Tree) -> None:
    for key, value in data.items():
        if isinstance(value, dict):
            branch = tree.add(f"[bold cyan]{key}/[/]")
            build_tree(value, branch)
        else:
            tree.add(f"[green]{key}[/]")

console = Console()
root = Tree("[bold magenta]project_root[/]")
build_tree(data, root)
console.print(root)
