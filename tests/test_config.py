import os
import unittest
from unittest.mock import patch

from config import get_settings


class ConfigTests(unittest.TestCase):
    def test_get_settings_requires_token(self) -> None:
        with patch.dict(os.environ, {"BOT_TOKEN": "   "}, clear=False):
            with self.assertRaises(RuntimeError):
                get_settings()

    def test_get_settings_parses_values(self) -> None:
        env = {
            "BOT_TOKEN": "123:abc",
            "LOG_LEVEL": "debug",
            "ADMIN_IDS": "1, 2, bad,3",
            "DB_PATH": "tmp/test.db",
            "RUN_MODE": "WEBHOOK",
            "WEBHOOK_BASE_URL": "https://example.com/",
            "WEBHOOK_PATH": "hook",
            "THROTTLE_SECONDS": "1.5",
        }
        with patch.dict(os.environ, env, clear=False):
            s = get_settings()
        self.assertEqual(s.bot_token, "123:abc")
        self.assertEqual(s.log_level, "DEBUG")
        self.assertEqual(s.admin_ids, frozenset({1, 2, 3}))
        self.assertEqual(s.db_path, "tmp/test.db")
        self.assertEqual(s.run_mode, "webhook")
        self.assertEqual(s.webhook_base_url, "https://example.com")
        self.assertEqual(s.webhook_path, "/hook")
        self.assertEqual(s.throttle_seconds, 1.5)


if __name__ == "__main__":
    unittest.main()
