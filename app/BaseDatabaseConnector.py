import psycopg2
from psycopg2 import Error
import logging
from Setup import setup_logging
from Config import Config

class BaseDatabaseConnector:
    """
    Base class for database connections.
    Handles common functionality like connection management, logging, etc.
    """
    # Class-level logging setup
    _logging_initialized = False

    def __init__(self):
        self.connection = None
        self.cursor = None
        self.config = Config()
        self.db_config = self.config.get_database_config();

        # Only initialize logging once
        if not BaseDatabaseConnector._logging_initialized:
            logging_config = self.config.get_logging_config()
            setup_logging(
                debug_mode=logging_config.get('debug', True),
                log_file=logging_config.get('log_file', 'app.log'),
                console_output=logging_config.get('console_output', True)
            )
            BaseDatabaseConnector._logging_initialized = True

    def connect(self):
        """
        Establishes a connection to the database using configuration settings.
        Returns True if successful, False otherwise.
        """
        try:
            self.connection = psycopg2.connect(
                user=self.db_config.get('user'),
                password=self.db_config.get('password'),
                host=self.db_config.get('host'),
                port=self.db_config.get('port'),
                database=self.db_config.get('name'),
                sslmode='disable',
                connect_timeout=10,  # Connection timeout in seconds
                keepalives=1,        # Enable keepalives
                keepalives_idle=30,  # Time in seconds between keepalives
                keepalives_interval=10,  # Time in seconds between retries
                keepalives_count=5   # Number of retries before giving up
            )
            self.cursor = self.connection.cursor()
            self.debug(self.connection.get_dsn_parameters())
            return True
        
        except (Exception) as error:
            self.error(f"Error while connecting to PostgreSQL: {error}")
            return False
    
    def disconnect(self):
        """
        Closes the database connection and cursor.
        """
        if self.connection:
            if self.cursor:
                self.cursor.close()
            self.connection.close()
            self.connection = None
            self.cursor = None
            self.log("PostgreSQL connection is closed")

    def __enter__(self):
        """
        Context manager entry point.
        Establishes a database connection.
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit point.
        Handles transaction management and closes the connection.
        """
        if exc_type is not None:
            # An exception occurred, rollback
            if self.connection:
                self.connection.rollback()
                self.error(f"Transaction rolled back due to: {exc_val}")
        else:
            # No exception, commit if needed
            if self.connection and not self.connection.autocommit:
                self.connection.commit()
        
        # Always disconnect
        if self.connection:
            self.disconnect()
        
        # Don't suppress exceptions
        return False

    @staticmethod
    def log(message):
        logging.info(message)

    @staticmethod
    def debug(message):
        logging.debug(message)

    @staticmethod
    def error(message):
        logging.error(message)

    @staticmethod
    def warning(message):
        logging.warning(message)

    @staticmethod
    def critical(message):
        logging.critical(message)
