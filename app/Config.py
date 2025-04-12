import os
import yaml
from typing import Dict, Any

class Config:
    _instance = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._config:
            self.load_config()

    def load_config(self):
        """Load configuration from file or environment variables"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_file = os.getenv('CONFIG_FILE', os.path.join(current_dir, 'config.yaml'))
        
        # Try to load from file first
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                self._config = yaml.safe_load(f)
        else:
            # Fallback to environment variables
            self._config = {
                'database': {
                    'user': os.getenv('DB_USER'),
                    'password': os.getenv('DB_PASSWORD'),
                    'host': os.getenv('DB_HOST'),
                    'port': os.getenv('DB_PORT'),
                    'name': os.getenv('DB_NAME')
                },
                'logging': {
                    'debug': os.getenv('LOG_DEBUG', 'true').lower() == 'true',
                    'log_file': os.getenv('LOG_FILE', 'app.log'),
                    'console_output': os.getenv('LOG_CONSOLE', 'true').lower() == 'true'
                }
            }

    def get_database_config(self) -> Dict[str, str]:
        """Get database configuration"""
        return self._config.get('database', {})

    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration"""
        return self._config.get('logging', {}) 
    

if __name__ == "__main__":
    print("Testing Config class...")
    
    # Test singleton pattern
    config1 = Config()
    config2 = Config()
    print("\nTesting singleton pattern:")
    print(f"✓ Same instance: {config1 is config2}")
    
    # Test database config
    print("\nTesting database configuration:")
    db_config = config1.get_database_config()
    print("Database config:", db_config)
    required_db_fields = ['user', 'password', 'host', 'port', 'name']
    missing_fields = [field for field in required_db_fields if field not in db_config]
    if not missing_fields:
        print("✓ All required database fields present")
    else:
        print(f"✗ Missing database fields: {missing_fields}")
        
    # Test logging config
    print("\nTesting logging configuration:")
    log_config = config1.get_logging_config()
    print("Logging config:", log_config)
    required_log_fields = ['debug', 'log_file', 'console_output']
    missing_fields = [field for field in required_log_fields if field not in log_config]
    if not missing_fields:
        print("✓ All required logging fields present")
    else:
        print(f"✗ Missing logging fields: {missing_fields}")
        
    # Test config file loading
    print("\nTesting config file loading:")
    if os.path.exists('config.yaml'):
        print("✓ Config file exists and was loaded")
    else:
        print("✓ No config file found, using environment variables")
        print("Current config:", config1._config)