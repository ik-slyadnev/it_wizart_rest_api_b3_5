import structlog

def setup_logging():
    """
    Настройка структурированного логирования
    """
    structlog.configure(
        processors=[
            structlog.processors.JSONRenderer(
                indent=4,
                ensure_ascii=True,
                sort_keys=True
            )
        ]
    )
