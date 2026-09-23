#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
scope="${1:-}"

if [[ ! "$scope" =~ ^[a-z0-9][a-z0-9._-]+$ ]]; then
  echo "Expected a lowercase benchmark cache scope, got: ${scope:-<empty>}" >&2
  exit 1
fi

config_path="${repo_root}/.boringcache.toml"
for name in nx-cache nx-workspace-data; do
  old_tag="storybook-${name}-local"
  new_tag="${scope}-${name}"
  if ! grep -Fq "tag = \"${old_tag}\"" "$config_path"; then
    echo "Missing expected local tag in ${config_path}: ${old_tag}" >&2
    exit 1
  fi
  sed -i.bak "s/tag = \"${old_tag}\"/tag = \"${new_tag}\"/" "$config_path"
  rm -f "${config_path}.bak"
done

echo "Scoped the BoringCache Storybook cache to ${scope}."
