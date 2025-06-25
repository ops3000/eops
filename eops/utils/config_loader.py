# eops/utils/config_loader.py
import importlib.util
from pathlib import Path
from typing import Dict, Any

def load_config_from_file(config_path: Path) -> Dict[str, Any]:
    """
    Dynamically loads a Python configuration file as a module.

    Args:
        config_path: The path to the Python configuration file.

    Returns:
        A dictionary containing the configuration objects.
    
    Raises:
        FileNotFoundError: If the config file does not exist.
        AttributeError: If required configurations are missing in the file.
    """
    if not config_path.is_file():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    # Create a module spec from the file path
    spec = importlib.util.spec_from_file_location(name="eops_config", location=str(config_path))
    if spec is None:
        raise ImportError(f"Could not load spec for module at {config_path}")
    
    # Create a new module based on the spec
    config_module = importlib.util.module_from_spec(spec)
    
    # Execute the module in its own namespace
    spec.loader.exec_module(config_module)

    # Extract required configurations
    try:
        config = {
            "exchange_class": config_module.EXCHANGE_CLASS,
            "exchange_params": getattr(config_module, "EXCHANGE_PARAMS", {}),
            "strategy_class": config_module.STRATEGY_CLASS,
            "strategy_params": getattr(config_module, "STRATEGY_PARAMS", {}),
            "engine_params": getattr(config_module, "ENGINE_PARAMS", {}),
            "backtest_data_path": getattr(config_module, "BACKTEST_DATA_PATH", None)
        }
        return config
    except AttributeError as e:
        raise AttributeError(f"Missing required configuration in {config_path}: {e}")