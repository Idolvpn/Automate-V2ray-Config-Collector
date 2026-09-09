from urllib.parse import urlparse, parse_qs, unquote
from typing import Optional, Dict, Any

from src.models.config import Config
from src.models.protocol import Protocol
from src.utils.encoding import decode_base64
import json


def build_xray_config(config: Config, local_port: int) -> Optional[Dict[str, Any]]:
    """Build a minimal xray config for health-checking a single config."""
    outbound = _build_outbound(config)
    if not outbound:
        return None

    return {
        "log": {"loglevel": "error"},
        "inbounds": [{
            "tag": "socks-in",
            "protocol": "socks",
            "listen": "127.0.0.1",
            "port": local_port,
            "settings": {"udp": True, "auth": "noauth"}
        }],
        "outbounds": [outbound, {"protocol": "freedom", "tag": "direct"}],
        "routing": {"rules": []}
    }


def _build_outbound(config: Config) -> Optional[Dict[str, Any]]:
    if config.protocol == Protocol.VLESS:
        return _build_vless(config)
    elif config.protocol == Protocol.VMESS:
        return _build_vmess(config)
    elif config.protocol == Protocol.TROJAN:
        return _build_trojan(config)
    elif config.protocol == Protocol.SHADOWSOCKS:
        return _build_ss(config)
    elif config.protocol == Protocol.REALITY:
        return _build_reality(config)
    return None


def _apply_transport(stream_settings: Dict[str, Any], network: str, params: dict, hostname: str) -> None:
    """Attach ws/grpc/h2/httpupgrade/xhttp settings when present."""
    path = unquote(params.get("path", [""])[0])
    host = unquote(params.get("host", [""])[0])
    if network == "ws":
        stream_settings["wsSettings"] = {
            "path": path or "/",
            "headers": {"Host": host or hostname}
        }
    elif network == "grpc":
        stream_settings["grpcSettings"] = {
            "serviceName": unquote(params.get("serviceName", [""])[0])
        }
    elif network == "h2":
        stream_settings["httpSettings"] = {
            "path": path or "/",
            "host": [host or hostname],
        }
    elif network in ("httpupgrade", "xhttp"):
        key = "xhttpSettings" if network == "xhttp" else "httpupgradeSettings"
        stream_settings[key] = {
            "path": path or "/",
            "host": host or hostname,
        }
    elif network == "tcp" and params.get("headerType", [""])[0] == "http":
        stream_settings["tcpSettings"] = {
            "header": {
                "type": "http",
                "request": {
                    "path": [path or "/"],
                    "headers": {"Host": [host or hostname]}
                }
            }
        }


def _build_vless(config: Config) -> Optional[Dict[str, Any]]:
    try:
        parsed = urlparse(config.raw)
    except ValueError:
        return None
    params = parse_qs(parsed.query)

    uuid = unquote(parsed.username or "")
    if not uuid:
        return None
    if not parsed.hostname or not parsed.port:
        return None

    security = params.get("security", [""])[0].lower()
    # A VLESS link with security=reality should have been classified as
    # REALITY by the parser; handle it here anyway for robustness.
    if security == "reality":
        return _build_reality(config)

    network = params.get("type", ["tcp"])[0]
    path = unquote(params.get("path", [""])[0])
    host = unquote(params.get("host", [""])[0])
    sni = unquote(params.get("sni", [""])[0]) or host or parsed.hostname

    stream_settings: Dict[str, Any] = {"network": network}

    if security in ("tls", "xtls"):
        stream_settings["security"] = security
        tls_settings: Dict[str, Any] = {}
        if sni:
            tls_settings["serverName"] = sni
        # Allow insecure/fingerprint params when present.
        fp = unquote(params.get("fp", [""])[0])
        if fp:
            tls_settings["fingerprint"] = fp
        if security == "tls":
            stream_settings["tlsSettings"] = tls_settings
        else:
            stream_settings["xtlsSettings"] = tls_settings

    _apply_transport(stream_settings, network, params, parsed.hostname)

    return {
        "protocol": "vless",
        "settings": {
            "vnext": [{
                "address": parsed.hostname,
                "port": parsed.port,
                "users": [{
                    "id": uuid,
                    "encryption": "none",
                    "flow": unquote(params.get("flow", [""])[0]) or ""
                }]
            }]
        },
        "streamSettings": stream_settings
    }


def _build_vmess(config: Config) -> Optional[Dict[str, Any]]:
    body = config.raw[len("vmess://"):].split("#", 1)[0].strip()
    payload = decode_base64(body)
    if not payload:
        return None
    try:
        data = json.loads(payload)
    except (json.JSONDecodeError, ValueError):
        return None

    try:
        port = int(data.get("port", 0))
    except (TypeError, ValueError):
        return None
    if not data.get("add") or not (1 <= port <= 65535):
        return None

    network = data.get("net", "tcp")
    stream_settings: Dict[str, Any] = {"network": network}

    if data.get("tls") == "tls":
        stream_settings["security"] = "tls"
        tls_settings: Dict[str, Any] = {}
        if data.get("sni") or data.get("host"):
            tls_settings["serverName"] = data.get("sni") or data.get("host")
        fp = data.get("fp")
        if fp:
            tls_settings["fingerprint"] = fp
        stream_settings["tlsSettings"] = tls_settings

    if network == "ws":
        stream_settings["wsSettings"] = {
            "path": data.get("path", "/"),
            "headers": {"Host": data.get("host", data.get("add"))}
        }
    elif network == "grpc":
        stream_settings["grpcSettings"] = {
            "serviceName": data.get("path", "")
        }

    try:
        alter_id = int(data.get("aid", 0))
    except (TypeError, ValueError):
        alter_id = 0

    user = {
        "id": data.get("id", ""),
        "alterId": alter_id,
        "security": data.get("scy", "auto")
    }
    if not user["id"]:
        return None

    return {
        "protocol": "vmess",
        "settings": {
            "vnext": [{
                "address": data.get("add"),
                "port": port,
                "users": [user]
            }]
        },
        "streamSettings": stream_settings
    }


def _build_trojan(config: Config) -> Optional[Dict[str, Any]]:
    try:
        parsed = urlparse(config.raw)
    except ValueError:
        return None
    params = parse_qs(parsed.query)

    # URL-decode password (may be percent-encoded).
    password = unquote(parsed.username or "")
    if not password:
        return None
    if not parsed.hostname or not parsed.port:
        return None

    security = params.get("security", ["tls"])[0].lower()
    network = params.get("type", ["tcp"])[0]
    path = unquote(params.get("path", [""])[0])
    host = unquote(params.get("host", [""])[0])
    sni = unquote(params.get("sni", [""])[0]) or host or parsed.hostname

    stream_settings: Dict[str, Any] = {"network": network}

    if security == "reality":
        # Trojan over Reality: same realitySettings shape as VLESS.
        pbk = unquote(params.get("pbk", [""])[0])
        sid = unquote(params.get("sid", [""])[0])
        if not pbk or not sni:
            return None
        fp = unquote(params.get("fp", [""])[0]) or "chrome"
        spx = unquote(params.get("spx", ["/"])[0])
        stream_settings["security"] = "reality"
        stream_settings["realitySettings"] = {
            "show": False,
            "fingerprint": fp,
            "serverName": sni,
            "publicKey": pbk,
            "shortId": sid,
            "spiderX": spx,
        }
    elif security == "tls":
        stream_settings["security"] = "tls"
        tls_settings: Dict[str, Any] = {}
        if sni:
            tls_settings["serverName"] = sni
        fp = unquote(params.get("fp", [""])[0])
        if fp:
            tls_settings["fingerprint"] = fp
        stream_settings["tlsSettings"] = tls_settings

    _apply_transport(stream_settings, network, params, parsed.hostname)

    return {
        "protocol": "trojan",
        "settings": {
            "servers": [{
                "address": parsed.hostname,
                "port": parsed.port,
                "password": password
            }]
        },
        "streamSettings": stream_settings
    }


def _build_ss(config: Config) -> Optional[Dict[str, Any]]:
    try:
        parsed = urlparse(config.raw)
    except ValueError:
        return None
    if not parsed.hostname or not parsed.port:
        return None

    method: Optional[str] = None
    password: Optional[str] = None

    # SIP002: ss://base64(method:password)@host:port
    if parsed.username and not parsed.password:
        body = config.raw[len("ss://"):].split("#", 1)[0]
        userinfo_b64 = body.rsplit("@", 1)[0].split("?", 1)[0].split("/", 1)[0]
        # Heuristic: base64 userinfo is long and may contain padding.
        if len(userinfo_b64) > 8:
            decoded = decode_base64(userinfo_b64)
            if decoded and ":" in decoded:
                method, password = decoded.split(":", 1)
        if method is None:
            # Plain (non-base64) method as username? e.g. ss://aes-...:pass@host
            # urlparse would have put it in username with password set, so
            # reaching here means undecodable -> invalid.
            return None
    elif parsed.username and parsed.password:
        method = unquote(parsed.username)
        password = unquote(parsed.password)
    else:
        # Legacy whole-link base64.
        try:
            auth_part = parsed.netloc.split("@")[0].split("?", 1)[0].split("/", 1)[0]
            auth = decode_base64(auth_part)
            if not auth or ":" not in auth:
                return None
            method, password = auth.split(":", 1)
        except Exception:  # noqa: BLE001
            return None

    if not method or not password:
        return None

    return {
        "protocol": "shadowsocks",
        "settings": {
            "servers": [{
                "address": parsed.hostname,
                "port": parsed.port,
                "method": method,
                "password": password
            }]
        },
        "streamSettings": {"network": "tcp"}
    }


def _build_reality(config: Config) -> Optional[Dict[str, Any]]:
    try:
        parsed = urlparse(config.raw)
    except ValueError:
        return None
    params = parse_qs(parsed.query)

    uuid = unquote(parsed.username or "")
    if not uuid:
        return None
    if not parsed.hostname or not parsed.port:
        return None

    network = params.get("type", ["tcp"])[0]
    sni = unquote(params.get("sni", [""])[0])
    fp = unquote(params.get("fp", [""])[0]) or "chrome"
    pbk = unquote(params.get("pbk", [""])[0])
    sid = unquote(params.get("sid", [""])[0])
    spx = unquote(params.get("spx", ["/"])[0])
    # Reality requires at least serverName + publicKey.
    if not sni or not pbk:
        return None

    stream_settings: Dict[str, Any] = {
        "network": network,
        "security": "reality",
        "realitySettings": {
            "show": False,
            "fingerprint": fp,
            "serverName": sni,
            "publicKey": pbk,
            "shortId": sid,
            "spiderX": spx
        }
    }

    _apply_transport(stream_settings, network, params, parsed.hostname)

    return {
        "protocol": "vless",
        "settings": {
            "vnext": [{
                "address": parsed.hostname,
                "port": parsed.port,
                "users": [{
                    "id": uuid,
                    "encryption": "none",
                    "flow": unquote(params.get("flow", [""])[0]) or "xtls-rprx-vision"
                }]
            }]
        },
        "streamSettings": stream_settings
    }
