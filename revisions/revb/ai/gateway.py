#!/usr/bin/env python3
"""Paky76 text gateway. Configure a provider and model per process."""
import argparse
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import hmac
import json
import os
from urllib.error import URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


SYSTEM = "Sei Paky76. Rispondi in italiano con frasi brevi, adatte a essere lette ad alta voce."
REMOTE = {
    "openai": "https://api.openai.com/v1/responses",
    "anthropic": "https://api.anthropic.com/v1/messages",
    "deepseek": "https://api.deepseek.com/chat/completions",
}
MAX_BODY = 8192


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *_args, **_kwargs):
        return None


@dataclass(frozen=True)
class Config:
    provider: str
    model: str = ""
    api_key: str = ""
    local_url: str = ""

    def __post_init__(self):
        if self.provider not in {*REMOTE, "local", "basic"}:
            raise ValueError("Provider non supportato")
        if self.provider != "basic" and not self.model:
            raise ValueError("PAKY_AI_MODEL è obbligatorio")
        if self.provider in REMOTE and not self.api_key:
            raise ValueError("PAKY_UPSTREAM_KEY è obbligatoria")
        if self.provider == "local":
            url = urlsplit(self.local_url)
            if (url.scheme not in {"http", "https"} or not url.hostname or url.username
                    or url.password or url.query or url.fragment):
                raise ValueError("PAKY_LOCAL_URL deve essere un URL HTTP(S) senza credenziali")
            if url.scheme == "http" and self.api_key:
                raise ValueError("Una chiave per il server interno richiede HTTPS")


def upstream_request(c, prompt):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if c.provider == "anthropic":
        headers.update({"x-api-key": c.api_key, "anthropic-version": "2023-06-01"})
        body = {"model": c.model, "system": SYSTEM, "max_tokens": 256,
                "messages": [{"role": "user", "content": prompt}]}
    else:
        if c.api_key:
            headers["Authorization"] = "Bearer " + c.api_key
        if c.provider == "openai":
            body = {"model": c.model, "instructions": SYSTEM, "input": prompt,
                    "max_output_tokens": 256, "store": False}
        else:
            body = {"model": c.model, "max_tokens": 256,
                    "messages": [{"role": "system", "content": SYSTEM},
                                 {"role": "user", "content": prompt}]}
    url = c.local_url if c.provider == "local" else REMOTE[c.provider]
    return Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")


def answer(c, prompt, opener=None):
    if c.provider == "basic":
        if prompt.casefold().strip(" !?.") in {"ciao", "salve", "buongiorno"}:
            return "Ciao, sono Paky76."
        if prompt.casefold().strip(" !?.") == "chi sei":
            return "Sono Paky76, il tuo assistente da scrivania."
        return "Sono in modalità di base. Posso rispondere solo a pochi comandi."
    opener = opener or build_opener(NoRedirect()).open
    with opener(upstream_request(c, prompt), timeout=25) as response:
        raw = response.read(262145)
    if len(raw) > 262144:
        raise ValueError("Risposta upstream troppo grande")
    result = json.loads(raw)
    if c.provider == "openai":
        out = [part.get("text", "") for item in result.get("output", [])
               if item.get("type") == "message" for part in item.get("content", [])
               if part.get("type") == "output_text"]
    elif c.provider == "anthropic":
        out = [part.get("text", "") for part in result.get("content", []) if part.get("type") == "text"]
    else:
        out = [result["choices"][0]["message"]["content"]]
    text = " ".join(s.strip() for s in out if isinstance(s, str) and s.strip())
    if not text:
        raise ValueError("Il provider non ha restituito testo")
    return text[:3000]


def handler(config, token):
    class Handler(BaseHTTPRequestHandler):
        def reply(self, status, payload):
            body = json.dumps(payload, ensure_ascii=False).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_POST(self):
            if self.path != "/v1/ask":
                return self.reply(404, {"error": "Endpoint sconosciuto"})
            auth = self.headers.get("Authorization", "").encode()
            if not hmac.compare_digest(auth, ("Bearer " + token).encode()):
                return self.reply(401, {"error": "Credenziali richieste"})
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= MAX_BODY:
                    return self.reply(413, {"error": "Richiesta troppo grande o vuota"})
                self.connection.settimeout(10)
                prompt = json.loads(self.rfile.read(length)).get("prompt")
                if not isinstance(prompt, str) or not 0 < len(prompt.strip()) <= 2000:
                    raise ValueError
            except (AttributeError, ValueError, TimeoutError):
                return self.reply(400, {"error": "Prompt non valido"})
            try:
                text = answer(config, prompt.strip())
            except (URLError, OSError, ValueError, KeyError, IndexError, TypeError, AttributeError):
                return self.reply(502, {"error": "Modello temporaneamente non disponibile"})
            return self.reply(200, {"text": text, "provider": config.provider, "model": config.model})

    return Handler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8766)
    args = parser.parse_args()
    token = os.environ.get("PAKY_GATEWAY_TOKEN", "")
    if len(token) < 24:
        parser.error("PAKY_GATEWAY_TOKEN deve avere almeno 24 caratteri")
    try:
        config = Config(os.getenv("PAKY_AI_PROVIDER", "basic"), os.getenv("PAKY_AI_MODEL", ""),
                        os.getenv("PAKY_UPSTREAM_KEY", ""), os.getenv("PAKY_LOCAL_URL", ""))
    except ValueError as exc:
        parser.error(str(exc))
    with ThreadingHTTPServer(("127.0.0.1", args.port), handler(config, token)) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
