from http.server import ThreadingHTTPServer
import io
import json
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from gateway import Config, answer, handler, upstream_request


class GatewayTests(unittest.TestCase):
    def test_adapters(self):
        text = "Ciao!"
        samples = {
            "openai": {"output": [{"type": "message", "content": [{"type": "output_text", "text": text}]}]},
            "anthropic": {"content": [{"type": "text", "text": text}]},
            "deepseek": {"choices": [{"message": {"content": text}}]},
            "local": {"choices": [{"message": {"content": text}}]},
        }
        for provider, reply in samples.items():
            with self.subTest(provider=provider):
                local = provider == "local"
                config = Config(provider, "test-model", "" if local else "key",
                                "http://model.lan:11434/v1/chat/completions" if local else "")
                def fake(request, timeout):
                    data = json.loads(request.data)
                    self.assertEqual(data["model"], "test-model")
                    self.assertEqual(timeout, 25)
                    if provider == "openai":
                        self.assertEqual(data["input"], "test")
                        self.assertFalse(data["store"])
                    else:
                        self.assertEqual(data["messages"][-1]["content"], "test")
                    if provider == "anthropic":
                        self.assertEqual(request.get_header("X-api-key"), "key")
                    elif local:
                        self.assertIsNone(request.get_header("Authorization"))
                    else:
                        self.assertEqual(request.get_header("Authorization"), "Bearer key")
                    return io.BytesIO(json.dumps(reply).encode())
                self.assertEqual(answer(config, "test", fake), text)

    def test_local_token_requires_tls(self):
        with self.assertRaises(ValueError):
            Config("local", "m", "secret", "http://model.lan/v1/chat/completions")
        req = upstream_request(Config("local", "m", "secret", "https://model.lan/v1/chat/completions"), "ciao")
        self.assertEqual(req.get_header("Authorization"), "Bearer secret")

    def test_real_loopback_and_auth(self):
        token = "test-token-for-local-requests"
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler(Config("basic"), token))
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            url = f"http://127.0.0.1:{server.server_port}/v1/ask"
            body = b'{"prompt":"ciao"}'
            with self.assertRaises(HTTPError) as denied:
                urlopen(Request(url, data=body), timeout=3)
            self.assertEqual(denied.exception.code, 401)
            headers = {"Authorization": f"Bearer {token}"}
            with urlopen(Request(url, data=body, headers=headers), timeout=3) as response:
                self.assertEqual(json.load(response)["text"], "Ciao, sono Paky76.")
            with self.assertRaises(HTTPError) as invalid:
                urlopen(Request(url, data=b"[]", headers=headers), timeout=3)
            self.assertEqual(invalid.exception.code, 400)
        finally:
            server.shutdown()
            server.server_close()
            worker.join(timeout=3)
