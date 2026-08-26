import json
from typing import Optional
from urllib.parse import parse_qs, urlparse

from src.models.config import Config
from src.models.protocol import Protocol
from src.utils.encoding import decode_base64
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class ConfigParser:
    """Parses raw config URIs into structured Config objects."""

    @staticmethod
    def parse(raw: str, source: str = "unknown") -> Optional[Config]:
        raw = raw.strip()
        try:
            if raw.startswith("vmess://"):
                return ConfigParser._parse_vmess(raw, source)
            if raw.startswith("vless://"):
                return ConfigParser._parse_vless_or_reality(raw, source)
            if raw.startswith("trojan://"):
                return ConfigParser._parse_standard(raw, Protocol.TROJAN, source)
            if raw.startswith("ss://"):
                return ConfigParser._parse_shadowsocks(raw, source)
            if raw.startswith("wireguard://"):
                return ConfigParser._parse_standard(raw, Protocol.WIREGUARD, source)
        except Exception as exc:  # noqa: BLE001
            # A single malformed config must never take down the whole
            # batch -- log and skip instead of raising up the stack.
            logger.debug("Failed to parse config (%s): %s", exc, raw[:60])
        return None

    @staticmethod
    def _parse_vmess(raw: str, source: str) -> Optional[Config]:
        payload = decode_base64(raw[len("vmess://"):])
        if not payload:
            return None
        data = json.loads(payload)
        host = data.get("add")
        port = data.get("port")
        if not host or not port:
            return None
        return Config(
            raw=raw,
            protocol=Protocol.VMESS,
            host=str(host),
            port=int(port),
            network=str(data.get("net", "tcp")),
            source=source,
        )

    @staticmethod
    def _parse_vless_or_reality(raw: str, source: str) -> Optional[Config]:
        parsed = urlparse(raw)
        if not parsed.hostname or not parsed.port:
            return None
        params = parse_qs(parsed.query)
        is_reality = params.get("security", [""])[0].lower() == "reality"
        protocol = Protocol.REALITY if is_reality else Protocol.VLESS
        network = params.get("type", ["tcp"])[0]
        return Config(
            raw=raw,
            protocol=protocol,
            host=parsed.hostname,
            port=parsed.port,
            network=network,
            source=source,
        )

    @staticmethod
    def _parse_standard(raw: str, protocol: Protocol, source: str) -> Optional[Config]:
        parsed = urlparse(raw)
        if not parsed.hostname or not parsed.port:
            return None
        params = parse_qs(parsed.query)
        network = params.get("type", ["tcp"])[0]
        return Config(
            raw=raw,
            protocol=protocol,
            host=parsed.hostname,
            port=parsed.port,
            network=network,
            source=source,
        )

    @staticmethod
    def _parse_shadowsocks(raw: str, source: str) -> Optional[Config]:
        parsed = urlparse(raw)
        if parsed.hostname and parsed.port:
            return Config(
                raw=raw,
                protocol=Protocol.SHADOWSOCKS,
                host=parsed.hostname,
                port=parsed.port,
                source=source,
            )

        # Legacy ss:// links base64-encode "method:password@host:port"
        # in their entirety instead of using a plain netloc.
        body = raw[len("ss://"):].split("#", 1)[0]
        decoded = decode_base64(body)
        if not decoded or "@" not in decoded:
            return None
        _, hostport = decoded.rsplit("@", 1)
        if ":" not in hostport:
            return None
        host, port_str = hostport.rsplit(":", 1)
        try:
            port = int(port_str)
        except ValueError:
            return None
        return Config(
            raw=raw, protocol=Protocol.SHADOWSOCKS, host=host, port=port, source=source
        )
