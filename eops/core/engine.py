# eops/core/engine.py
import time
from typing import Dict, Any

class LiveEngine:
    """
    The engine for running strategies in a live trading environment.
    """
    def __init__(self, config: Dict[str, Any]):
        self.log = print

        self.log("🔧 Initializing Live Engine...")

        # 1. Instantiate the user-defined Exchange
        exchange_class = config["exchange_class"]
        exchange_params = config["exchange_params"]
        self.exchange = exchange_class(params=exchange_params)
        self.log(f"   - Exchange loaded: {exchange_class.__name__}")

        # 2. Prepare context and instantiate the user-defined Strategy
        context = {"exchange": self.exchange}
        strategy_class = config["strategy_class"]
        strategy_params = config["strategy_params"]
        self.strategy = strategy_class(context=context, params=strategy_params)
        self.log(f"   - Strategy loaded: {strategy_class.__name__}")
        
        # 3. Get engine parameters
        engine_params = config["engine_params"]
        self.loop_interval = engine_params.get("loop_interval_seconds", 5)
        self.log(f"   - Engine loop interval: {self.loop_interval} seconds")
        self.log("✅ Engine initialization complete.")

    def run(self):
        """
        Starts the main trading loop.
        """
        self.log("🚀 Starting live trading loop...")
        try:
            while True:
                self.strategy.next()
                time.sleep(self.loop_interval)
        except KeyboardInterrupt:
            self.log("\n🛑 Live trading loop interrupted by user. Shutting down.")
        except Exception as e:
            self.log(f"\n❌ An unexpected error occurred in the trading loop: {e}")
            # Consider adding alerting mechanisms here (e.g., email, SMS)
        finally:
            self.log("👋 Eops engine has stopped.")