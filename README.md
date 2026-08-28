<div align="center">

# ⚡ Automate V2Ray Config Collector

### 🚀 Automated V2Ray / Xray Configuration Collector, Validator & Publisher

**Collect • Parse • Deduplicate • TCP Filter • Xray Test • GeoIP • Export • Automate**

<br>

[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge\&logo=python\&logoColor=white)](https://www.python.org/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-2088FF?style=for-the-badge\&logo=github-actions\&logoColor=white)](https://github.com/features/actions)
[![Xray](https://img.shields.io/badge/Xray-Core-00ADD8?style=for-the-badge)](https://github.com/XTLS/Xray-core)
[![License](https://img.shields.io/badge/License-MIT-2ea44f?style=for-the-badge)](LICENSE)

<br>

**English** · [🇮🇷 فارسی](#-نسخه-فارسی)

<br>

⭐ **If this project is useful to you, consider giving it a Star!**

</div>

---

## 📖 About

**Automate V2Ray Config Collector** is an automated Python-based pipeline designed to collect, process, validate, categorize, and publish V2Ray/Xray proxy configurations from multiple public sources.

Instead of simply collecting configuration links, the project goes further by validating configurations through a **two-stage testing system**:

```text
Public Sources
      │
      ▼
┌───────────────┐
│ Fetch Sources │
└───────┬───────┘
        ▼
┌───────────────┐
│ Parse Configs │
└───────┬───────┘
        ▼
┌───────────────┐
│ Deduplicate   │
└───────┬───────┘
        ▼
┌───────────────┐
│ TCP Fast Test │
└───────┬───────┘
        ▼
┌───────────────┐
│ Xray Real Test│
└───────┬───────┘
        ▼
┌───────────────┐
│ GeoIP Lookup  │
└───────┬───────┘
        ▼
┌───────────────┐
│ Export Output │
└───────┬───────┘
        ▼
    GitHub Repo
```

The whole workflow can run automatically through **GitHub Actions**, eliminating the need for a dedicated server for the default workflow.

---

# ✨ Features

| Feature                       | Description                                                 |
| ----------------------------- | ----------------------------------------------------------- |
| 🔄 **Automatic Collection**   | Collect configurations from multiple public sources         |
| 📡 **Multiple Sources**       | Raw URLs, subscription sources and public Telegram channels |
| 🧩 **Protocol Parsing**       | Parse supported V2Ray/Xray configuration formats            |
| 🧹 **Deduplication**          | Remove duplicate configurations automatically               |
| ⚡ **TCP Fast Filter**         | Quickly eliminate unreachable endpoints                     |
| 🧪 **Xray Validation**        | Perform real proxy connectivity tests using Xray-core       |
| 📊 **Latency Measurement**    | Measure and filter configurations by response time          |
| 🌍 **GeoIP**                  | Detect approximate server country/location                  |
| 📁 **Categorized Output**     | Export configurations by protocol, country and network      |
| 🔗 **Base64 Subscriptions**   | Generate subscription-ready Base64 output                   |
| 🤖 **GitHub Actions**         | Fully automated scheduled collection                        |
| 📢 **Telegram Notifications** | Optional run summary notifications                          |
| 📈 **Statistics**             | Generate JSON statistics for collected results              |
| 🪶 **Lite Outputs**           | Generate smaller configuration lists when required          |

---

# 🧩 Supported Protocols

The collector currently recognizes:

* `VMess`
* `VLESS`
* `Trojan`
* `Shadowsocks`
* `WireGuard`
* `VLESS Reality`

Reality configurations are detected separately when:

```text
security=reality
```

is present in the configuration.

---

# ⚡ Smart Health Checking

One of the main differences between this project and a basic configuration scraper is its **two-stage validation system**.

## 1️⃣ TCP Fast Filter

First, configurations go through a lightweight TCP connectivity test.

```text
Collected Configurations
          │
          ▼
    TCP Connectivity
          │
          ├── ❌ Unreachable → Removed
          │
          └── ✅ Reachable
                  │
                  ▼
             Xray Testing
```

This prevents wasting resources on configurations whose endpoints are not even reachable.

The TCP filter supports concurrent testing and can keep only the fastest candidates for the next stage.

---

## 2️⃣ Real Xray Validation

TCP connectivity alone does **not** prove that a proxy configuration actually works.

A configuration may have:

* An open port
* A reachable IP
* A valid TCP connection

while still failing because of:

* TLS problems
* Incorrect credentials
* Invalid Reality parameters
* Incorrect transport settings
* Proxy-side failures
* Upstream connectivity problems

Therefore, candidates are tested through **Xray-core**.

The collector creates a temporary Xray configuration, starts an Xray instance, exposes a local SOCKS5 proxy and performs a real HTTP request through it.

```text
Config
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
  ├── ❌ Failed
  │
  └── ✅ Healthy
```

This provides a much more meaningful health check than a simple port scanner.

---

# 🌍 GeoIP

Healthy configurations can be enriched with approximate geographic information.

The project uses **ip-api.com batch requests** to resolve server IP locations.

Results can be used to categorize configurations by country.

Example:

```text
🇩🇪 Germany
🇺🇸 United States
🇳🇱 Netherlands
🇫🇷 France
🇹🇷 Turkey
🇮🇷 Iran
```

GeoIP lookups use batching and caching to reduce unnecessary API requests.

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
├── reality.txt
└── wireguard.txt
```

## Country Outputs

Examples:

```text
configs/
├── country_US.txt
├── country_DE.txt
├── country_NL.txt
├── country_FR.txt
├── country_TR.txt
└── country_IR.txt
```

Country files are generated dynamically based on the detected server locations.

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

### `mix.txt`

Contains the combined healthy configurations.

### `mix_sub.txt`

Contains the combined configurations encoded as Base64 and can be used as a subscription source in compatible clients.

### `lite_mix.txt`

A smaller version of the combined output when `MAX_CONFIGS_PER_OUTPUT` is enabled.

### `lite_mix_sub.txt`

Base64 subscription version of the Lite output.

---

# 📊 Statistics

The collector generates:

```text
configs/stats.json
```

The statistics file can contain information such as:

* Total healthy configurations
* Protocol distribution
* Country distribution
* Average latency

Example structure:

```json
{
  "total": 1234,
  "protocols": {},
  "countries": {},
  "average_latency_ms": 0
}
```

---

# 🔄 Automated GitHub Workflow

The project is designed to work seamlessly with **GitHub Actions**.

The collector can automatically:

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

The repository includes:

```text
.github/workflows/collector.yml
```

for the collector workflow.

A separate workflow is also provided for tests:

```text
.github/workflows/tests.yml
```

The collector can also be manually triggered from:

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
| `PING_RETRIES`            | Number of test retries            |
| `LATENCY_THRESHOLD_MS`    | Maximum accepted latency          |
| `TCP_FILTER_LIMIT`        | Maximum candidates passed to Xray |
| `TCP_FILTER_WORKERS`      | TCP test concurrency              |
| `TCP_FILTER_TIMEOUT`      | TCP connection timeout            |
| `GEOIP_ENABLED`           | Enable/disable GeoIP              |
| `GEOIP_CACHE_TTL_SECONDS` | GeoIP cache lifetime              |
| `OUTPUT_DIR`              | Output directory                  |
| `LOG_LEVEL`               | Logging level                     |
| `MAX_CONFIGS_PER_OUTPUT`  | Limit Lite output size            |
| `XRAY_PATH`               | Xray binary path                  |
| `TEST_URL`                | URL used for health checking      |
| `XRAY_STARTUP_DELAY`      | Xray startup delay                |

Example:

```env
TCP_FILTER_LIMIT=2000
TCP_FILTER_WORKERS=100
TCP_FILTER_TIMEOUT=2.0

MAX_WORKERS=8
PING_TIMEOUT=8
LATENCY_THRESHOLD_MS=5000

GEOIP_ENABLED=true
```

---

# 📡 Adding Sources

Source definitions are located in:

```text
src/config/sources.py
```

## Raw Sources

Add subscription or raw configuration sources to:

```python
RAW_SOURCES = [
    "https://example.com/source.txt",
]
```

The fetcher can process plain-text configuration lists and Base64-encoded subscription content.

---

## Telegram Sources

Public Telegram channels can be configured using:

```python
TELEGRAM_CHANNELS = [
    "example_channel",
]
```

Use the channel username **without `@`**.

Public channel previews are accessed through:

```text
https://t.me/s/<channel>
```

No Telegram bot token is required for reading public channel previews.

---

# 🧹 Deduplication

The collector automatically removes duplicate configurations before testing.

Configuration identity is based on important connection parameters rather than display remarks.

This means that the same configuration appearing in several sources will not unnecessarily appear multiple times in the final output.

---

# 🚀 Installation

## Requirements

* Python `3.12+`
* Xray-core
* Internet connection

Clone the repository:

```bash
git clone https://github.com/Idolvpn/Automate-V2ray-Config-Collector.git
cd Automate-V2ray-Config-Collector
```

Install dependencies:

```bash
pip install -r requirements.txt
```

For development/testing:

```bash
pip install -r requirements-dev.txt
```

---

# ▶️ Run

Start the collector with:

```bash
python -m src.main
```

Generated files will be available inside:

```text
configs/
```

---

# 🧪 Run Tests

Run the test suite with:

```bash
pytest
```

The repository includes tests for components such as:

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

The notification system can send a summary after a collector run.

For GitHub Actions, sensitive values should be stored in:

```text
Repository
→ Settings
→ Secrets and variables
→ Actions
```

### 🔐 Never commit your Telegram Bot Token to Git.

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
├── LICENSE
└── README.md
```

---

# 🛠️ Development

The project is structured into separate components so that collection, parsing, validation and exporting can be maintained independently.

### Core components

| Module            | Responsibility                      |
| ----------------- | ----------------------------------- |
| `collector.py`    | Main collection pipeline            |
| `fetcher.py`      | Download and source processing      |
| `parser.py`       | Parse configuration URLs            |
| `dedup.py`        | Remove duplicates                   |
| `tester.py`       | Connectivity and health testing     |
| `xray_builder.py` | Build temporary Xray configurations |
| `geoip.py`        | IP geolocation                      |
| `exporter.py`     | Generate output files               |
| `notifier.py`     | Telegram notifications              |

---

# 🤝 Contributing

Contributions, bug reports and improvements are welcome.

### 1. Fork

Fork the repository.

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

This project is provided for **educational, research, networking and development purposes**.

The collector processes configuration data obtained from publicly accessible sources.

Users are responsible for ensuring that their use of this software and any collected configurations complies with:

* Applicable laws
* Network policies
* Service terms
* Copyright/licensing requirements
* Policies of the original configuration providers

The maintainers do not guarantee the availability, security, privacy, performance or legality of collected configurations.

**Use responsibly and at your own risk.**

---

# 📄 License

This project is licensed under the:

**MIT License**

See [LICENSE](LICENSE) for the complete license text.

---

# ⭐ Support

If you find this project useful:

### ⭐ Star the repository

### 🍴 Fork it

### 🐛 Report issues

### 🤝 Contribute improvements

Repository:

**https://github.com/Idolvpn/Automate-V2ray-Config-Collector**

---

<br>

# 🇮🇷 نسخه فارسی

## 📖 معرفی

**Automate V2Ray Config Collector** یک سیستم خودکار مبتنی بر Python برای جمع‌آوری، پردازش، بررسی، دسته‌بندی و انتشار کانفیگ‌های V2Ray/Xray از منابع عمومی مختلف است.

این پروژه فقط یک **Config Scraper ساده** نیست؛ کانفیگ‌های جمع‌آوری‌شده را ابتدا فیلتر می‌کند و سپس با استفاده از **Xray-core** آن‌ها را به‌صورت واقعی آزمایش می‌کند.

روند کلی:

```text
منابع عمومی
     ↓
دریافت کانفیگ‌ها
     ↓
استخراج و Parse
     ↓
حذف Duplicate
     ↓
فیلتر سریع TCP
     ↓
تست واقعی با Xray
     ↓
اندازه‌گیری Latency
     ↓
تشخیص کشور با GeoIP
     ↓
دسته‌بندی
     ↓
ساخت Subscription
     ↓
انتشار در GitHub
```

---

## ✨ امکانات

* 🔄 جمع‌آوری خودکار کانفیگ‌ها
* 📡 پشتیبانی از چندین منبع
* 📱 دریافت از کانال‌های عمومی Telegram
* 🧩 تشخیص Protocol
* 🧹 حذف کانفیگ‌های تکراری
* ⚡ فیلتر سریع TCP
* 🧪 تست واقعی با Xray-core
* 📊 اندازه‌گیری Latency
* 🌍 تشخیص کشور سرور
* 📁 دسته‌بندی بر اساس کشور
* 🌐 دسته‌بندی بر اساس Network
* 🔗 ساخت Subscription به‌صورت Base64
* 📈 تولید آمار
* 🤖 اجرای خودکار با GitHub Actions
* 📢 ارسال گزارش به Telegram
* 🪶 تولید خروجی Lite

---

## 🧩 پروتکل‌های پشتیبانی‌شده

پروژه در حال حاضر این پروتکل‌ها را شناسایی می‌کند:

```text
VMess
VLESS
Trojan
Shadowsocks
WireGuard
VLESS Reality
```

---

## ⚡ سیستم تست دو مرحله‌ای

### مرحله اول — TCP Filter

ابتدا بررسی می‌شود که Endpoint کانفیگ از طریق TCP قابل دسترسی است یا خیر.

این مرحله سریع‌تر است و باعث می‌شود کانفیگ‌های کاملاً غیرقابل‌دسترسی قبل از اجرای Xray حذف شوند.

```text
کانفیگ‌ها
   ↓
TCP Test
   ├── ❌ Fail → حذف
   └── ✅ Pass
           ↓
       Xray Test
```

### مرحله دوم — تست واقعی Xray

کانفیگ‌های باقی‌مانده با Xray-core تست می‌شوند.

برای هر کانفیگ:

1. تنظیمات Xray ساخته می‌شود.
2. یک Instance موقت Xray اجرا می‌شود.
3. یک SOCKS5 Proxy محلی ایجاد می‌شود.
4. درخواست واقعی HTTP از Proxy ارسال می‌شود.
5. Latency اندازه‌گیری می‌شود.
6. نتیجه به‌عنوان سالم یا ناموفق ثبت می‌شود.

بنابراین صرفاً باز بودن Port به‌عنوان سالم بودن کانفیگ در نظر گرفته نمی‌شود.

---

## 📂 خروجی‌ها

تمام خروجی‌ها داخل پوشه زیر قرار می‌گیرند:

```text
configs/
```

### بر اساس Protocol

```text
vmess.txt
vless.txt
trojan.txt
ss.txt
reality.txt
wireguard.txt
```

### بر اساس کشور

برای مثال:

```text
country_IR.txt
country_DE.txt
country_US.txt
country_NL.txt
country_TR.txt
```

### بر اساس Network

```text
network_tcp.txt
network_ws.txt
network_grpc.txt
network_h2.txt
network_http.txt
network_httpupgrade.txt
network_xhttp.txt
network_raw.txt
```

### خروجی ترکیبی

```text
mix.txt
mix_sub.txt
```

`mix.txt` شامل کانفیگ‌های سالم ترکیبی است.

`mix_sub.txt` نسخه Base64 و مناسب استفاده به‌عنوان Subscription در Clientهای سازگار است.

---

## 🤖 اجرای خودکار

پروژه دارای GitHub Actions است.

Workflow می‌تواند به‌صورت خودکار:

```text
جمع‌آوری
   ↓
Parse
   ↓
Deduplicate
   ↓
TCP Filter
   ↓
Xray Test
   ↓
GeoIP
   ↓
Export
   ↓
Commit
```

را انجام دهد.

بنابراین برای اجرای دائمی پروژه، در حالت پیش‌فرض نیازی به خرید یا نگهداری یک سرور اختصاصی نیست.

---

## ⚙️ تنظیمات

تنظیمات محیطی در فایل زیر قرار دارند:

```text
_.env.example
```

از جمله:

```env
MAX_WORKERS=8
FETCH_TIMEOUT=15
PING_TIMEOUT=8
PING_RETRIES=1

TCP_FILTER_LIMIT=2000
TCP_FILTER_WORKERS=100
TCP_FILTER_TIMEOUT=2.0

LATENCY_THRESHOLD_MS=5000

GEOIP_ENABLED=true
GEOIP_CACHE_TTL_SECONDS=86400
```

---

## 📡 افزودن Source جدید

منابع در:

```text
src/config/sources.py
```

قرار دارند.

برای Sourceهای Raw:

```python
RAW_SOURCES = [
    "https://example.com/source.txt",
]
```

و برای کانال‌های عمومی Telegram:

```python
TELEGRAM_CHANNELS = [
    "example_channel",
]
```

نام کانال را بدون `@` وارد کنید.

---

## 📊 آمار

اطلاعات آماری در:

```text
configs/stats.json
```

ذخیره می‌شود.

این فایل می‌تواند شامل:

* تعداد کانفیگ‌های سالم
* تعداد بر اساس Protocol
* تعداد بر اساس Country
* میانگین Latency

باشد.

---

## 🚀 نصب

نیازمندی‌ها:

* Python 3.12+
* Xray-core
* Internet Connection

دریافت پروژه:

```bash
git clone https://github.com/Idolvpn/Automate-V2ray-Config-Collector.git
cd Automate-V2ray-Config-Collector
```

نصب Dependencies:

```bash
pip install -r requirements.txt
```

اجرای پروژه:

```bash
python -m src.main
```

---

## 🧪 اجرای تست‌ها

برای اجرای تست‌های پروژه:

```bash
pip install -r requirements-dev.txt
pytest
```

---

## 🔐 امنیت

اطلاعات حساس مانند:

```text
TELEGRAM_TOKEN
API Keys
Private Credentials
```

را داخل Repository قرار ندهید.

برای GitHub Actions از:

```text
Settings
→ Secrets and variables
→ Actions
```

استفاده کنید.

---

## ⚠️ سلب مسئولیت

این پروژه با هدف‌های آموزشی، تحقیقاتی، توسعه نرم‌افزار و آزمایش‌های شبکه ارائه شده است.

مسئولیت نحوه استفاده از نرم‌افزار و کانفیگ‌های جمع‌آوری‌شده کاملاً بر عهده کاربر است.

کاربر باید قوانین کشور خود، قوانین شبکه، شرایط سرویس‌ها و حقوق صاحبان منابع را رعایت کند.

توسعه‌دهندگان هیچ تضمینی در مورد:

* پایداری
* سرعت
* امنیت
* حریم خصوصی
* قانونی بودن
* یا در دسترس بودن

کانفیگ‌های جمع‌آوری‌شده ارائه نمی‌کنند.

**مسئولانه استفاده کنید.**

---

## 📄 License

این پروژه تحت مجوز:

**MIT License**

منتشر شده است.

برای اطلاعات کامل به فایل [LICENSE](LICENSE) مراجعه کنید.

---

<div align="center">

## ⭐ اگر پروژه برایت مفید بود، یک Star بده!

**Made with ❤️ for Open Source & Network Automation**

[⬆ Back to Top](#-automate-v2ray-config-collector)

</div>
