from aiogram import Router


def get_handlers_router() -> Router:
    from . import (
        start,
        language,
        support
    )

    router = Router()
    router.include_router(start.router)
    router.include_router(language.router)
    router.include_router(support.router)

    return router
