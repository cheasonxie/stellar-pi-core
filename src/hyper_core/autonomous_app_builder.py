import asyncio
import logging
from typing import Dict, List, Any, Optional
import subprocess
import os
import json
from transformers import pipeline  # For generative AI app code creation
from docker import from_env  # Docker client for containerization on Pi
from kubernetes import client, config  # For orchestration (if scaled; optional for Pi)
from gpiozero import LED, Buzzer  # Pi hardware: LED for build status, Buzzer for alerts
from ahi_ai_core import AutonomousHyperIntelligenceAI  # File 1
from pi_stablecoin_manager import PIStablecoinManager  # File 2
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - App Builder: %(message)s')

class AutonomousAppBuilder:
    def __init__(self, ahi_ai: AutonomousHyperIntelligenceAI, pi_manager: PIStablecoinManager, led_pin: int = 19, buzzer_pin: int = 24):
        self.ahi_ai = ahi_ai
        self.pi_manager = pi_manager
        self.docker_client = from_env()  # Docker for Pi-based containers
        self.code_generator = pipeline("text-generation", model="gpt2")  # Generative AI for app code (hyper-simplified; use advanced models like GPT-4 in prod)
        self.apps: Dict[str, Dict] = self._load_apps()
        self.pi_led = LED(led_pin)  # Blue: building, Green: deployed, Red: failed
        self.alert_buzzer = Buzzer(buzzer_pin)  # Buzz on failures or halts
        self.reinforcement_model = self._build_reinforcement_learner()  # For self-healing and optimization

    def _load_apps(self) -> Dict[str, Dict]:
        """Loads deployed apps from storage."""
        if os.path.exists('./deployed_apps.json'):
            with open('./deployed_apps.json', 'r') as f:
                return json.load(f)
        return {}

    def _build_reinforcement_learner(self):
        """Builds a simple reinforcement learning model for app optimization (hyper-tech: use RLlib or similar)."""
        # Simplified Q-learning table for decisions
        return {'build_success': 1.0, 'deploy_fail': -1.0}  # Rewards

    async def generate_app(self, app_spec: Dict[str, Any]) -> Optional[str]:
        """Autonomously generates app code using generative AI, ensuring PI integration and no gambling apps."""
        # Explicit check for gambling to ensure no gambling apps are generated
        gambling_keywords = ['gambling', 'casino', 'bet', 'lottery', 'poker', 'slot', 'jackpot', 'dice', 'roulette', 'blackjack']
        if any(keyword in str(app_spec).lower() for keyword in gambling_keywords):
            logging.error("App generation rejected: Gambling-related spec detected. No gambling apps allowed.")
            return None
        if not await self.ahi_ai.filter_transaction({'action': 'app_gen', 'spec': app_spec}):  # Filter via AHI AI (includes anti-gambling)
            logging.error("App generation rejected: Volatile or non-compliant spec detected.")
            return None
        # Enforce PI-exclusive: All apps must use PI for transactions
        prompt = f"Generate Python code for a Pi app: {app_spec['description']}. Must use PI Coin exclusively for payments. Integrate with PI Manager. No gambling features."
        generated_code = self.code_generator(prompt, max_length=500, num_return_sequences=1)[0]['generated_text']
        # Hyper-enhance: Add PI imports and compliance checks
        enhanced_code = self._enhance_code_with_pi(generated_code)
        return enhanced_code

    def _enhance_code_with_pi(self, code: str) -> str:
        """Enhances generated code with PI integration and isolation."""
        pi_imports = "from pi_stablecoin_manager import PIStablecoinManager\n"
        compliance_check = "if not await pi_manager.create_pi_transaction(...): return 'Rejected'\n"
        return pi_imports + code + compliance_check

    async def build_and_deploy_app(self, app_name: str, app_code: str) -> bool:
        """Builds and deploys the app in a Docker container on Pi."""
        self.pi_led.blink(on_time=0.2, off_time=0.2)  # Blue: building
        # Create Dockerfile dynamically
        dockerfile_content = f"""
FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
"""
        os.makedirs(f'./apps/{app_name}', exist_ok=True)
        with open(f'./apps/{app_name}/Dockerfile', 'w') as f:
            f.write(dockerfile_content)
        with open(f'./apps/{app_name}/app.py', 'w') as f:
            f.write(app_code)
        # Build Docker image
        try:
            image, logs = self.docker_client.images.build(path=f'./apps/{app_name}', tag=f'{app_name}:latest')
            # Deploy container
            container = self.docker_client.containers.run(f'{app_name}:latest', detach=True, ports={'5000/tcp': 5000})
            self.apps[app_name] = {'container_id': container.id, 'status': 'deployed', 'code': app_code}
            self._save_apps()
            self.pi_led.on()  # Green: success
            logging.info(f"App {app_name} deployed successfully.")
            # Reward RL model
            self.reinforcement_model['build_success'] += 0.1
            return True
        except Exception as e:
            logging.error(f"Deployment failed for {app_name}: {e}")
            self.alert_buzzer.beep(on_time=1, off_time=1, n=3)  # Alert
            self.pi_led.off()  # Red: failure
            # Penalize RL
            self.reinforcement_model['deploy_fail'] -= 0.1
            return False

    async def monitor_and_manage_apps(self):
        """Autonomously monitors and manages deployed apps, scaling or healing as needed."""
        while True:
            for app_name, app_data in self.apps.items():
                try:
                    container = self.docker_client.containers.get(app_data['container_id'])
                    if container.status != 'running':
                        logging.warning(f"App {app_name} not running. Self-healing...")
                        # RL decision: Retry or rebuild
                        if random.random() < 0.8:  # Based on RL rewards
                            await self.build_and_deploy_app(app_name, app_data.get('code', ''))
                        else:
                            logging.info(f"Scaling app {app_name}...")  # Simulate scaling
                except Exception as e:
                    logging.error(f"Error monitoring app {app_name}: {e}")
                # Check Pi compliance
                if self.ahi_ai.stellar_halted:  # From File 1
                    logging.critical("Pi compliance breached. Halting all apps.")
                    self._halt_all_apps()
                    break
            await asyncio.sleep(300)  # Monitor every 5 minutes

    def _halt_all_apps(self):
        """Halts all apps on compliance breach."""
        for app_name, app_data in self.apps.items():
            try:
                container = self.docker_client.containers.get(app_data['container_id'])
                container.stop()
                logging.info(f"App {app_name} halted.")
            except Exception as e:
                logging.error(f"Error halting app {app_name}: {e}")
        self.apps.clear()
        self._save_apps()

    def _save_apps(self):
        """Saves app data."""
        with open('./deployed_apps.json', 'w') as f:
            json.dump(self.apps, f)

    async def create_app_from_spec(self, spec: Dict[str, Any]):
        """Full pipeline: Generate, build, deploy."""
        code = await self.generate_app(spec)
        if code:
            success = await self.build_and_deploy_app(spec['name'], code)
            if success:
                # Reward contributor with PI (from File 2)
                await self.pi_manager.distribute_rewards("creator", "contribution_rewards")

# Usage example (integrate into main app)
if __name__ == "__main__":
    from ahi_ai_core import AutonomousHyperIntelligenceAI  # File 1
    from pi_stablecoin_manager import PIStablecoinManager  # File 2
    # Mock setups
    ahi_ai = AutonomousHyperIntelligenceAI(pi_client=None, stellar_server=None)
    pi_manager = PIStablecoinManager(ahi_ai)
    builder = AutonomousAppBuilder(ahi_ai, pi_manager)
    # Example: Create an app
    spec = {'name': 'pi_payment_app', 'description': 'An app for PI payments on Pi hardware.'}
    asyncio.run(builder.create_app_from_spec(spec))
    # Start monitoring
    asyncio.run(builder.monitor_and_manage_apps())
