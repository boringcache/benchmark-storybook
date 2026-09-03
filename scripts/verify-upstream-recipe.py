#!/usr/bin/env python3
"""Fail when the Storybook sandbox plan drifts from generated upstream CI."""

from __future__ import annotations

import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = ["corepack", "yarn", "task", "build", "--template", "react-vite/default-ts", "--no-link", "-s", "build"]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> int:
    try:
        plan = tomllib.loads((ROOT / ".boringcache.toml").read_text())
        require(plan["adapters"]["nx"]["command"] == EXPECTED, "Storybook plan changed")
        upstream = (ROOT / "upstream/scripts/ci/sandboxes.ts").read_text()
        require("command: `yarn task build --template ${key} --no-link -s build`" in upstream, "generated CircleCI build command changed")
        require("'react-vite/default-ts'" in upstream, "upstream react-vite template key changed")
        require("name: 'Create Sandbox'" in upstream, "upstream sandbox prerequisite changed")
        action = (ROOT / ".github/actions/storybook-nx-benchmark/action.yml").read_text()
        require("run-benchmark-plan.py nx --working-directory upstream" in action, "workflow bypasses the plan")
        require(
            "yarn task --task sandbox --start-from=auto --template react-vite/default-ts --no-link --debug" in action,
            "workflow omits Storybook's automatic sandbox dependency chain",
        )
        require(
            "test -s storybook-sandboxes/react-vite-default-ts/storybook-static/index.html" in action,
            "workflow does not verify Storybook's configured sandbox output",
        )
        require("yarn nx run bench/" not in action, "retired GitHub Nx recipe remains")

        node_version = (ROOT / "upstream/.nvmrc").read_text().strip()
        workflow_paths = (
            ROOT / ".github/workflows/storybook-benchmark.yml",
            ROOT / ".github/workflows/storybook-fresh-benchmark.yml",
        )
        for workflow_path in workflow_paths:
            node_inputs = [
                line.strip()
                for line in workflow_path.read_text().splitlines()
                if line.strip().startswith("node_version:")
            ]
            require(node_inputs, f"{workflow_path.name} has no Node version input")
            require(
                all(line == f'node_version: "{node_version}"' for line in node_inputs),
                f"{workflow_path.name} does not use upstream Node {node_version}",
            )

        sync = (ROOT / ".github/workflows/sync.yml").read_text()
        require("storybook-benchmark.yml" in sync, "sync omits the rolling Node pin")
        require("storybook-fresh-benchmark.yml" in sync, "sync omits the fresh Node pins")
        require("pinned_count" not in sync, "sync assumes a fixed provider count")
    except (KeyError, OSError, RuntimeError, tomllib.TOMLDecodeError) as error:
        print(f"Storybook recipe mismatch: {error}", file=sys.stderr)
        return 1
    print("Verified Storybook's generated react-vite sandbox build plan.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
