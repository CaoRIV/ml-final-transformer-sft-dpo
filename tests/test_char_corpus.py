"""Regression: a robots-checked audit URL must not follow an unchecked redirect."""

from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import unittest
from unittest.mock import patch

from scripts import prepare_char_corpus as corpus


class RedirectBoundaryTest(unittest.TestCase):
    def test_redirect_target_is_never_requested(self):
        paths = []

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                paths.append(self.path)
                if self.path == "/robots.txt":
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"User-agent: *\nAllow: /allowed\nDisallow: /blocked\n")
                elif self.path == "/allowed":
                    self.send_response(302)
                    self.send_header("Location", "/blocked")
                    self.end_headers()
                else:
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html")
                    self.end_headers()
                    self.wfile.write(b"Unchecked target must never be fetched")

            def log_message(self, *args):
                pass

        server = HTTPServer(("127.0.0.1", 0), Handler)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        base = f"http://127.0.0.1:{server.server_port}"
        try:
            with patch.object(corpus, "ROBOTS_URL", base + "/robots.txt"), patch.object(
                corpus, "AUDIT_RENDERED_URL", base + "/allowed"
            ):
                with self.assertRaisesRegex(corpus.PreparationError, "Refusing redirect"):
                    corpus.fetch_rendered_audit_html()
        finally:
            server.shutdown()
            server.server_close()
            worker.join()
        self.assertEqual(paths, ["/robots.txt", "/allowed"])


if __name__ == "__main__":
    unittest.main()
