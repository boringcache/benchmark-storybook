# BoringCache Storybook benchmark

This repository contains the BoringCache benchmark for Storybook.

Benchmark workflows are in [`.github/workflows/`](.github/workflows/), with configuration in [`.boringcache.toml`](.boringcache.toml).

The workflows install and build the pinned Storybook source on fresh runners.
`boringcache/one` owns Nx cache setup, restore, save, and evidence; this
repository retains the product evidence without reimplementing its correctness
contract.
