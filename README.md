# Patch: Two-Stage Real Health Check

## What changed
- **Stage 1 — TCP Fast Filter:** All configs get a lightweight TCP handshake test with **100 concurrent workers**. Only the **top 2000 fastest** survive.
- **Stage 2 — Real Xray Test:** Those 2000 configs get validated with **xray-core** (spin up SOCKS5 proxy + real HTTP request). Only working proxies are published.

## Files to replace
1. `src/core/xray_builder.py`   — NEW
2. `src/core/tester.py`        — REPLACE
3. `src/config/settings.py`   — REPLACE
4. `.github/workflows/collector.yml` — REPLACE
5. `.env.example`               — REPLACE

## Performance estimate
| Stage | Configs | Workers | Avg time | Total |
|-------|---------|---------|----------|-------|
| TCP filter | 12,000 | 100 | ~0.5s | ~60s |
| Xray real test | 2,000 | 8 | ~5s | ~21 min |
| **Total** | — | — | — | **~22 min** |

Well within the 30-minute GitHub Actions timeout.

## Environment variables
| Var | Default | Description |
|-----|---------|-------------|
| `TCP_FILTER_LIMIT` | 2000 | How many top TCP-fast configs go to xray test |
| `TCP_FILTER_WORKERS` | 100 | Concurrent TCP handshake workers |
| `TCP_FILTER_TIMEOUT` | 2.0s | TCP connect timeout in stage 1 |
| `MAX_WORKERS` | 8 | Concurrent xray real-test workers |
| `PING_TIMEOUT` | 8.0s | HTTP timeout through xray proxy |
| `LATENCY_THRESHOLD_MS` | 5000 | Max acceptable latency for published configs |

## Local testing
```bash
# 1. Install xray-core
curl -L -o xray.zip https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-64.zip
unzip xray.zip -d /usr/local/bin/
chmod +x /usr/local/bin/xray

# 2. Run
python -m src.main
```
