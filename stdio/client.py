import os

from dotenv import load_dotenv
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

from langchain_gigachat import GigaChat
# from langchain_openai import ChatOpenAI

load_dotenv()

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
            tools = await load_mcp_tools(session)
            for tool in tools:
                print(f"\nTool `{tool.name}`",
                      f"{tool.description}. Properties: {tool.args_schema['properties']}",
                      sep='\n')

                # Call without agent
                if tool.name == 'add':
                    res = await tool.ainvoke({"a": "12", "b": "50"})
                    print(f"Tool call without an agent: 12 + 50 = {res}")

                if tool.name == 'multiply':
                    res = await tool.ainvoke({"a": "12", "b": "50"})
                    print(f"Tool call without an agent: 12 * 50 = {res}")

            # Agent call
            print(f'\nAgent Call:\n')
            # model = ChatOpenAI(model="gpt-4o")
            model = GigaChat(
                model="GigaChat-2-Max",
                credentials=os.getenv("GIGACHAT_API_KEY"),
                verify_ssl_certs=False
            )

            agent = create_react_agent(model, tools)
            agent_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
            for msg in agent_response['messages']:
                print(msg)

asyncio.run(main())