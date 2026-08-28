# Raw / subscription-style text sources.
# Each entry may be plain text (one config per line), or base64-encoded
# subscription content -- the fetcher tries plain text first and falls
# back to base64 automatically.
RAW_SOURCES = [
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt",
    "https://raw.githubusercontent.com/vfarid/v2ray-share/main/configs.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/mix",
    "https://raw.githubusercontent.com/youfoundamin/V2rayCollector/main/mixed_iran.txt",
    "https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/refs/heads/main/config/all_configs.txt",
    "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt",
    "https://raw.githubusercontent.com/freefq/free/master/v2",
    "https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub",
    "https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2",
    "https://raw.githubusercontent.com/WilliamStar007/ClashX-V2Ray-TopFreeProxy/main/combine/v2raysub.txt",
    "https://raw.githubusercontent.com/peasoft/NoMoreWalls/master/list_raw.txt",
    "https://raw.githubusercontent.com/itsyebekhe/HiN-VPN/main/subscription/normal/mix",
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/xray/normal/mix",
]

# Telegram channel usernames (without @). Fetched via the public
# https://t.me/s/<channel> preview endpoint, no bot token required.
TELEGRAM_CHANNELS = [
    "v2ray_configs_pool",
    "DirectVPN",
    "v2rayngvpn",
    "vpnowl",
    "outlinevpnofficial",
    "ShadowsocksRss",
    "proxy_mtm",
]

# Channels that have repeatedly returned nothing useful. Kept separately
# (rather than silently dropped) so maintainers know why they're excluded
# and can re-enable them by moving the entry back to TELEGRAM_CHANNELS.
DISABLED_TELEGRAM_CHANNELS: list[str] = []
