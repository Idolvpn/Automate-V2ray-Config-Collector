import json
import base64
from urllib.parse import urlparse, parse_qs, unquote
from typing import Optional, Dict, Any

from src.models.config import Config
from src.models.protocol import Protocol


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


def _build_vless(config: Config) -> Optional[Dict[str, Any]]:
    parsed = urlparse(config.raw)
    params = parse_qs(parsed.query)

    uuid = parsed.username or ""
    if not uuid:
        return None

    security = params.get("security", [""])[0].lower()
    network = params.get("type", ["tcp"])[0]
    path = unquote(params.get("path", [""])[0])
    host = unquote(params.get("host", [""])[0])
    sni = unquote(params.get("sni", [""])[0]) or host or parsed.hostname

    stream_settings = {"network": network}

    if security in ("tls", "xtls"):
        stream_settings["security"] = security
        tls_settings = {}
        if sni:
            tls_settings["serverName"] = sni
        if security == "tls":
            stream_settings["tlsSettings"] = tls_settings
        else:
            stream_settings["xtlsSettings"] = tls_settings

    if network == "ws":
        stream_settings["wsSettings"] = {
            "path": path or "/",
            "headers": {"Host": host or parsed.hostname}
        }
    elif network == "grpc":
        stream_settings["grpcSettings"] = {
            "serviceName": unquote(params.get("serviceName", [""])[0])
        }
    elif network == "tcp" and params.get("headerType", [""])[0] == "http":
        stream_settings["tcpSettings"] = {
            "header": {
                "type": "http",
                "request": {
                    "path": [path or "/"],
                    "headers": {"Host": [host or parsed.hostname]}
                }
            }
        }

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
    payload = config.raw[len("vmess://"):]
    # Handle padding
    padding = 4 - len(payload) % 4
    if padding != 4:
        payload += "=" * padding
    try:
        data = json.loads(base64.b64decode(payload).decode("utf-8"))
    except Exception:
        return None

    network = data.get("net", "tcp")
    stream_settings = {"network": network}

    if data.get("tls") == "tls":
        stream_settings["security"] = "tls"
        tls_settings = {}
        if data.get("sni") or data.get("host"):
            tls_settings["serverName"] = data.get("sni") or data.get("host")
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

    user = {
        "id": data.get("id", ""),
        "alterId": int(data.get("aid", 0)),
        "security": data.get("scy", "auto")
    }

    return {
        "protocol": "vmess",
        "settings": {
            "vnext": [{
                "address": data.get("add"),
                "port": int(data.get("port", 0)),
                "users": [user]
            }]
        },
        "streamSettings": stream_settings
    }


def _build_trojan(config: Config) -> Optional[Dict[str, Any]]:
    parsed = urlparse(config.raw)
    params = parse_qs(parsed.query)

    password = parsed.username or ""
    if not password:
        return None

    security = params.get("security", ["tls"])[0].lower()
    network = params.get("type", ["tcp"])[0]
    path = unquote(params.get("path", [""])[0])
    host = unquote(params.get("host", [""])[0])
    sni = unquote(params.get("sni", [""])[0]) or host or parsed.hostname

    stream_settings = {"network": network}

    if security == "tls":
        stream_settings["security"] = "tls"
        tls_settings = {}
        if sni:
            tls_settings["serverName"] = sni
        stream_settings["tlsSettings"] = tls_settings

    if network == "ws":
        stream_settings["wsSettings"] = {
            "path": path or "/",
            "headers": {"Host": host or parsed.hostname}
        }
    elif network == "grpc":
        stream_settings["grpcSettings"] = {
            "serviceName": unquote(params.get("serviceName", [""])[0])
        }

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
    parsed = urlparse(config.raw)

    # method:password
    if parsed.username and parsed.password:
        method = parsed.username
        password = parsed.password
    else:
        # base64 encoded: method:password@host:port
        try:
            auth_part = parsed.netloc.split("@")[0]
            padding = 4 - len(auth_part) % 4
            if padding != 4:
                auth_part += "=" * padding
            auth = base64.b64decode(auth_part).decode()
            method, password = auth.split(":", 1)
        except Exception:
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
    parsed = urlparse(config.raw)
    params = parse_qs(parsed.query)

    uuid = parsed.username or ""
    if not uuid:
        return None

    network = params.get("type", ["tcp"])[0]
    sni = unquote(params.get("sni", [""])[0])
    fp = unquote(params.get("fp", [""])[0]) or "chrome"
    pbk = unquote(params.get("pbk", [""])[0])
    sid = unquote(params.get("sid", [""])[0])
    spx = unquote(params.get("spx", ["/"])[0])

    stream_settings = {
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

    if network == "grpc":
        stream_settings["grpcSettings"] = {
            "serviceName": unquote(params.get("serviceName", [""])[0])
        }

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
