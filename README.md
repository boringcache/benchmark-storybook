# benchmark-storybook

Public Storybook benchmark runner for BoringCache vs GitHub Actions cache. Exercises the [Storybook](https://github.com/storybookjs/storybook) Nx workspace as the upstream source.

This repo exists separately from [`boringcache/benchmarks`](https://github.com/boringcache/benchmarks) so the benchmark keeps:

- one pinned upstream source commit (Storybook)
- isolated GitHub Actions cache usage
- one shared BoringCache workspace name: `boringcache/benchmarks`
- independent workflow history plus upstream-sync-driven benchmark runs and manual dispatches

## Source Model

- Upstream source lives in the pinned `upstream/` submodule pointing at `storybookjs/storybook`.

Pinned upstream source:

- see committed `upstream/` submodule on `main`

## What It Measures

This benchmark exercises the Nx self-hosted remote cache (`mode: nx-proxy` in `boringcache/one` v1.12.75+) alongside a hybrid local archive of `upstream/.nx/cache` for fair warm/rolling parity with `actions/cache`.

Fresh lane runs the same scenario set for each backend:

- `cold`
- `warm1`

Rolling lane records only the first build after upstream sync and intentionally skips `warm1`.

The story this benchmark is meant to show is:

- speed on fresh cold and warm paths
- first-build behavior after upstream sync in the rolling lane
- storage footprint in each backend
- whether the Nx remote cache plus local `.nx/cache` archive stays reliable on fresh runners

## Token Model

This repo uses split BoringCache tokens as the standard CI shape:

- `BORINGCACHE_RESTORE_TOKEN` for read-only restore and proxy access
- `BORINGCACHE_SAVE_TOKEN` for trusted write paths
- `BORINGCACHE_API_TOKEN` only where a single bearer variable is still required for compatibility
