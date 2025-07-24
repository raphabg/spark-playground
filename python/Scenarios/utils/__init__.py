import os

os.chdir("/wsl_mount_point/spark_data")

from . import custom_logging
from . import profiling
from . import spark_session

custom_logging.setup_logging()
profiling.setup_profiling()
spark_session.setup_spark_session()
