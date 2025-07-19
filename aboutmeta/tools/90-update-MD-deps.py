import subprocess
import re

def get_pip_freeze_lines(env="debug"):
    try:
        result = subprocess.run(
            ["hatch", "run", f"{env}:pip", "freeze"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        print("Erreur pip freeze:", e.stderr)
        return []

def parse_freeze(lines):
    deps = []
    for line in lines:
        if line.startswith("-e git+"):
            continue
        match = re.match(r"([^=<>~!]+)==(.+)", line)
        if match:
            deps.append((match.group(1), match.group(2)))
    return deps

if __name__ == "__main__":
    lines = get_pip_freeze_lines()
    for name, version in parse_freeze(lines):
        print(f"{name}  [{version}]")
