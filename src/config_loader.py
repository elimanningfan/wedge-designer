"""
Configuration loader for wedge designer.
Loads and validates YAML configuration files.
"""

import yaml
import os
from typing import Dict, Any


class WedgeConfig:
    """
    Loads and validates wedge configuration from YAML file.
    
    Usage:
        config = WedgeConfig('configs/vokey_56_8.yaml')
        loft = config.get('wedge_specs.loft')
        hosel_bore = config.get('wedge_specs.hosel.bore_diameter')
    """
    
    def __init__(self, config_path: str):
        """
        Initialize configuration from YAML file.
        
        Args:
            config_path: Path to YAML configuration file
        """
        self.config_path = config_path
        self.config = self._load_yaml()
        self._validate()
    
    def _load_yaml(self) -> Dict[str, Any]:
        """Load YAML configuration file."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        return config
    
    def _validate(self):
        """
        Validate that required configuration fields are present.
        Raises ValueError if validation fails.
        """
        # TODO: Implement validation logic
        # Check for required fields:
        # - wedge_specs.loft (45-64 degrees)
        # - wedge_specs.lie (60-66 degrees)
        # - wedge_specs.bounce (0-16 degrees)
        # - wedge_specs.hosel.bore_diameter (9.4mm standard)
        # etc.
        
        required_fields = [
            'wedge_specs.loft',
            'wedge_specs.lie',
            'wedge_specs.bounce',
        ]
        
        for field in required_fields:
            value = self.get(field)
            if value is None:
                raise ValueError(f"Required field missing: {field}")
        
        # Validate ranges
        loft = self.get('wedge_specs.loft')
        if not (45 <= loft <= 64):
            raise ValueError(f"Loft must be between 45-64 degrees, got {loft}")
        
        bounce = self.get('wedge_specs.bounce')
        if not (0 <= bounce <= 16):
            raise ValueError(f"Bounce must be between 0-16 degrees, got {bounce}")
        
        print(f"✓ Configuration validated: {self.config_path}")
    
    def get(self, key_path: str, default=None):
        """
        Get configuration value using dot-notation path.
        
        Args:
            key_path: Dot-separated path (e.g., 'wedge_specs.hosel.bore_diameter')
            default: Default value if key not found
        
        Returns:
            Configuration value or default
        
        Example:
            config.get('wedge_specs.loft')  # Returns 56
            config.get('wedge_specs.hosel.bore_diameter')  # Returns 9.4
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def get_all(self) -> Dict[str, Any]:
        """Return entire configuration dictionary."""
        return self.config


# Convenience function for quick loading
def load_config(config_path: str) -> WedgeConfig:
    """
    Load a wedge configuration file.
    
    Args:
        config_path: Path to YAML config file
    
    Returns:
        WedgeConfig object
    """
    return WedgeConfig(config_path)


if __name__ == "__main__":
    # Test configuration loading
    config = load_config('configs/vokey_56_8.yaml')
    
    print("\nConfiguration loaded successfully!")
    print(f"Wedge name: {config.get('wedge_specs.name')}")
    print(f"Loft: {config.get('wedge_specs.loft')}°")
    print(f"Bounce: {config.get('wedge_specs.bounce')}°")
    print(f"Hosel bore: {config.get('wedge_specs.hosel.bore_diameter')}mm")
