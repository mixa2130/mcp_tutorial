import asyncio
import json
import os
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.sse import sse_client

from langchain_gigachat import GigaChat
from dotenv import load_dotenv
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

load_dotenv()


class MCPClient:
    def __init__(self, llm_auth_key: str):
        self.session: Optional[ClientSession] = None

        self.exit_stack = AsyncExitStack()
        self.model: GigaChat = GigaChat(
            model="GigaChat-2-Max",
            credentials=llm_auth_key,
            verify_ssl_certs=False
        )

    async def cleanup(self):
        """Properly clean up the session and streams"""
        if self._session_context:
            await self._session_context.__aexit__(None, None, None)
        if self._streams_context:
            await self._streams_context.__aexit__(None, None, None)

    async def connect_to_sse_server(self, server_url: str):
        """Connect to an MCP server running with SSE transport"""
        # Store the context managers so they stay alive
        self._streams_context = sse_client(url=server_url)

        streams = await self._streams_context.__aenter__()

        self._session_context: ClientSession = ClientSession(*streams)
        self.session: ClientSession = await self._session_context.__aenter__()

        # Initialize
        await self.session.initialize()

        # List available tools to verify connection
        print("Initialized SSE client...")
        print("Listing tools...")
        response = await self.session.list_tools()
        print("\nConnected to server with tools:", [tool.name for tool in response.tools])

    async def process_query(self) -> str:
        """Process a query using Claude and available tools"""
        tools = await load_mcp_tools(self.session)

        # Create and run the agent
        agent = create_react_agent(self.model, tools)
        agent_response = await agent.ainvoke({"messages": "whats the weather like in Spokane?"})
        for msg in agent_response['messages']:
            print(msg)


async def main():

    client = MCPClient(os.getenv('GIGACHAT_API_KEY'))
    try:
        await client.connect_to_sse_server(server_url='http://localhost:8080/sse')
        await client.process_query()
    except Exception as exc:
        print(repr(exc))
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())