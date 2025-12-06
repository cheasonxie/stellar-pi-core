import unittest
from src.hyper_core.ahi_ai_core import AutonomousHyperIntelligenceAI

class TestAHIAI(unittest.TestCase):
    def test_gambling_filter(self):
        ahi_ai = AutonomousHyperIntelligenceAI(pi_client=None, stellar_server=None)
        result = ahi_ai._check_gambling_filter({'description': 'gambling app'})
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
