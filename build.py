"""Genera dist/simple_export-<version>.zip, instalable en Blender 4.0+.

Uso:  python build.py
"""

import os
import re
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
MODULE = "simple_export"
FILES = [
    "__init__.py",
    "properties.py",
    "operators.py",
    "panels.py",
    "utils.py",
    "blender_manifest.toml",
    "LICENSE",
]


def main():
    with open(os.path.join(ROOT, "blender_manifest.toml"), encoding="utf-8") as f:
        version = re.search(r'^version\s*=\s*"([^"]+)"', f.read(), re.M).group(1)

    dist = os.path.join(ROOT, "dist")
    os.makedirs(dist, exist_ok=True)
    out = os.path.join(dist, "%s-%s.zip" % (MODULE, version))

    # Todo dentro de una carpeta "simple_export/" para que funcione tanto
    # como add-on clasico (4.0/4.1) como extension (4.2+)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for name in FILES:
            z.write(os.path.join(ROOT, name), MODULE + "/" + name)

    print("Built " + out)


if __name__ == "__main__":
    main()
