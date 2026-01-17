"""
D4GameEnhancer Build Script
Builds .nvda-addon file from source
"""

import re
import zipfile
from pathlib import Path


def get_version(manifest_path: Path) -> str:
    """Parse version from manifest.ini"""
    content = manifest_path.read_text(encoding="utf-8")
    match = re.search(r"^version\s*=\s*(.+)$", content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "0.0.0"


def build():
    root = Path(__file__).parent.parent
    dist = root / "dist"
    dist.mkdir(exist_ok=True)

    manifest = root / "manifest.ini"
    version = get_version(manifest)

    addon_name = f"D4GameEnhancer-v{version}.nvda-addon"
    addon_path = dist / addon_name

    # Remove old build
    if addon_path.exists():
        addon_path.unlink()

    # Create zip with .nvda-addon extension
    with zipfile.ZipFile(addon_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add manifest.ini
        zf.write(manifest, "manifest.ini")

        # Add globalPlugins/ (recursive, excluding CLAUDE.md)
        global_plugins = root / "globalPlugins"
        for file in global_plugins.rglob("*"):
            if file.is_file() and file.name != "CLAUDE.md":
                arcname = file.relative_to(root)
                zf.write(file, arcname)

    print(f"Built: {addon_path}")
    print(f"Size: {addon_path.stat().st_size:,} bytes")
    return addon_path


if __name__ == "__main__":
    build()
