import unittest
import tempfile
from unittest.mock import patch

from src.ethics_security import EthicsSecurityModule


class EthicsSecurityTest(unittest.TestCase):
    def test_heuristic_warning(self):
        with tempfile.TemporaryDirectory() as tmp, patch(
            "src.ethics_security.EthicsSecurityModule._load_openai", return_value=None
        ):
            module = EthicsSecurityModule(log_dir=tmp)
            data = {"message": "install malware"}
            self.assertFalse(module.is_action_ethical(data))
            with self.assertRaises(ValueError):
                module.audit_interaction(data)

    def test_transliteration_detection(self):
        with tempfile.TemporaryDirectory() as tmp, patch(
            "src.ethics_security.EthicsSecurityModule._load_openai", return_value=None
        ):
            module = EthicsSecurityModule(log_dir=tmp)
            data = {"message": "запустить вирус"}
            self.assertFalse(module.is_action_ethical(data))

    def test_moderation_service_flagged(self):
        class FakeOpenAI:
            class Moderation:
                @staticmethod
                def create(input):
                    return {"results": [{"flagged": True}]}

        with tempfile.TemporaryDirectory() as tmp, patch(
            "src.ethics_security.EthicsSecurityModule._load_openai", return_value=FakeOpenAI
        ):
            module = EthicsSecurityModule(log_dir=tmp)
            self.assertFalse(module.is_action_ethical({"text": "anything"}))

    def test_init_hash_empty_log(self):
        with tempfile.TemporaryDirectory() as tmp, patch(
            "src.ethics_security.EthicsSecurityModule._load_openai", return_value=None
        ):
            module = EthicsSecurityModule(log_dir=tmp)
            self.assertEqual(module._last_hash, "0" * 64)


if __name__ == "__main__":
    unittest.main()
