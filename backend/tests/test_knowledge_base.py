import os
import unittest

from app.services.knowledge_base import KnowledgeBase

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "data", "vespa_knowledge.db")


class KnowledgeBaseRecognitionTests(unittest.TestCase):
    def setUp(self):
        self.kb = KnowledgeBase(db_path=DB_PATH)

    def test_extract_code_prefix_removes_serial_digits(self):
        self.assertEqual("VLA1T", KnowledgeBase._extract_code_prefix("VLA1T12345"))
        self.assertEqual("VBC1T", KnowledgeBase._extract_code_prefix("VBC1T12345"))
        self.assertEqual("VMB1T", KnowledgeBase._extract_code_prefix("VMB1T12345"))
        self.assertEqual("VMA1T", KnowledgeBase._extract_code_prefix("VMA1T12345"))
        self.assertEqual("V5A1T", KnowledgeBase._extract_code_prefix("V5A1T12345"))
        self.assertEqual("ZAPM", KnowledgeBase._extract_code_prefix("ZAPM0401"))
        self.assertEqual("PX125M", KnowledgeBase._extract_code_prefix("PX125M1"))

    def test_identify_by_frame_number_handles_classic_prefixes(self):
        samples = {
            "VLA1T12345": "Vespa Sprint (VLA1T)",
            "VBC1T12345": "Vespa Sprint Veloce (VBC)",
            "VMB1T12345": "Vespa Primavera ET3 (VMB1T)",
            "VMA1T12345": "Vespa 125 Nuova (VMA1T)",
            "VSD1T12345": "Vespa Rally 180 (VSD1T)",
            "VSE1T12345": "Vespa Rally 200 (VSE1T)",
            "V5A1T12345": "Vespa 50 (V5A1T)",
        }

        for serial, expected_name in samples.items():
            with self.subTest(serial=serial):
                result = self.kb.identify_by_frame_number(serial)
                self.assertIsNotNone(result, f"Serial {serial} should match a known Vespa model")
                self.assertIn(expected_name, result["model_name"])


if __name__ == "__main__":
    unittest.main()
