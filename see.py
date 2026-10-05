#!/usr/bin/env python3
"""
See tool — file → MiMo-V2.5 vision via OpenCode Zen, fallback OpenCode Go.

stdin:  {"file": "C:/path/to/image.png", "prompt": "Describe this image"}
stdout: {"success": true, "text": "..."}  or {"success": false, "message": "..."}
"""
import base64
import json
import mimetypes
import os
import sys
import urllib.request
import urllib.error

# (name, url, key env, model) — tried in order, first success wins
PROVIDERS = [
    ("go", "https://opencode.ai/zen/go/v1/chat/completions", "GO_API_KEY", "mimo-v2.5"),
    ("zen", "https://opencode.ai/zen/v1/chat/completions", "ZEN_API_KEY", "mimo-v2.5-free"),
]


def get_session_id() -> str:
    """Stable per-machine ID for x-opencode-session (vendor requires one stable ID)."""
    import uuid
    sid_file = os.path.join(os.path.expanduser("~"), ".config", "opencode", "tools", ".see-session-id")
    try:
        with open(sid_file, "r") as f:
            sid = f.read().strip()
        if sid:
            return sid
    except OSError:
        pass
    sid = str(uuid.uuid4())
    try:
        with open(sid_file, "w") as f:
            f.write(sid)
    except OSError:
        pass
    return sid


def main() -> int:
    try:
        raw = sys.stdin.read().strip() or "{}"
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(json.dumps({"success": False, "message": f"Invalid JSON: {e}"}))
        return 1

    file_path = (data.get("file") or data.get("path") or "").strip()
    prompt = data.get("prompt") or "Describe this image in detail"

    if not file_path:
        print(json.dumps({"success": False, "message": "Missing 'file' parameter"}))
        return 1

    if not os.path.isfile(file_path):
        print(json.dumps({"success": False, "message": f"File not found: {file_path}"}))
        return 1

    mime, _ = mimetypes.guess_type(file_path)
    if mime is None:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            mime = "application/pdf"
        else:
            mime = "image/png"

    try:
        with open(file_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
    except Exception as e:
        print(json.dumps({"success": False, "message": f"Failed to read file: {e}"}))
        return 1

    # ponytail: no resize v1 — add thumbnail if provider rejects >20MB payload
    data_uri = f"data:{mime};base64,{b64}"

    errors = []
    for name, url, key_env, model in PROVIDERS:
        api_key = os.environ.get(key_env, "").strip()
        if not api_key:
            errors.append(f"{name}: {key_env} not set")
            continue

        payload = {
            "model": model,
            "max_tokens": 2048,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": data_uri}},
                    ],
                }
            ],
        }

        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
                "HTTP-Referer": "https://opencode.ai",
                "X-Title": "opencode-see",
                "x-opencode-session": get_session_id(),
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                resp_body = resp.read().decode("utf-8", errors="ignore")
        except urllib.error.HTTPError as e:
            err = e.read().decode(errors="ignore")[-400:]
            errors.append(f"{name} API {e.code}: {err}")
            continue
        except Exception as e:
            errors.append(f"{name}: {e}")
            continue

        try:
            j = json.loads(resp_body.strip())
            # OpenAI-compatible: choices[0].message.content
            choices = j.get("choices") or []
            if choices:
                msg = choices[0].get("message") or {}
                content = msg.get("content")
                if isinstance(content, list):
                    # content blocks
                    text = "".join(c.get("text", "") for c in content if isinstance(c, dict))
                else:
                    text = content or ""
                if not text:
                    text = msg.get("reasoning_content") or ""
                if text:
                    print(json.dumps({"success": True, "text": text}))
                    return 0
            errors.append(f"{name} unexpected response: {resp_body[:400]}")
        except Exception as e:
            errors.append(f"{name} parse error: {e} — {resp_body[:200]}")
            continue

    print(json.dumps({"success": False, "message": "; ".join(errors)}))
    return 1


if __name__ == "__main__":
    sys.exit(main())
