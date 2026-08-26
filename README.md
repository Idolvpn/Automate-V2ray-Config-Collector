# V2Ray Config Collector

[English](#english) | [فارسی](#فارسی)

---

## English

An automated collector that fetches free V2Ray / proxy configs from public
subscription sources and Telegram channels, health-checks them, tags them
by country, and publishes clean, deduplicated subscription files — updated
every 2 hours via GitHub Actions.

### 🔗 Subscription Links

Copy any of the links below directly into your V2Ray client (v2rayNG,
NekoBox, V2Box, etc.) as a subscription URL.

| Type | Link |
| --- | --- |
| **Mix (all protocols)** | `https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/mix.txt` |
| **Mix (Base64 subscription)** | `https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/mix_sub.txt` |
| **VLESS** | `https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/vless.txt` |
| **VMESS** | `https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/vmess.txt` |
| **Trojan** | `https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/trojan.txt` |
| **Shadowsocks** | `https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/ss.txt` |
| **Reality** | `https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/reality.txt` |
| **WireGuard** | `https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/wireguard.txt` |

#### How to import
1. Copy the link for the protocol (or `mix`) you want.
2. Open your V2Ray client.
3. Go to **Import config from URL** / **Add subscription**.
4. Paste the link and confirm.
5. Set an auto-update interval if your client supports it — the source
   updates every 2 hours.

### Features

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

### Project layout

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

### Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # optional — defaults work out of the box
python -m src.main
```

Output is written to `configs/` (protocol files, country files,
`mix.txt`, `mix_sub.txt`, and `stats.json`).

### Running tests

```bash
pip install -r requirements-dev.txt
pytest
```

### Deploying via GitHub Actions

The `Collect V2Ray Configs` workflow runs every 2 hours automatically and
commits updated files under `configs/` back to the repo. You can also
trigger it manually from the **Actions** tab → **Collect V2Ray Configs**
→ **Run workflow**.

(Optional) Add `TELEGRAM_TOKEN` / `TELEGRAM_CHAT_ID` repository secrets
under **Settings → Secrets and variables → Actions** if you want a
run-summary notification sent to Telegram.

### Configuration

All tunables live in environment variables — see `.env.example`:
concurrency, timeouts, latency threshold, how many Telegram messages to
scan per channel, and whether GeoIP tagging is enabled.

To add or remove sources, edit `src/config/sources.py`.

### Disclaimer

⚠️ Configs are collected automatically from public sources and are not
vetted for trustworthiness. Don't send sensitive traffic through configs
you don't control. This project is provided for research and censorship
circumvention purposes.

### License

MIT — see [LICENSE](LICENSE).

---

## فارسی

یک جمع‌آوری‌کننده‌ی خودکار کانفیگ‌های رایگان V2Ray / پروکسی که از منابع
عمومی سابسکریپشن و کانال‌های تلگرام جمع‌آوری می‌کنه، سلامت هر کانفیگ رو
تست می‌کنه، بر اساس کشور دسته‌بندی می‌کنه، و فایل‌های تمیز و بدون تکرار
منتشر می‌کنه — هر ۲ ساعت یک‌بار به‌صورت خودکار با GitHub Actions به‌روز
می‌شه.

### 🔗 لینک‌های سابسکریپشن

هر کدوم از لینک‌های زیر رو می‌تونی مستقیم توی کلاینت V2Ray خودت
(v2rayNG، NekoBox، V2Box و...) به‌عنوان لینک سابسکریپشن اضافه کنی.

| نوع | لینک |
| --- | --- |
| **ترکیبی (همه‌ی پروتکل‌ها)** | `https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/mix.txt` |
| **ترکیبی (سابسکریپشن Base64)** | `https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/mix_sub.txt` |
| **VLESS** | `https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/vless.txt` |
| **VMESS** | `https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/vmess.txt` |
| **Trojan** | `https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/trojan.txt` |
| **Shadowsocks** | `https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/ss.txt` |
| **Reality** | `https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/reality.txt` |
| **WireGuard** | `https://raw.githubusercontent.com/Idolvpn/Automate-V2ray-Config-Collector/main/configs/wireguard.txt` |

#### نحوه‌ی استفاده
۱. لینک پروتکل موردنظر (یا `mix`) رو کپی کن.
۲. کلاینت V2Ray خودت رو باز کن.
۳. برو به **Import config from URL** یا **Add subscription**.
۴. لینک رو پیست کن و تایید کن.
۵. اگه کلاینتت پشتیبانی می‌کنه، بازه‌ی آپدیت خودکار رو تنظیم کن — منبع
هر ۲ ساعت یک‌بار به‌روز می‌شه.

### ویژگی‌ها

- **چند نوع منبع**: هم لینک‌های متنی/base64، هم پیش‌نمایش کانال‌های
  عمومی تلگرام (بدون نیاز به توکن بات)
- **حذف تکراری واقعی**: کانفیگ‌ها بر اساس پروتکل + هاست + پورت +
  اطلاعات ورود (credential) بررسی می‌شن، نه فقط اسم نمایشی — پس هر بار
  اجرا، فایل‌ها پر از تکراری نمی‌شن
- **تست سلامت**: هر کانفیگ با تست همزمان اتصال TCP بررسی می‌شه؛ فقط
  کانفیگ‌های زیر آستانه‌ی تاخیر منتشر می‌شن
- **دسته‌بندی کشوری**: با درخواست‌های دسته‌ای GeoIP (تا ۱۰۰ هاست در هر
  درخواست) به‌جای یک درخواست برای هر کانفیگ
- **چند فرمت خروجی**: دسته‌بندی‌شده بر اساس پروتکل، کشور، نوع شبکه، یک
  فایل ترکیبی `mix.txt`، و یک لینک سابسکریپشن base64 با نام `mix_sub.txt`
- **کد ماژولار و قابل تست**: هر مرحله (دریافت، پردازش، حذف تکراری، تست،
  خروجی) جدا از بقیه‌ست و تست واحد داره

### ساختار پروژه

```
src/
  config/     تنظیمات و لیست منابع
  core/       دریافت، پردازش، حذف تکراری، geoip، تست، خروجی، اطلاع‌رسانی
  models/     مدل‌های Config و Protocol
  utils/      ابزار لاگ و base64
tests/        تست واحد برای هر ماژول
.github/workflows/
  collector.yml   اجرای زمان‌بندی‌شده، هر ۲ ساعت
  tests.yml       اجرای تست روی هر push / PR
```

### راه‌اندازی

```bash
pip install -r requirements.txt
cp .env.example .env   # اختیاری — تنظیمات پیش‌فرض کافیه
python -m src.main
```

خروجی توی پوشه‌ی `configs/` نوشته می‌شه (فایل‌های پروتکل، فایل‌های
کشوری، `mix.txt`، `mix_sub.txt`، و `stats.json`).

### اجرای تست‌ها

```bash
pip install -r requirements-dev.txt
pytest
```

### راه‌اندازی با GitHub Actions

ورک‌فلوی `Collect V2Ray Configs` هر ۲ ساعت به‌صورت خودکار اجرا می‌شه و
فایل‌های به‌روزشده رو زیر پوشه‌ی `configs/` کامیت می‌کنه. می‌تونی از تب
**Actions** → **Collect V2Ray Configs** → **Run workflow** هم به‌صورت
دستی اجراش کنی.

(اختیاری) اگه می‌خوای بعد از هر اجرا یه خلاصه توی تلگرام بگیری،
سکرت‌های `TELEGRAM_TOKEN` و `TELEGRAM_CHAT_ID` رو زیر
**Settings → Secrets and variables → Actions** اضافه کن.

### تنظیمات

همه‌ی مقادیر قابل تنظیم توی متغیرهای محیطی هستن — فایل `.env.example`
رو ببین: میزان همزمانی، تایم‌اوت‌ها، آستانه‌ی تاخیر، تعداد پیام‌های
بررسی‌شده در هر کانال تلگرام، و فعال/غیرفعال بودن تشخیص کشور.

برای اضافه یا حذف منبع، فایل `src/config/sources.py` رو ویرایش کن.

### سلب مسئولیت

⚠️ کانفیگ‌ها به‌صورت خودکار از منابع عمومی جمع‌آوری می‌شن و از نظر
امنیتی تضمینی ندارن. ترافیک حساس رو از طریق کانفیگ‌هایی که کنترلشون
دست خودت نیست رد نکن. این پروژه صرفاً برای پژوهش و عبور از فیلترینگ
ارائه شده.

### مجوز

MIT — فایل [LICENSE](LICENSE) رو ببین.
