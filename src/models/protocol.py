from enum import Enum


class Protocol(str, Enum):
    """Supported V2Ray / proxy protocols."""

    VMESS = "vmess"
    VLESS = "vless"
    TROJAN = "trojan"
    SHADOWSOCKS = "ss"
    WIREGUARD = "wireguard"
    REALITY = "reality"

    def __str__(self) -> str:
        return self.value
