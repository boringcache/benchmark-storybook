#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
scenario="${1:-base}"

git -C "${repo_root}/upstream" reset --hard
git -C "${repo_root}/upstream" clean -fdx

nx_json="${repo_root}/upstream/nx.json"
if [[ -f "${nx_json}" ]]; then
  node - "${nx_json}" <<'JS'
const fs = require('fs');

const nxJsonPath = process.argv[2];
const nxJson = JSON.parse(fs.readFileSync(nxJsonPath, 'utf8'));
let changed = false;

for (const key of ['nxCloudId', 'nxCloudAccessToken', 'nxCloudUrl']) {
  if (Object.prototype.hasOwnProperty.call(nxJson, key)) {
    delete nxJson[key];
    changed = true;
  }
}

if (changed) {
  fs.writeFileSync(nxJsonPath, `${JSON.stringify(nxJson, null, 2)}\n`);
  console.log('Removed Storybook Nx Cloud workspace binding for benchmark run');
}
JS
fi

case "${scenario}" in
  base|warm1)
    ;;
  *)
    echo "Unknown scenario: ${scenario}" >&2
    exit 1
    ;;
esac

git -C "${repo_root}/upstream" status --short
