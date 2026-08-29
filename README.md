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

🇬🇧 English &nbsp; • &nbsp; 🇮🇷 [فارسی](#-نسخه-فارسی)

<br>

⭐ **If this project is useful to you, please give it a Star!**

</div>

---

# 🚀 Live Subscriptions

> Automatically generated and continuously updated configuration outputs.

## 🌐 Main Subscriptions

| Type | Link |
|---|---|
| 🔥 **MIX Subscription** | [Open](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/mix_sub.txt) |
| 🪶 **Lite MIX Subscription** | [Open](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/lite_mix_sub.txt) |
| 📋 **MIX Raw Configs** | [Open](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/mix.txt) |

### 📌 Copy Subscription URL

**MIX**
```text
https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/mix_sub.txt
```

**Lite MIX**
```text
https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/lite_mix_sub.txt
```

> 💡 The `mix_sub.txt` and `lite_mix_sub.txt` files are Base64 subscription outputs for compatible clients.

---

# 📡 Protocol Outputs

| Protocol | Output |
|---|---|
| 🟢 **VLESS** | [vless.txt](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/vless.txt) |
| 🔵 **VMess** | [vmess.txt](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/vmess.txt) |
| 🟠 **Trojan** | [trojan.txt](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/trojan.txt) |
| 🟣 **Shadowsocks** | [ss.txt](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/ss.txt) |
| 🔷 **Reality** | [reality.txt](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/reality.txt) |


---

# 🌍 Country Outputs

Country-specific configuration files are generated automatically according to detected server locations.

| Country | Output |
|---|---|
| 🇩🇪 **Germany** | [country_DE.txt](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/country_DE.txt) |
| 🇺🇸 **United States** | [country_US.txt](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/country_US.txt) |
| 🇳🇱 **Netherlands** | [country_NL.txt](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/country_NL.txt) |
| 🇹🇷 **Turkey** | [country_TR.txt](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/country_TR.txt) |
| 🇮🇷 **Iran** | [country_IR.txt](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/country_IR.txt) |

> Additional country files may appear automatically depending on collected configurations.

---

# 📖 About

**Automate V2Ray Config Collector** is an automated Python-based pipeline for collecting, processing, validating, categorizing, and publishing V2Ray/Xray configurations from multiple public sources.

Unlike a basic configuration scraper, the project performs multiple filtering and validation stages before publishing configurations.

## 🔄 Pipeline

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

- 🔄 Automatic configuration collection
- 📡 Multiple public sources
- 📱 Public Telegram channel support
- 🧩 V2Ray/Xray protocol parsing
- 🧹 Automatic deduplication
- ⚡ Fast TCP connectivity filtering
- 🧪 Real Xray-core validation
- 📊 Latency measurement
- 🌍 GeoIP detection
- 📁 Country-based outputs
- 🌐 Network-based outputs
- 🔗 Base64 subscription generation
- 🤖 Automated GitHub Actions workflow
- 📢 Optional Telegram notifications
- 📈 JSON statistics
- 🪶 Lite configuration outputs

---

# 🧩 Supported Protocols

The collector currently recognizes:

- VMess
- VLESS
- Trojan
- Shadowsocks
- VLESS Reality

Reality configurations are detected separately when the configuration contains:

```text
security=reality
```

---

# ⚡ Two-Stage Health Checking

One of the key features of this project is its two-stage configuration validation system.

## 1️⃣ TCP Fast Filter

Before starting Xray, collected configurations are checked using a lightweight TCP connectivity test.

```text
Collected Configurations
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

Unreachable endpoints are removed before entering the more expensive Xray testing stage.

The TCP filter supports concurrent testing and can limit the number of candidates passed to Xray.

## 2️⃣ Real Xray Validation

An open TCP port does not necessarily mean that a proxy configuration actually works.

A configuration can fail because of:

- Invalid credentials
- TLS errors
- Incorrect Reality parameters
- Invalid transport settings
- Server-side failures
- Upstream connectivity problems

For this reason, candidates are tested through **Xray-core**.

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
  ┌───┴────┐
  ▼        ▼
 FAIL    HEALTHY
```

Only configurations that pass the configured health-check criteria are exported.

---

# 🌍 GeoIP

Healthy configurations can be enriched with approximate geographic information.

The collector uses **ip-api.com** batch requests to resolve server IP locations.

The detected country can then be used to generate country-specific configuration files.

Examples:

```text
🇩🇪 Germany
🇺🇸 United States
🇳🇱 Netherlands
🇫🇷 France
🇹🇷 Turkey
🇮🇷 Iran
```

GeoIP requests use batching and caching to reduce unnecessary API requests.

GeoIP can also be disabled through configuration.

---

# 📂 Output Structure

Generated files are stored inside:

```text
configs/
```

## Protocol Outputs

```text
configs/
├── vmess.txt
├── vless.txt
├── trojan.txt
├── ss.txt
└── reality.txt
```

## Country Outputs

```text
configs/
├── country_IR.txt
├── country_DE.txt
├── country_US.txt
├── country_NL.txt
├── country_TR.txt
└── ...
```

## Network Outputs

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

## Combined Outputs

```text
configs/
├── mix.txt
├── mix_sub.txt
├── lite_mix.txt
└── lite_mix_sub.txt
```

---

# 📊 Statistics

The collector generates:

```text
configs/stats.json
```

Statistics include:

- Total healthy configurations
- Protocol distribution
- Country distribution
- Average latency

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

The main workflow is:

```text
.github/workflows/collector.yml
```

## Workflow

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

The collector runs automatically every **2 hours** and can also be triggered manually.

### Manual Run

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

| Variable | Description |
|---|---|
| `MAX_WORKERS` | Number of concurrent workers |
| `FETCH_TIMEOUT` | Source fetching timeout |
| `PING_TIMEOUT` | Xray test timeout |
| `PING_RETRIES` | Number of retries |
| `LATENCY_THRESHOLD_MS` | Maximum accepted latency |
| `TCP_FILTER_LIMIT` | Maximum candidates passed to Xray |
| `TCP_FILTER_WORKERS` | TCP test concurrency |
| `TCP_FILTER_TIMEOUT` | TCP connection timeout |
| `GEOIP_ENABLED` | Enable or disable GeoIP |
| `GEOIP_CACHE_TTL_SECONDS` | GeoIP cache lifetime |
| `OUTPUT_DIR` | Output directory |
| `LOG_LEVEL` | Logging level |
| `MAX_CONFIGS_PER_OUTPUT` | Lite output limit |
| `XRAY_PATH` | Xray binary path |
| `TEST_URL` | URL used for health testing |
| `XRAY_STARTUP_DELAY` | Xray startup delay |

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

Source definitions are located in:

```text
src/config/sources.py
```

## Raw Sources

Add raw configuration sources using:

```python
RAW_SOURCES = [
    "https://example.com/source.txt",
]
```

The collector can process plain-text configuration lists and Base64 subscription content.

## Telegram Channels

Public Telegram channels can be configured using:

```python
TELEGRAM_CHANNELS = [
    "example_channel",
]
```

Use the Telegram channel username **without `@`**.

Public channel previews are accessed through:

```text
https://t.me/s/<channel>
```

---

# 🧹 Deduplication

Configurations collected from different sources are automatically deduplicated.

The collector creates a stable identity using important connection parameters rather than display names or remarks.

This prevents the same configuration from appearing multiple times when it exists across several sources.

---

# 🚀 Installation

## Requirements

- Python 3.12+
- Xray-core
- Internet connection

## Clone the Repository

```bash
git clone https://github.com/Idolvpn/Automate-V2ray-Config-Collector.git
cd Automate-V2ray-Config-Collector
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run

Start the collector with:

```bash
python -m src.main
```

Generated outputs will be stored in:

```text
configs/
```

---

# 🧪 Testing

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

Run the test suite:

```bash
pytest
```

Tests are located in:

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

### 🔐 Never commit your Telegram Bot Token to the repository.

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
├── assets/
│   └── logo.jpg
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
├── _.env.example
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── LICENSE
└── README.md
```

---

# 🛠️ Core Components

| File | Responsibility |
|---|---|
| `collector.py` | Main collection pipeline |
| `fetcher.py` | Download and process sources |
| `parser.py` | Parse configuration URLs |
| `dedup.py` | Remove duplicate configurations |
| `tester.py` | Connectivity and health testing |
| `xray_builder.py` | Build temporary Xray configurations |
| `geoip.py` | IP geolocation |
| `exporter.py` | Generate output files |
| `notifier.py` | Telegram notifications |

---

# 🤝 Contributing

Contributions, improvements and bug reports are welcome.

### 1. Fork the repository

### 2. Create a branch

```bash
git checkout -b feature/my-improvement
```

### 3. Make your changes

### 4. Run tests

```bash
pytest
```

### 5. Commit

```bash
git commit -m "feat: improve collector"
```

### 6. Push

```bash
git push origin feature/my-improvement
```

### 7. Open a Pull Request

---

# ⚠️ Disclaimer

This project is provided for:

- Educational purposes
- Networking research
- Software development
- Automation
- Testing

The collector processes configuration data obtained from publicly accessible sources.

Users are responsible for ensuring that their use of this software and collected configurations complies with applicable laws, network policies, service terms and licensing requirements.

The maintainers do not guarantee the:

- Availability
- Security
- Privacy
- Performance
- Reliability
- Legality

of collected configurations.

**Use responsibly and at your own risk.**

---

# 📄 License

This project is licensed under the **MIT License**.

See [LICENSE](LICENSE) for the complete license text.

---

# ⭐ Support the Project

If you find this project useful:

⭐ **Star the repository**

🍴 **Fork the project**

🐛 **Report bugs**

🤝 **Contribute improvements**

🔗 **Share the project**

---

# 🇮🇷 نسخه فارسی

## 📖 معرفی

**Automate V2Ray Config Collector** یک سیستم خودکار مبتنی بر Python برای جمع‌آوری، پردازش، تست، دسته‌بندی و انتشار کانفیگ‌های V2Ray/Xray از منابع عمومی مختلف است.

این پروژه صرفاً یک Scraper ساده نیست و کانفیگ‌ها قبل از انتشار از چند مرحله فیلترینگ و بررسی عبور می‌کنند.

---

# 🔥 لینک‌های Subscription

## 🌐 اشتراک اصلی

```text
https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/mix_sub.txt
```

## 🪶 اشتراک Lite

```text
https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/lite_mix_sub.txt
```

## 📋 خروجی ترکیبی خام

```text
https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/mix.txt
```

> لینک‌های بالا را می‌توانید مستقیماً در Clientهایی که از Subscription پشتیبانی می‌کنند وارد کنید.

---

# 📡 خروجی پروتکل‌ها

| پروتکل | لینک |
|---|---|
| 🟢 VLESS | [مشاهده](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/vless.txt) |
| 🔵 VMess | [مشاهده](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/vmess.txt) |
| 🟠 Trojan | [مشاهده](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/trojan.txt) |
| 🟣 Shadowsocks | [مشاهده](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/ss.txt) |
| 🔷 Reality | [مشاهده](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/reality.txt) |

---

# 🌍 خروجی کشورهای منتخب

| کشور | لینک |
|---|---|
| 🇩🇪 آلمان | [country_DE.txt](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/country_DE.txt) |
| 🇺🇸 آمریکا | [country_US.txt](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/country_US.txt) |
| 🇳🇱 هلند | [country_NL.txt](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/country_NL.txt) |
| 🇹🇷 ترکیه | [country_TR.txt](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/country_TR.txt) |
| 🇮🇷 ایران | [country_IR.txt](https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/country_IR.txt) |

> کشورهای دیگر نیز در صورت وجود کانفیگ سالم به‌صورت خودکار به خروجی‌ها اضافه می‌شوند.

---

# ✨ امکانات

- 🔄 جمع‌آوری خودکار کانفیگ‌ها
- 📡 پشتیبانی از منابع مختلف
- 📱 پشتیبانی از کانال‌های عمومی Telegram
- 🧩 تشخیص Protocol
- 🧹 حذف کانفیگ‌های تکراری
- ⚡ فیلتر سریع TCP
- 🧪 تست واقعی با Xray-core
- 📊 اندازه‌گیری Latency
- 🌍 تشخیص کشور سرور
- 📁 دسته‌بندی بر اساس کشور
- 🌐 دسته‌بندی بر اساس Network
- 🔗 ساخت Subscription به‌صورت Base64
- 🤖 اجرای خودکار با GitHub Actions
- 📢 ارسال گزارش Telegram
- 📈 تولید Statistics
- 🪶 تولید خروجی Lite

---

# ⚡ سیستم تست دو مرحله‌ای

## 1️⃣ فیلتر TCP

ابتدا Endpoint کانفیگ از طریق TCP بررسی می‌شود.

کانفیگ‌هایی که قابل دسترسی نیستند در همین مرحله حذف می‌شوند.

## 2️⃣ تست واقعی Xray

کانفیگ‌های باقی‌مانده توسط Xray-core تست می‌شوند.

یک Xray موقت اجرا شده و از طریق SOCKS5 یک درخواست واقعی ارسال می‌شود.

بنابراین فقط باز بودن Port به‌عنوان سالم بودن کانفیگ در نظر گرفته نمی‌شود.

---

# 🌍 GeoIP

کانفیگ‌های سالم می‌توانند با اطلاعات تقریبی موقعیت سرور تکمیل شوند.

اطلاعات کشور برای ساخت خروجی‌های جداگانه کشورها استفاده می‌شود.

---

# 🤖 اجرای خودکار

Collector از GitHub Actions استفاده می‌کند.

Workflow اصلی:

```text
.github/workflows/collector.yml
```

به‌صورت پیش‌فرض هر **۲ ساعت** اجرا می‌شود و امکان اجرای دستی نیز وجود دارد.

```text
GitHub
 → Actions
 → Collect V2Ray Configs
 → Run workflow
```

---

# 📂 خروجی‌ها

خروجی‌ها در پوشه زیر قرار می‌گیرند:

```text
configs/
```

شامل:

```text
vmess.txt
vless.txt
trojan.txt
ss.txt
reality.txt

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

تنظیمات پروژه در فایل زیر قرار دارند:

```text
_.env.example
```

نمونه:

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

# 🚀 نصب

نیازمندی‌ها:

- Python 3.12+
- Xray-core
- اتصال اینترنت

دریافت پروژه:

```bash
git clone https://github.com/Idolvpn/Automate-V2ray-Config-Collector.git
cd Automate-V2ray-Config-Collector
```

نصب وابستگی‌ها:

```bash
pip install -r requirements.txt
```

اجرای Collector:

```bash
python -m src.main
```

---

# 🧪 تست

نصب وابستگی‌های توسعه:

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

نباید داخل Repository قرار بگیرند.

برای GitHub Actions از:

```text
Settings
 → Secrets and variables
 → Actions
```

استفاده کنید.

### 🔒 هیچ‌وقت Telegram Bot Token را داخل GitHub Commit نکنید.

---

# 🤝 مشارکت

Pull Request، گزارش باگ و پیشنهادهای بهبود پروژه استقبال می‌شود.

---

# ⚠️ سلب مسئولیت

این پروژه با اهداف آموزشی، تحقیقاتی، توسعه نرم‌افزار، اتوماسیون و تست شبکه ارائه شده است.

مسئولیت نحوه استفاده از نرم‌افزار و کانفیگ‌های جمع‌آوری‌شده بر عهده کاربر است.

کاربر موظف است قوانین کشور خود، قوانین شبکه، شرایط سرویس‌ها و حقوق صاحبان منابع را رعایت کند.

توسعه‌دهندگان هیچ تضمینی در خصوص سرعت، پایداری، امنیت، حریم خصوصی، قابلیت دسترسی یا قانونی بودن کانفیگ‌های جمع‌آوری‌شده ارائه نمی‌کنند.

**مسئولانه استفاده کنید.**

---

# 📄 مجوز

این پروژه تحت مجوز **MIT License** منتشر شده است.

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
