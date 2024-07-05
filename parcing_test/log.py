from datetime import datetime

from loguru import logger

format = (
    "{extra[utc]} --- "
    "{level} --- "
    "{message}"
)

logger.configure(
    handlers=[
        dict(sink="errors.log", format=format, level="ERROR", rotation="10 Mb", enqueue=True),
    ],
    extra={"common_to_all": "default"},
    patcher=lambda record: record["extra"].update(utc=datetime.now()),
    activation=[("my_module.secret", False), ("another_library.module", True)],
)
