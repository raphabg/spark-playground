import sys
import os
import gzip
import shutil
import time
import logging
from logging.handlers import BaseRotatingHandler

# ============================================
# Combined Rotating File Handler (Size + Time)
# ============================================

class CompressingSizeAndTimeRotatingFileHandler(BaseRotatingHandler):
    """
    A log handler that rotates logs based on both size and time intervals,
    with gzip compression of old logs.
    """

    def __init__(self, filename, maxBytes=0, when="h", interval=1, backupCount=5, encoding=None, delay=False):
        """
        :param filename: The log file name.
        :param maxBytes: Max file size in bytes before rotation (0 disables size-based rotation).
        :param when: Time interval type ('S', 'M', 'H', 'D').
        :param interval: How many 'when' units before rotation.
        :param backupCount: Number of compressed log backups to keep.
        """
        self.maxBytes = maxBytes
        self.when = when.upper()
        self.interval = interval
        self.backupCount = backupCount

        # Map time interval to seconds
        self.when_dict = {
            'S': 1,
            'M': 60,
            'H': 60 * 60,
            'D': 60 * 60 * 24,
        }
        if self.when not in self.when_dict:
            raise ValueError("Invalid rollover interval specified: %s" % self.when)

        self.interval_seconds = self.when_dict[self.when] * self.interval
        self.rolloverAt = self.compute_initial_rollover(time.time())

        BaseRotatingHandler.__init__(self, filename, 'a', encoding, delay)

    def compute_initial_rollover(self, current_time):
        """Calculate the next rollover timestamp."""
        return current_time + self.interval_seconds

    def shouldRollover(self, record):
        """
        Determine if rollover should occur:
        - If the current file size exceeds maxBytes (if set).
        - If the current time exceeds the scheduled rollover time.
        """
        if self.stream is None:
            self.stream = self._open()

        # Check size-based rotation
        if self.maxBytes > 0:
            self.stream.seek(0, os.SEEK_END)
            if self.stream.tell() >= self.maxBytes:
                return True

        # Check time-based rotation
        current_time = time.time()
        if current_time >= self.rolloverAt:
            return True

        return False

    def doRollover(self):
        """
        Perform log rotation: rename and compress old log files.
        """
        if self.stream:
            self.stream.close()
        current_time = time.time()
        self.rolloverAt = self.compute_initial_rollover(current_time)

        # Rotate old log files
        for i in range(self.backupCount - 1, 0, -1):
            sfn = f"{self.baseFilename}.{i}.gz"
            dfn = f"{self.baseFilename}.{i + 1}.gz"
            if os.path.exists(sfn):
                if os.path.exists(dfn):
                    os.remove(dfn)
                os.rename(sfn, dfn)

        # Rename current log to .1
        dfn = f"{self.baseFilename}.1"
        if os.path.exists(dfn + ".gz"):
            os.remove(dfn + ".gz")
        if os.path.exists(self.baseFilename):
            os.rename(self.baseFilename, dfn)

        # Compress .1 log
        if os.path.exists(dfn):
            with open(dfn, 'rb') as f_in, gzip.open(dfn + ".gz", 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
            os.remove(dfn)

        # Reopen the stream
        self.stream = self._open()

    def getFilesToDelete(self):
        """
        Determine which log files are old and should be removed.
        """
        dirName, baseName = os.path.split(self.baseFilename)
        fileNames = os.listdir(dirName)
        result = []
        prefix = baseName + "."
        plen = len(prefix)
        for fileName in fileNames:
            if fileName.startswith(prefix) and fileName.endswith(".gz"):
                suffix = fileName[plen:-3]
                if suffix.isdigit():
                    result.append(os.path.join(dirName, fileName))
        result.sort()
        return result[:-self.backupCount]  # Keep only the last `backupCount` files


# ============================================
# Stream Redirection Class
# ============================================

class StreamToLogger:
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level
        self._buffer = ""

    def write(self, message):
        self._buffer += message
        while "\n" in self._buffer:
            line, self._buffer = self._buffer.split("\n", 1)
            if line.strip():
                self.logger.log(self.level, line.strip())

    def flush(self):
        if self._buffer.strip():
            self.logger.log(self.level, self._buffer.strip())
        self._buffer = ""


# ============================================
# Logging Setup
# ============================================

_is_logging_configured = False

def setup_logging(log_dir=None):
    """
    Configure logging for stdout and stderr with combined size+time rolling and compression.
    Ensures no duplicate handlers are added.
    """
    global _is_logging_configured
    if _is_logging_configured:
        return  # Already configured

    # Clear root handlers
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    log_dir = log_dir or os.getenv("SPARK_DRIVER_LOGS_DIR", "./logs")
    os.makedirs(log_dir, exist_ok=True)

    stdout_log = os.path.join(log_dir, "driver.stdout.log")
    stderr_log = os.path.join(log_dir, "driver.stderr.log")

    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(name)s:  %(message)s', "%Y-%m-%d %H:%M:%S"
    )

    # ========================
    # STDOUT Logger
    # ========================
    stdout_logger = logging.getLogger("DriverStdout")
    stdout_logger.setLevel(logging.INFO)
    stdout_logger.propagate = False
    stdout_logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.__stdout__)
    console_handler.setFormatter(formatter)
    stdout_logger.addHandler(console_handler)

    # Combined handler
    stdout_handler = CompressingSizeAndTimeRotatingFileHandler(
        stdout_log, maxBytes=100 * 1024 * 1024, when="h", interval=1, backupCount=5
    )
    stdout_handler.setFormatter(formatter)
    stdout_logger.addHandler(stdout_handler)

    # ========================
    # STDERR Logger
    # ========================
    stderr_logger = logging.getLogger("DriverStderr")
    stderr_logger.setLevel(logging.ERROR)
    stderr_logger.propagate = False
    stderr_logger.handlers.clear()

    stderr_handler = CompressingSizeAndTimeRotatingFileHandler(
        stderr_log, maxBytes=100 * 1024 * 1024, when="h", interval=1, backupCount=5
    )
    stderr_handler.setFormatter(formatter)
    stderr_logger.addHandler(stderr_handler)

    # ========================
    # Redirect stdout/stderr
    # ========================
    sys.stdout = StreamToLogger(stdout_logger, logging.INFO)
    sys.stderr = StreamToLogger(stderr_logger, logging.ERROR)

    _is_logging_configured = True
