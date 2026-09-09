import json
from typing import Optional
from urllib.parse import parse_qs, urlparse

from src.models.config import Config
from src.models.protocol import Protocol
from src.utils.encoding import decode_base64
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

_ALLOWED_NETWORKS = {
    "tcp",
    "ws",
    "grpc",
    "h2",
    "http",
    "httpupgrade",
    "xhttp",
    "kcp",
    "quic",
    "raw",
    "none",
}


def _normalize_network(value: str) -> str:
    v = (value or "tcp").strip().lower()
    # Strip anything unsafe (e.g. 'tcp:443' from malformed sources).
    v = "".join(c for c in v if c.isalnum() or c in ("-", "_")) or "tcp"
    if v not in _ALLOWED_NETWORKS:
        # Keep unknown values but sanitized, so exporter never gets ':' etc.
        # Truncate to avoid absurd filenames.
        return v[:16]
    return v


def _valid_port(port) -> Optional[int]:
    try:
        p = int(port)
    except (TypeError, ValueError):
        return None
    if 1 <= p <= 65535:
        return p
    return None


class ConfigParser:
    """Parses raw config URIs into structured Config objects."""

    @staticmethod
    def parse(raw: str, source: str = "unknown") -> Optional[Config]:
        if not raw:
            return None
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
                # Xray-core cannot test WireGuard here, so drop early to
                # avoid wasting TCP-filter + xray cycles on configs that
                # would always be filtered out in Stage 2.
                logger.debug("Skipping unsupported wireguard config")
                return None
        except Exception as exc:  # noqa: BLE001
            # A single malformed config must never take down the whole
            # batch -- log and skip instead of raising up the stack.
            logger.debug("Failed to parse config (%s): %s", exc, raw[:60])
        return None

    @staticmethod
    def _parse_vmess(raw: str, source: str) -> Optional[Config]:
        payload = decode_base64(raw[len("vmess://") :].split("#", 1)[0])
        if not payload:
            return None
        try:
            data = json.loads(payload)
        except (json.JSONDecodeError, ValueError):
            return None
        host = data.get("add")
        port = _valid_port(data.get("port"))
        if not host or port is None:
            return None
        return Config(
            raw=raw,
            protocol=Protocol.VMESS,
            host=str(host).strip(),
            port=port,
            network=_normalize_network(str(data.get("net", "tcp"))),
            source=source,
        )

    @staticmethod
    def _parse_vless_or_reality(raw: str, source: str) -> Optional[Config]:
        try:
            parsed = urlparse(raw)
        except ValueError:
            return None
        if not parsed.hostname:
            return None
        try:
            port = parsed.port
        except ValueError:
            return None
        port = _valid_port(port)
        if port is None:
            return None
        params = parse_qs(parsed.query)
        is_reality = params.get("security", [""])[0].lower() == "reality"
        protocol = Protocol.REALITY if is_reality else Protocol.VLESS
        network = _normalize_network(params.get("type", ["tcp"])[0])
        return Config(
            raw=raw,
            protocol=protocol,
            host=parsed.hostname,
            port=port,
            network=network,
            source=source,
        )

    @staticmethod
    def _parse_standard(raw: str, protocol: Protocol, source: str) -> Optional[Config]:
        try:
            parsed = urlparse(raw)
        except ValueError:
            return None
        if not parsed.hostname:
            return None
        try:
            port = parsed.port
        except ValueError:
            return None
        port = _valid_port(port)
        if port is None:
            return None
        params = parse_qs(parsed.query)
        network = _normalize_network(params.get("type", ["tcp"])[0])
        return Config(
            raw=raw,
            protocol=protocol,
            host=parsed.hostname,
            port=port,
            network=network,
            source=source,
        )

    @staticmethod
    def _parse_shadowsocks(raw: str, source: str) -> Optional[Config]:
        # Strip fragment first; it never affects connectivity.
        body, _, _ = raw[len("ss://") :].partition("#")
        # Case 1: plain SIP002 with userinfo, e.g. ss://method:pass@host:port
        # urlparse handles this directly.
        try:
            parsed = urlparse(raw)
        except ValueError:
            parsed = None
        if parsed is not None and parsed.hostname and parsed.port:
            port = _valid_port(parsed.port)
            if port is None:
                return None
            # Sub-case 1a: ss://base64(method:pass)@host:port -- username is
            # base64, password is empty. Decode to validate.
            if parsed.username and not parsed.password and "@" in body:
                userinfo_b64 = body.rsplit("@", 1)[0].split("?", 1)[0].split("/", 1)[0]
                decoded = decode_base64(userinfo_b64)
                if decoded and ":" in decoded:
                    return Config(
                        raw=raw,
                        protocol=Protocol.SHADOWSOCKS,
                        host=parsed.hostname,
                        port=port,
                        network="tcp",
                        source=source,
                    )
                # Undecodable userinfo -> invalid.
                if "+" not in userinfo_b64 and "/" not in userinfo_b64 and "=" not in userinfo_b64:
                    # It was plain text without ':', still accept host/port.
                    return Config(
                        raw=raw,
                        protocol=Protocol.SHADOWSOCKS,
                        host=parsed.hostname,
                        port=port,
                        network="tcp",
                        source=source,
                    )
                return None
            return Config(
                raw=raw,
                protocol=Protocol.SHADOWSOCKS,
                host=parsed.hostname,
                port=port,
                network="tcp",
                source=source,
            )

        # Case 2: legacy whole-link base64: ss://base64(method:pass@host:port)
        core = body.split("?", 1)[0].split("/", 1)[0]
        decoded = decode_base64(core)
        if not decoded or "@" not in decoded:
            return None
        _, hostport = decoded.rsplit("@", 1)
        if ":" not in hostport:
            return None
        host, port_str = hostport.rsplit(":", 1)
        host = host.strip("[] ")
        port = _valid_port(port_str.strip())
        if not host or port is None:
            return None
        return Config(
            raw=raw, protocol=Protocol.SHADOWSOCKS, host=host, port=port,
            network="tcp", source=source,
        )
