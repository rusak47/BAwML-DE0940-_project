import logging

def setup_logging(debug_mode=False, log_file=None, console_output=True):
    # Disable watchdog debug logging
    logging.getLogger('watchdog.observers.inotify_buffer').setLevel(logging.WARNING)
    
    # Get root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)
    
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    # Remove all existing handlers to prevent duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create a console handler and set the log level
    if console_output:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG if debug_mode else logging.INFO)

        # Create a formatter and set it for the handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(ch)

    if log_file:
        # Create file handler and set level
        fh = logging.FileHandler(log_file, mode='a')  # Use append mode
        fh.setLevel(logging.DEBUG if debug_mode else logging.INFO)
        
        # Set formatter for file handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        
        # Add file handler to logger
        logger.addHandler(fh)

if __name__ == "__main__":
    import os
    import logging
    
    print("Testing logging setup...")
    
    # Test without log file first
    print("\nTesting without log file...")
    setup_logging(debug_mode=True)
    logger = logging.getLogger()
    logger.info("Test message without log file")
    
    # Test with log file
    print("\nTesting with log file...")
    test_log_file = "test.log"
    
    # Make sure test file doesn't exist
    if os.path.exists(test_log_file):
        os.remove(test_log_file)
        print(f"✓ Cleaned up existing '{test_log_file}'")
    
    setup_logging(debug_mode=True, log_file=test_log_file, console_output=False)
    logger = logging.getLogger()
    
    print("\nTesting different log levels...")
    logger.debug("Test debug message")
    logger.info("Test info message") 
    logger.warning("Test warning message")
    logger.error("Test error message")
    logger.critical("Test critical message")
    
    # Verify log file was created and contains messages
    if os.path.exists(test_log_file):
        print(f"\n✓ Log file '{test_log_file}' was created successfully")
        with open(test_log_file, 'r') as f:
            log_contents = f.read()
            print("\nLog file contents:")
            print(log_contents)
        
        # Clean up test log file
        os.remove(test_log_file)
        print(f"\n✓ Test log file '{test_log_file}' cleaned up")
    else:
        print(f"\n✗ Failed to create log file '{test_log_file}'")