from starlette.requests import Request
from mcp.server.sse import SseServerTransport
from .mcp_api import mcp_server

sse = SseServerTransport("/messages/")
sse_post_messages_handler = sse.handle_post_message

async def sse_session_endpoint(request: Request) -> None:
    async with sse.connect_sse(
            request.scope,
            request.receive,
            request._send,  # noqa: SLF001
    ) as (read_stream, write_stream):
        await mcp_server.run(
            read_stream,
            write_stream,
            mcp_server.create_initialization_options()
        )


__all__ = [
    'sse_session_endpoint',
    'sse_post_messages_handler'
]
