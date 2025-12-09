import unittest
from src.hyper_core.pi_stablecoin_manager import PIStablecoinManager
from src.hyper_core.ahi_ai_core import AutonomousHyperIntelligenceAI

class TestPIStablecoinManager(unittest.TestCase):
    def setUp(self):
        self.ahi_ai = AutonomousHyperIntelligenceAI(pi_client=None, stellar_server=None)
        self.pi_manager = PIStablecoinManager(self.ahi_ai)

    def test_stablecoin_only(self):
        balance = self.pi_manager.get_balance()
        self.assertIsInstance(balance, int)

if __name__ == '__main__':
    unittest.main()
