
````markdown
<div align="center">

<img src="assets/logo.jpg" alt="IdolVPN" width="180">

# ⚡ Automate V2Ray Config Collector

### Automated V2Ray / Xray Configuration Collector, Validator & Publisher

**Collect • Parse • Deduplicate • TCP Filter • Xray Test • GeoIP • Export • Automate**

<br>

[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Xray](https://img.shields.io/badge/Xray-Core-00ADD8?style=for-the-badge)](https://github.com/XTLS/Xray-core)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br>

🇬🇧 **English** &nbsp; | &nbsp; 🇮🇷 **[فارسی](#-نسخه-فارسی)**

<br>

⭐ **If you find this project useful, please give it a Star!**

</div>

---

# 🚀 Live Subscriptions

> Ready-to-use subscription links generated automatically by the collector.

### 🔥 Main Subscription

| Type | Subscription |
|---|---|
| 🌐 **Mixed** | [`mix_sub.txt`](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/mix_sub.txt) |
| 🪶 **Lite Mixed** | [`lite_mix_sub.txt`](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/lite_mix_sub.txt) |

### 📡 Protocols

| Protocol | Link |
|---|---|
| 🟢 **VLESS** | [`vless.txt`](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/vless.txt) |
| 🔵 **VMess** | [`vmess.txt`](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/vmess.txt) |
| 🟠 **Trojan** | [`trojan.txt`](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/trojan.txt) |
| 🟣 **Shadowsocks** | [`ss.txt`](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/ss.txt) |
| 🔷 **Reality** | [`reality.txt`](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/reality.txt) |
| 🟡 **WireGuard** | [`wireguard.txt`](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/wireguard.txt) |

### 📋 Combined Raw Configs

**All healthy configurations:**

```text
https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/mix.txt
````

**Base64 Subscription:**

```text
https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/mix_sub.txt
```

> 💡 لینک `mix_sub.txt` را می‌توانید مستقیماً داخل کلاینت‌های سازگار با Subscription وارد کنید.

---

# 📖 About

**Automate V2Ray Config Collector** is an automated Python-based pipeline designed to collect, process, validate, categorize, and publish V2Ray/Xray proxy configurations from multiple public sources.

Unlike a simple configuration scraper, this project performs multiple validation stages before publishing configurations.

```text
┌─────────────────────────┐
│     Public Sources      │
│ GitHub / Telegram / Raw │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   Fetch Configurations  │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│      Parse & Validate   │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│      Deduplication      │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│     Fast TCP Filter     │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│    Real Xray Testing    │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│     Latency Filter      │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│       GeoIP Lookup      │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   Categorized Outputs   │
└────────────┬────────────┘
             │
             ▼
        GitHub Repository
```

---

# ✨ Features

| Feature                   | Description                                             |
| ------------------------- | ------------------------------------------------------- |
| 🔄 Automatic Collection   | Collect configurations from multiple public sources     |
| 📡 Multiple Sources       | Raw sources, subscriptions and public Telegram channels |
| 🧩 Protocol Parsing       | Parse supported V2Ray/Xray configuration formats        |
| 🧹 Deduplication          | Remove duplicate configurations automatically           |
| ⚡ TCP Fast Filter         | Quickly eliminate unreachable endpoints                 |
| 🧪 Xray Validation        | Real proxy testing using Xray-core                      |
| 📊 Latency Measurement    | Measure and filter configurations by latency            |
| 🌍 GeoIP                  | Detect approximate server country                       |
| 📁 Categorized Output     | Group configurations by protocol, country and network   |
| 🔗 Base64 Subscription    | Generate subscription-ready Base64 output               |
| 🤖 GitHub Actions         | Automated scheduled collection                          |
| 📢 Telegram Notifications | Optional execution reports                              |
| 📈 Statistics             | Generate JSON statistics                                |
| 🪶 Lite Output            | Generate smaller configuration lists                    |

---

# 🧩 Supported Protocols

The collector currently recognizes:

* VMess
* VLESS
* Trojan
* Shadowsocks
* WireGuard
* VLESS Reality

Reality configurations are detected separately when:

```text
security=reality
```

is present.

---

# ⚡ Two-Stage Health Checking

## 1️⃣ TCP Fast Filter

Before running Xray, configurations are checked using a lightweight TCP connectivity test.

```text
Collected Configs
       │
       ▼
   TCP Filter
       │
   ┌───┴───┐
   ▼       ▼
 FAIL     PASS
   │       │
   ✕       ▼
        Xray Test
```

This removes unreachable endpoints before the more expensive Xray validation stage.

The TCP filter supports high concurrency and can keep only the fastest candidates.

---

## 2️⃣ Real Xray Validation

A reachable TCP port does not necessarily mean that a proxy actually works.

A configuration may still fail because of:

* Invalid credentials
* TLS errors
* Incorrect Reality parameters
* Invalid transport settings
* Server-side errors
* Upstream connectivity problems

Therefore, candidates are tested through **Xray-core**.

```text
Configuration
      │
      ▼
Xray Config Builder
      │
      ▼
Temporary Xray Instance
      │
      ▼
Local SOCKS5 Proxy
      │
      ▼
Real HTTP Request
      │
      ▼
Latency Measurement
      │
 ┌────┴────┐
 ▼         ▼
FAIL     HEALTHY
```

Only configurations that successfully pass the configured health-check criteria are exported.

---

# 🌍 GeoIP

Healthy configurations can be enriched with approximate geographic information.

The collector uses **ip-api.com** batch requests to resolve server IP locations.

Country information is then used to generate country-specific files.

Examples:

```text
🇩🇪 Germany
🇺🇸 United States
🇳🇱 Netherlands
🇫🇷 France
🇹🇷 Turkey
🇮🇷 Iran
```

GeoIP lookups use batching and caching to reduce unnecessary API requests.

GeoIP can be disabled through configuration.

---

# 📂 Output Files

All generated files are stored inside:

```text
configs/
```

## Protocol

```text
configs/
├── vmess.txt
├── vless.txt
├── trojan.txt
├── ss.txt
├── reality.txt
└── wireguard.txt
```

## Countries

Country-specific files are generated dynamically:

```text
configs/
├── country_IR.txt
├── country_DE.txt
├── country_US.txt
├── country_NL.txt
├── country_TR.txt
└── ...
```

## Network

```text
configs/
├── network_tcp.txt
├── network_ws.txt
├── network_grpc.txt
├── network_h2.txt
├── network_http.txt
├── network_httpupgrade.txt
├── network_xhttp.txt
├── network_raw.txt
└── network_none.txt
```

## Combined

```text
configs/
├── mix.txt
├── mix_sub.txt
├── lite_mix.txt
└── lite_mix_sub.txt
```

---

# 🔗 Subscription Links

The most important generated subscription is:

### 🌐 MIX Subscription

```text
https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/mix_sub.txt
```

### 🪶 Lite MIX Subscription

```text
https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/lite_mix_sub.txt
```

### 📋 Raw MIX

```text
https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/mix.txt
```

---

# 🌍 Country Subscriptions

Country outputs can also be used individually.

For example:

### 🇩🇪 Germany

```text
https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/country_DE.txt
```

### 🇺🇸 United States

```text
https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/country_US.txt
```

### 🇳🇱 Netherlands

```text
https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/country_NL.txt
```

### 🇹🇷 Turkey

```text
https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/country_TR.txt
```

### 🇮🇷 Iran

```text
https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/country_IR.txt
```

> Country files are generated dynamically, so additional countries may appear depending on the collected configurations.

---

# 📊 Statistics

The collector generates:

```text
configs/stats.json
```

Statistics include:

* Total healthy configurations
* Protocol distribution
* Country distribution
* Average latency

Example:

```json
{
  "total": 1234,
  "by_protocol": {},
  "by_country": {},
  "avg_latency_ms": 0
}
```

---

# 🤖 GitHub Actions

The project is designed to run automatically through GitHub Actions.

The collector workflow:

```text
⏰ Scheduled Run
      ↓
📥 Fetch Sources
      ↓
🧩 Parse
      ↓
🧹 Deduplicate
      ↓
⚡ TCP Filter
      ↓
🧪 Xray Health Check
      ↓
🌍 GeoIP
      ↓
📦 Generate Outputs
      ↓
📊 Generate Statistics
      ↓
💾 Commit Changes
```

The collector workflow is located at:

```text
.github/workflows/collector.yml
```

The workflow runs automatically every **2 hours** and can also be triggered manually.

```text
GitHub
 → Actions
 → Collect V2Ray Configs
 → Run workflow
```

---

# ⚙️ Configuration

Environment variables are documented in:

```text
_.env.example
```

Important options include:

| Variable                  | Description                       |
| ------------------------- | --------------------------------- |
| `MAX_WORKERS`             | Number of concurrent workers      |
| `FETCH_TIMEOUT`           | Source fetching timeout           |
| `PING_TIMEOUT`            | Xray test timeout                 |
| `PING_RETRIES`            | Number of retries                 |
| `LATENCY_THRESHOLD_MS`    | Maximum accepted latency          |
| `TCP_FILTER_LIMIT`        | Maximum candidates passed to Xray |
| `TCP_FILTER_WORKERS`      | TCP concurrency                   |
| `TCP_FILTER_TIMEOUT`      | TCP connection timeout            |
| `GEOIP_ENABLED`           | Enable/disable GeoIP              |
| `GEOIP_CACHE_TTL_SECONDS` | GeoIP cache lifetime              |
| `OUTPUT_DIR`              | Output directory                  |
| `LOG_LEVEL`               | Logging level                     |
| `MAX_CONFIGS_PER_OUTPUT`  | Lite output limit                 |
| `XRAY_PATH`               | Xray binary path                  |
| `TEST_URL`                | URL used for health testing       |
| `XRAY_STARTUP_DELAY`      | Xray startup delay                |

Example:

```env
MAX_WORKERS=8

FETCH_TIMEOUT=15
PING_TIMEOUT=8
PING_RETRIES=1

LATENCY_THRESHOLD_MS=5000

TCP_FILTER_LIMIT=2000
TCP_FILTER_WORKERS=100
TCP_FILTER_TIMEOUT=2.0

GEOIP_ENABLED=true
GEOIP_CACHE_TTL_SECONDS=86400
```

---

# 📡 Adding Sources

Source definitions are located at:

```text
src/config/sources.py
```

## Raw Sources

```python
RAW_SOURCES = [
    "https://example.com/source.txt",
]
```

The collector can process plain-text configuration sources and Base64 subscription content.

## Telegram Channels

```python
TELEGRAM_CHANNELS = [
    "example_channel",
]
```

Use the channel username without `@`.

Public Telegram channel previews are accessed through:

```text
https://t.me/s/<channel>
```

---

# 🧹 Deduplication

Configurations collected from different sources are automatically deduplicated.

The collector creates a stable identity based on important connection parameters rather than display remarks.

This prevents the same configuration from appearing repeatedly when it exists in multiple sources.

---

# 🚀 Installation

## Requirements

* Python 3.12+
* Xray-core
* Internet connection

Clone:

```bash
git clone https://github.com/Idolvpn/Automate-V2ray-Config-Collector.git

cd Automate-V2ray-Config-Collector
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶️ Run

Start the collector:

```bash
python -m src.main
```

Generated files will be stored in:

```text
configs/
```

---

# 🧪 Testing

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

Run tests:

```bash
pytest
```

The project includes tests for:

```text
tests/
├── test_dedup.py
├── test_exporter.py
├── test_fetcher.py
├── test_parser.py
└── test_tester.py
```

---

# 📢 Telegram Notifications

Telegram notifications are optional.

Configure:

```env
TELEGRAM_TOKEN=YOUR_BOT_TOKEN
TELEGRAM_CHAT_ID=YOUR_CHAT_ID
```

For GitHub Actions, store these values as GitHub Secrets:

```text
Repository
 → Settings
 → Secrets and variables
 → Actions
```

### 🔐 Never commit your Telegram Bot Token.

---

# 🗂️ Project Structure

```text
Automate-V2ray-Config-Collector/
│
├── .github/
│   └── workflows/
│       ├── collector.yml
│       └── tests.yml
│
├── configs/
│   ├── country_*.txt
│   ├── network_*.txt
│   ├── vmess.txt
│   ├── vless.txt
│   ├── trojan.txt
│   ├── ss.txt
│   ├── reality.txt
│   ├── mix.txt
│   ├── mix_sub.txt
│   ├── lite_mix.txt
│   ├── lite_mix_sub.txt
│   └── stats.json
│
├── src/
│   ├── config/
│   │   ├── settings.py
│   │   └── sources.py
│   │
│   ├── core/
│   │   ├── collector.py
│   │   ├── dedup.py
│   │   ├── exporter.py
│   │   ├── fetcher.py
│   │   ├── geoip.py
│   │   ├── notifier.py
│   │   ├── parser.py
│   │   ├── tester.py
│   │   └── xray_builder.py
│   │
│   ├── models/
│   │   ├── config.py
│   │   └── protocol.py
│   │
│   ├── utils/
│   │   ├── encoding.py
│   │   └── logger.py
│   │
│   └── main.py
│
├── tests/
│   ├── test_dedup.py
│   ├── test_exporter.py
│   ├── test_fetcher.py
│   ├── test_parser.py
│   └── test_tester.py
│
├── assets/
│   └── logo.jpg
│
├── _.env.example
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── LICENSE
└── README.md
```

---

# 🛠️ Core Components

| File              | Responsibility                      |
| ----------------- | ----------------------------------- |
| `collector.py`    | Main collection pipeline            |
| `fetcher.py`      | Download and process sources        |
| `parser.py`       | Parse configuration URLs            |
| `dedup.py`        | Remove duplicates                   |
| `tester.py`       | Connectivity and health testing     |
| `xray_builder.py` | Build temporary Xray configurations |
| `geoip.py`        | IP geolocation                      |
| `exporter.py`     | Generate output files               |
| `notifier.py`     | Telegram notifications              |

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a branch

```bash
git checkout -b feature/my-improvement
```

3. Make your changes
4. Run tests

```bash
pytest
```

5. Commit

```bash
git commit -m "feat: improve collector"
```

6. Push

```bash
git push origin feature/my-improvement
```

7. Open a Pull Request

---

# ⚠️ Disclaimer

This project is provided for:

* Educational purposes
* Networking research
* Software development
* Automation
* Testing

The collector processes configuration data obtained from publicly accessible sources.

Users are responsible for ensuring that their use of this software and collected configurations complies with applicable laws, network policies, service terms and licensing requirements.

The maintainers do not guarantee the:

* Availability
* Security
* Privacy
* Performance
* Reliability
* Legality

of collected configurations.

**Use responsibly and at your own risk.**

---

# 📄 License

This project is licensed under the **MIT License**.

See [LICENSE](LICENSE) for the complete license text.

---

# ⭐ Support the Project

If this project is useful to you:

⭐ **Star the repository**

🍴 **Fork the project**

🐛 **Report bugs**

🤝 **Contribute**

🔗 **Share the project**

---

<br>

# 🇮🇷 نسخه فارسی

## 📖 معرفی

**Automate V2Ray Config Collector** یک سیستم خودکار برای جمع‌آوری، پردازش، تست، دسته‌بندی و انتشار کانفیگ‌های V2Ray/Xray است.

این پروژه صرفاً یک Scraper ساده نیست و کانفیگ‌های جمع‌آوری‌شده را قبل از انتشار در چند مرحله بررسی می‌کند.

```text
منابع عمومی
     ↓
دریافت کانفیگ
     ↓
Parse
     ↓
حذف تکراری‌ها
     ↓
TCP Filter
     ↓
تست واقعی Xray
     ↓
بررسی Latency
     ↓
GeoIP
     ↓
دسته‌بندی
     ↓
ساخت خروجی
     ↓
انتشار در GitHub
```

---

# 🔥 لینک Subscription

### 🌐 اشتراک اصلی

```text
https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/mix_sub.txt
```

### 🪶 اشتراک Lite

```text
https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/lite_mix_sub.txt
```

### 📋 خروجی خام ترکیبی

```text
https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/mix.txt
```

این لینک‌ها را می‌توانید در Clientهایی که از Subscription پشتیبانی می‌کنند استفاده کنید.

---

# 📡 لینک پروتکل‌ها

| پروتکل         | لینک                                                                                                           |
| -------------- | -------------------------------------------------------------------------------------------------------------- |
| 🟢 VLESS       | [مشاهده](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/vless.txt)     |
| 🔵 VMess       | [مشاهده](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/vmess.txt)     |
| 🟠 Trojan      | [مشاهده](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/trojan.txt)    |
| 🟣 Shadowsocks | [مشاهده](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/ss.txt)        |
| 🔷 Reality     | [مشاهده](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/reality.txt)   |
| 🟡 WireGuard   | [مشاهده](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/wireguard.txt) |

---

# 🌍 لینک کشورهای منتخب

### 🇩🇪 آلمان

```text
https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/country_DE.txt
```

### 🇺🇸 آمریکا

```text
https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/country_US.txt
```

### 🇳🇱 هلند

```text
https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/country_NL.txt
```

### 🇹🇷 ترکیه

```text
https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/country_TR.txt
```

### 🇮🇷 ایران

```text
https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/country_IR.txt
```

> فایل‌های کشورهای دیگر نیز در صورت وجود کانفیگ سالم برای آن کشور به‌صورت خودکار ایجاد می‌شوند.

---

# ✨ امکانات

* 🔄 جمع‌آوری خودکار
* 📡 دریافت از منابع مختلف
* 📱 پشتیبانی از کانال‌های عمومی Telegram
* 🧩 تشخیص Protocol
* 🧹 حذف کانفیگ‌های تکراری
* ⚡ TCP Filter سریع
* 🧪 تست واقعی با Xray-core
* 📊 اندازه‌گیری Latency
* 🌍 تشخیص کشور سرور
* 📁 دسته‌بندی بر اساس کشور
* 🌐 دسته‌بندی بر اساس Network
* 🔗 ساخت Subscription به‌صورت Base64
* 🤖 اجرای خودکار با GitHub Actions
* 📢 ارسال گزارش Telegram
* 📈 تولید Statistics
* 🪶 تولید خروجی Lite

---

# ⚡ سیستم تست دو مرحله‌ای

## مرحله اول — TCP Filter

ابتدا Endpoint کانفیگ از طریق TCP بررسی می‌شود.

کانفیگ‌هایی که قابل دسترسی نیستند در همین مرحله حذف می‌شوند.

## مرحله دوم — Xray Health Check

کانفیگ‌های باقی‌مانده توسط Xray-core تست می‌شوند.

یک Xray موقت اجرا شده و از طریق SOCKS5 یک درخواست واقعی ارسال می‌شود.

در نتیجه فقط باز بودن Port ملاک سالم بودن کانفیگ نیست.

---

# 🤖 اجرای خودکار

Collector توسط GitHub Actions اجرا می‌شود.

Workflow اصلی:

```text
.github/workflows/collector.yml
```

به‌صورت پیش‌فرض هر **۲ ساعت** اجرا می‌شود.

همچنین می‌توان آن را به‌صورت دستی اجرا کرد:

```text
GitHub
 → Actions
 → Collect V2Ray Configs
 → Run workflow
```

پس برای اجرای Collector در حالت اتوماتیک، نیازی به سرور اختصاصی ندارید.

---

# 📂 خروجی‌ها

تمام خروجی‌ها داخل:

```text
configs/
```

ذخیره می‌شوند.

از جمله:

```text
vmess.txt
vless.txt
trojan.txt
ss.txt
reality.txt
wireguard.txt

mix.txt
mix_sub.txt

lite_mix.txt
lite_mix_sub.txt

country_*.txt
network_*.txt

stats.json
```

---

# ⚙️ تنظیمات

تنظیمات پروژه در:

```text
_.env.example
```

قرار دارد.

از جمله:

```env
MAX_WORKERS=8
FETCH_TIMEOUT=15
PING_TIMEOUT=8
PING_RETRIES=1

LATENCY_THRESHOLD_MS=5000

TCP_FILTER_LIMIT=2000
TCP_FILTER_WORKERS=100
TCP_FILTER_TIMEOUT=2.0

GEOIP_ENABLED=true
```

---

# 🚀 نصب

نیازمندی‌ها:

* Python 3.12+
* Xray-core
* اتصال اینترنت

دریافت پروژه:

```bash
git clone https://github.com/Idolvpn/Automate-V2ray-Config-Collector.git
cd Automate-V2ray-Config-Collector
```

نصب Dependencies:

```bash
pip install -r requirements.txt
```

اجرای Collector:

```bash
python -m src.main
```

---

# 🧪 تست

برای نصب وابستگی‌های توسعه:

```bash
pip install -r requirements-dev.txt
```

اجرای تست‌ها:

```bash
pytest
```

---

# 🔐 امنیت

اطلاعات حساس مانند:

```text
TELEGRAM_TOKEN
API Keys
Private Credentials
```

نباید در Repository قرار بگیرند.

برای GitHub Actions از GitHub Secrets استفاده کنید:

```text
Settings
 → Secrets and variables
 → Actions
```

---

# ⚠️ سلب مسئولیت

این پروژه با اهداف آموزشی، تحقیقاتی، توسعه نرم‌افزار، اتوماسیون و تست شبکه ارائه شده است.

مسئولیت نحوه استفاده از نرم‌افزار و کانفیگ‌های جمع‌آوری‌شده بر عهده کاربر است.

کاربر موظف است قوانین کشور خود، قوانین شبکه، شرایط سرویس‌ها و حقوق صاحبان منابع را رعایت کند.

توسعه‌دهندگان هیچ تضمینی در خصوص سرعت، پایداری، امنیت، حریم خصوصی یا قانونی بودن کانفیگ‌های جمع‌آوری‌شده ارائه نمی‌کنند.

**مسئولانه استفاده کنید.**

---

# 📄 مجوز

این پروژه تحت مجوز **MIT License** منتشر شده است.

برای اطلاعات کامل:

[مشاهده LICENSE](LICENSE)

---

<div align="center">

# ⭐ اگر پروژه برای شما مفید بود، یک Star بدهید!

### IdolVPN

**Freedom • Privacy • Limitless**

[GitHub Repository](https://github.com/Idolvpn/Automate-V2ray-Config-Collector)

<br>

Made with ❤️ for Open Source & Network Automation

</div>
```
` و فایل‌های پروتکل هم خروجی‌های واقعی Exporter هستند. همچنین Workflow واقعی پروژه طبق کد موجود، **هر ۲ ساعت** اجرا می‌شود و در اجرای GitHub Actions محدودیت Latency آن `1500ms` است.
