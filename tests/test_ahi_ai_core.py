import unittest
from src.hyper_core.ahi_ai_core import AutonomousHyperIntelligenceAI

class TestAHIAICore(unittest.TestCase):
    def setUp(self):
        self.ahi_ai = AutonomousHyperIntelligenceAI(pi_client=None, stellar_server=None)

    def test_anti_gambling_filter(self):
        result = self.ahi_ai._check_gambling_filter({'description': 'gambling app'})
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
