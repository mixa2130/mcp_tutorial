from starlette.applications import Starlette
from starlette.routing import Mount, Route

from .app import *

app_main = Starlette(
    debug=True,
    routes=[
        Route("/sse", endpoint=sse_session_endpoint),
        # 	Mount is used to delegate an entire path prefix (/messages/) to another ASGI app or callable.
        Mount("/messages/", app=sse_post_messages_handler),
    ],
)

__all__ = [
    'app_main'
]
