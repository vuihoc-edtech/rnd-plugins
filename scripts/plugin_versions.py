#!/usr/bin/env python3
"""Quản lý và đồng bộ phiên bản (SemVer) cho các plugin trong kho rnd-plugins.

Cách dùng:
  python3 scripts/plugin_versions.py status
  python3 scripts/plugin_versions.py check
  python3 scripts/plugin_versions.py bump vuihoc-content-authoring patch
  python3 scripts/plugin_versions.py bump vuihoc-content-authoring --set 1.1.0
  python3 scripts/plugin_versions.py bump all patch
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
PLUGINS_DIR = ROOT / "plugins"

SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)

PLUGIN_MANIFEST_RELPATHS: tuple[str, ...] = (
    ".claude-plugin/plugin.json",
    ".codex-plugin/plugin.json",
    ".cursor-plugin/plugin.json",
    "gemini-extension.json",
    "plugin.json",
)

ROOT_MARKETPLACES: tuple[tuple[Path, tuple[str, ...]], ...] = (
    (ROOT / ".claude-plugin" / "marketplace.json", ("metadata", "version")),
    (ROOT / ".cursor-plugin" / "marketplace.json", ("metadata", "version")),
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def parse_semver(version: str) -> tuple[int, int, int]:
    match = SEMVER_RE.match(version)
    if not match:
        raise ValueError(f"Phiên bản không đúng chuẩn SemVer (MAJOR.MINOR.PATCH): {version!r}")
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def next_semver(current: str, part: str) -> str:
    major, minor, patch = parse_semver(current)
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    if part == "patch":
        return f"{major}.{minor}.{patch + 1}"
    parse_semver(part)
    return part


def plugin_dirs() -> list[Path]:
    if not PLUGINS_DIR.is_dir():
        return []
    return sorted(p for p in PLUGINS_DIR.iterdir() if p.is_dir() and not p.name.startswith("."))


def plugin_manifests(plugin_dir: Path) -> list[Path]:
    return [plugin_dir / rel for rel in PLUGIN_MANIFEST_RELPATHS if (plugin_dir / rel).is_file()]


def collect_plugin_versions(plugin_dir: Path) -> dict[str, str]:
    versions: dict[str, str] = {}
    for manifest in plugin_manifests(plugin_dir):
        data = load_json(manifest)
        ver = data.get("version")
        rel = manifest.relative_to(ROOT).as_posix()
        versions[rel] = str(ver) if ver is not None else "<missing>"
    return versions


def print_status() -> int:
    print("=== Phiên bản các Plugin ===")
    for pdir in plugin_dirs():
        versions = collect_plugin_versions(pdir)
        unique = sorted(set(versions.values()))
        status = "OK" if len(unique) == 1 and SEMVER_RE.match(unique[0]) else "LỆCH/LỖI"
        ver_display = unique[0] if len(unique) == 1 else ", ".join(f"{k}={v}" for k, v in versions.items())
        manifests_str = ", ".join(Path(k).parent.name or Path(k).name for k in versions)
        print(f"  - {pdir.name:28s} v{ver_display:10s} [{status}] ({manifests_str})")

    print("\n=== Phiên bản Marketplace Root ===")
    for mp_path, keys in ROOT_MARKETPLACES:
        if mp_path.is_file():
            data = load_json(mp_path)
            cur: Any = data
            for k in keys:
                cur = cur.get(k, {}) if isinstance(cur, dict) else None
            print(f"  - {mp_path.relative_to(ROOT).as_posix():36s} v{cur}")
    return 0


def check_all() -> int:
    errors: list[str] = []
    for pdir in plugin_dirs():
        versions = collect_plugin_versions(pdir)
        if not versions:
            errors.append(f"{pdir.name}: không tìm thấy manifest nào.")
            continue
        for where, ver in versions.items():
            if not SEMVER_RE.match(ver):
                errors.append(f"{where}: version {ver!r} không hợp lệ (cần MAJOR.MINOR.PATCH).")
        unique = sorted(set(versions.values()))
        if len(unique) > 1:
            detail = ", ".join(f"{k}={v}" for k, v in versions.items())
            errors.append(f"{pdir.name}: lệch version giữa các manifest: {detail}")

        # Kiểm tra không có file .DS_Store nằm trong plugin
        for ds in pdir.rglob(".DS_Store"):
            errors.append(f"{ds.relative_to(ROOT).as_posix()}: chứa file hệ thống .DS_Store.")

    # Kiểm tra các đường dẫn plugin trong marketplace root đều tồn tại
    for mp_rel in (".claude-plugin/marketplace.json", ".cursor-plugin/marketplace.json", ".agents/plugins/marketplace.json"):
        mp_file = ROOT / mp_rel
        if not mp_file.is_file():
            continue
        mp_data = load_json(mp_file)
        for entry in mp_data.get("plugins", []):
            src = entry.get("source")
            path_str = src.get("path") if isinstance(src, dict) else src
            if isinstance(path_str, str) and path_str.startswith("./"):
                target = ROOT / path_str[2:]
                if not target.is_dir():
                    errors.append(f"{mp_rel}: plugin {entry.get('name')!r} trỏ tới {path_str!r} không tồn tại.")

    if errors:
        print("Kiểm tra thất bại:", file=sys.stderr)
        for err in errors:
            print(f"  ✗ {err}", file=sys.stderr)
        return 1

    print("✔ Tất cả phiên bản manifest và đường dẫn marketplace đều hợp lệ và đồng bộ.")
    return 0


def bump_plugin(target: str, part: str, explicit_version: str | None) -> int:
    targets = plugin_dirs() if target == "all" else [PLUGINS_DIR / target]
    for pdir in targets:
        if not pdir.is_dir():
            print(f"Không tìm thấy plugin: {pdir.name}", file=sys.stderr)
            return 1
        manifests = plugin_manifests(pdir)
        if not manifests:
            print(f"Plugin {pdir.name} không có manifest.", file=sys.stderr)
            return 1
        first_data = load_json(manifests[0])
        current_ver = str(first_data.get("version", "0.1.0"))
        new_ver = explicit_version if explicit_version else next_semver(current_ver, part)
        parse_semver(new_ver)

        for manifest in manifests:
            data = load_json(manifest)
            data["version"] = new_ver
            write_json(manifest, data)
        print(f"✔ {pdir.name}: {current_ver} -> {new_ver} ({len(manifests)} manifest)")

        # Nếu có entry version trong marketplace root thì cập nhật đồng bộ
        for mp_path, _ in ROOT_MARKETPLACES:
            if not mp_path.is_file():
                continue
            mp_data = load_json(mp_path)
            changed = False
            for entry in mp_data.get("plugins", []):
                if entry.get("name") == pdir.name and "version" in entry:
                    entry["version"] = new_ver
                    changed = True
            if changed:
                write_json(mp_path, mp_data)

    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="Hiển thị bảng phiên bản hiện tại của tất cả plugin")
    sub.add_parser("check", help="Kiểm tra tính hợp lệ và đồng bộ version trên toàn repo")

    bump = sub.add_parser("bump", help="Tăng hoặc đặt version đồng bộ cho mọi manifest của một plugin")
    bump.add_argument("plugin", help="Tên thư mục plugin (ví dụ: vuihoc-content-authoring) hoặc 'all'")
    bump.add_argument("part", choices=["patch", "minor", "major"], nargs="?", default="patch")
    bump.add_argument("--set", dest="set_version", help="Đặt thẳng phiên bản SemVer cụ thể (ví dụ: 1.2.0)")

    args = parser.parse_args()
    if args.cmd == "status":
        raise SystemExit(print_status())
    if args.cmd == "check":
        raise SystemExit(check_all())
    if args.cmd == "bump":
        raise SystemExit(bump_plugin(args.plugin, args.part, args.set_version))


if __name__ == "__main__":
    main()
