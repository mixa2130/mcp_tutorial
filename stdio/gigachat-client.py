import os

from dotenv import load_dotenv
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

load_dotenv()

# from langchain_openai import ChatOpenAI
# model = ChatOpenAI(model="gpt-4o")
from langchain_gigachat import GigaChat

model = GigaChat(
    model="GigaChat-2-Max",
    credentials=os.getenv("GIGACHAT_API_KEY"),
    verify_ssl_certs=False
)
server_params = StdioServerParameters(
    command="python",
    # Make sure to update to the full absolute path to your math_server.py file
    args=["./server.py"],
)

async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            print("Available tools:")
            tools = await load_mcp_tools(session)
            for tool in tools:
                print(tool)

            # Create and run the agent
            agent = create_react_agent(model, tools)
            agent_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
            for msg in agent_response['messages']:
                print(msg)

asyncio.run(main())