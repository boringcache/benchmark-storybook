# benchmark-storybook

Public Storybook benchmark runner for BoringCache vs GitHub Actions cache. Exercises the [Storybook](https://github.com/storybookjs/storybook) Nx workspace as the upstream source.

This repo exists separately from [`boringcache/benchmarks`](https://github.com/boringcache/benchmarks) so the benchmark keeps:

- one pinned upstream source commit (Storybook)
- isolated GitHub Actions cache usage
- one per-repo BoringCache workspace name: `boringcache/benchmark-storybook`
- independent workflow history plus upstream-sync-driven benchmark runs and manual dispatches

## Source Model

- Upstream source lives in the pinned `upstream/` submodule pointing at `storybookjs/storybook`.

Pinned upstream source:

- see committed `upstream/` submodule on `main`

## What It Measures

This benchmark compares BoringCache's Nx self-hosted remote cache (`mode: nx-proxy` in `boringcache/one` v1.12.75+) with GitHub Actions cache restoring Nx's local task-cache paths.

The measured build runs Storybook's cacheable Nx target `bench/react-vite-default-ts:build` from the upstream workspace root. It intentionally avoids `code/yarn build`, which bypasses Nx, and the full Storybook `run-many --target=build`, which pulls in the broader sandbox/repro matrix.

Source preparation removes Storybook's checked-in Nx Cloud workspace binding from the temporary checkout. The benchmark measures BoringCache's self-hosted Nx proxy against the actions/cache local `.nx/cache` path, not Storybook's private Nx Cloud workspace.

Fresh lane runs the same scenario set for each backend:

- `cold`
- `warm1`

Rolling lane records only the first build after upstream sync and intentionally skips `warm1`.

The story this benchmark is meant to show is:

- speed on fresh cold and warm paths
- first-build behavior after upstream sync in the rolling lane
- storage footprint in each backend
- whether Nx cache reuse stays reliable on fresh runners

The BoringCache lane archives Yarn dependency state only. It does not archive
`upstream/.nx/cache` or `upstream/.nx/workspace-data`; those paths are the
local Nx cache surface used by the actions/cache lane.

## Token Model

This repo uses split BoringCache tokens as the standard CI shape:

- `BORINGCACHE_RESTORE_TOKEN` for read-only restore and proxy access
- `BORINGCACHE_SAVE_TOKEN` for trusted write paths
- `BORINGCACHE_API_TOKEN` only where a single bearer variable is still required for compatibility
