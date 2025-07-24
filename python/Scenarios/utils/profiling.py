import atexit
import cProfile
from .custom_logging import stdout_logger
from pathlib import Path

def setup_profiling():
    # Start cProfile
    _profiler = cProfile.Profile()
    _profiler.enable()

    def _stop_profiler():
        """Stop the profiler and dump stats to a file."""
        _profiler.disable()
        stats_file = Path(__file__).parent / "profile_stats.prof"
        _profiler.dump_stats(stats_file)
        stdout_logger.info(f"cProfile stats saved to {stats_file}")

    # Ensure cProfile stops and dumps results when the app exits
    atexit.register(_stop_profiler)
