# V2Ray Config Collector

An automated collector that fetches free V2Ray / proxy configs from public
subscription sources and Telegram channels, health-checks them, tags them
by country, and publishes clean, deduplicated subscription files — updated
every 2 hours via GitHub Actions.

This project combines the useful ideas from a few common single-purpose
collector scripts (Telegram scraping, country tagging, base64 subscription
output) while fixing the gaps that tend to show up in them: no
deduplication across runs, no health checking, sequential/slow fetching,
and silent failure on errors.

## Features

- **Multiple source types**: plain-text/base64 subscription URLs *and*
  public Telegram channel previews (no bot token needed for scraping).
- **Deduplication**: configs are deduplicated by protocol + host + port +
  credentials, not by their (often cosmetic) remark — so re-running the
  collector never lets duplicate entries pile up.
- **Health checking**: every config gets a concurrent TCP reachability
  test before publishing; only configs under the latency threshold make
  it into the output.
- **Country tagging**: batched GeoIP lookups (up to 100 hosts per HTTP
  call) instead of one request per config.
- **Multiple export formats**: grouped by protocol, by country, by
  network type, an all-in-one `mix.txt`, and a base64 `mix_sub.txt`
  subscription link — written atomically so a failed run never leaves a
  half-written file.
- **Config-driven, testable code**: fetch / parse / dedup / test /
  export are separate modules, each covered by unit tests.

## Project layout

```
src/
  config/     settings + source list
  core/       fetcher, parser, dedup, geoip, tester, exporter, notifier
  models/     Config + Protocol dataclasses
  utils/      logging, base64 helpers
tests/        unit tests for every core module
.github/workflows/
  collector.yml   scheduled run, every 2 hours
  tests.yml       CI test run on push / PR
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # optional — defaults work out of the box
python -m src.main
```

Output is written to `configs/` (protocol files, country files,
`mix.txt`, `mix_sub.txt`, and `stats.json`).

## Running tests

```bash
pip install -r requirements-dev.txt
pytest
```

## Deploying via GitHub Actions

1. Push this repository to GitHub.
2. (Optional) add `TELEGRAM_TOKEN` / `TELEGRAM_CHAT_ID` repository
   secrets if you want a run-summary notification.
3. The `Collect V2Ray Configs` workflow runs every 2 hours automatically
   and commits updated files under `configs/` back to the repo. You can
   also trigger it manually from the Actions tab.

## Configuration

All tunables live in environment variables — see `.env.example`:
concurrency, timeouts, latency threshold, how many Telegram messages to
scan per channel, and whether GeoIP tagging is enabled.

To add or remove sources, edit `src/config/sources.py`.

## Disclaimer

⚠️ Configs are collected automatically from public sources and are not
vetted for trustworthiness. Don't send sensitive traffic through configs
you don't control. This project is provided for research and censorship
circumvention purposes.

## License

MIT — see [LICENSE](LICENSE).
