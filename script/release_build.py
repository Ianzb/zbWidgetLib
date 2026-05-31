#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import *

import json
import argparse

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def write_text(path: str, content: str):
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)


def get_current_version():
    import toml
    data = toml.load(PYPROJECT_TOML)
    return data["project"]["version"]


def replace_pyproject_toml(version: str):
    import toml
    data = toml.load(PYPROJECT_TOML)
    data["project"]["version"] = version
    with open(PYPROJECT_TOML, "w", encoding="utf-8") as file:
        toml.dump(data, file)
    print("已修改pyproject.toml版本号！")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", required=False, help="版本号")
    args = parser.parse_args()
    version = args.version

    current_version = get_current_version()
    if not version:
        version = current_version

    replace_pyproject_toml(version)

    out = {
        "version": version,
    }

    out_path = os.path.join(ROOT, "script", "release_output.json")
    print("打包结果：", out)
    write_text(out_path, json.dumps(out, ensure_ascii=False, indent=4))
