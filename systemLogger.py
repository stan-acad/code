class SystemLogger:
    
    log_count = 0
    last_log_type = None

    @staticmethod
    def log_error(message):
        SystemLogger.log_count += 1
        SystemLogger.last_log_type = "ERROR"
        print(f"\nERROR: {message}\n")

    @staticmethod
    def log_info(message):
        SystemLogger.log_count += 1
        SystemLogger.last_log_type = "INFO"
        print(f"\nINFO: {message}\n")

    @staticmethod
    def log_warning(message):
        SystemLogger.log_count += 1
        SystemLogger.last_log_type = "WARNING"
        print(f"\nWARNING: {message}\n")

    @staticmethod
    def log_debug(message):
        SystemLogger.log_count += 1
        SystemLogger.last_log_type = "DEBUG"
        print(f"\nDEBUG: {message}\n")

    @staticmethod
    def reset_log_count():
        SystemLogger.log_count = 0

    @staticmethod
    def get_log_count():
        return SystemLogger.log_count

    @staticmethod
    def get_last_log_type():
        return SystemLogger.last_log_type