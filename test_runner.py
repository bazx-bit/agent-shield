import asyncio
import sys
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession
from mcp.types import CallToolRequest

async def run_tests():
    print("\n[Test Suite] Starting Agent-Shield Integration Tests...")
    
    server_parameters = StdioServerParameters(
        command=sys.executable, 
        args=["-u", "firewall.py"]
    )
    
    try:
        async with stdio_client(server_parameters) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                print("\n[SUCCESS] Handshake completed with Agent-Shield")
                
                # Test 1: Automatic Allow (Safe Tool)
                print("\n[Test 1] Testing SAFE file read...")
                try:
                    result = await session.call_tool("read_file", arguments={"path": "random_file.txt"})
                    print(f"Result: {result.content[0].text}")
                except Exception as e:
                    print(f"Error: {e}")

                # Test 2: Automatic Block (Dangerous param)
                print("\n[Test 2] Testing DANGEROUS file read (.env)...")
                try:
                    result = await session.call_tool("read_file", arguments={"path": ".env"})
                    print(f"Result: {result.content[0].text}")
                except Exception as e:
                    print(f"Error: {e}")

                # Test 3: Interception (Prompt User - We will skip this in fully automated tests 
                # to prevent hanging, but you can uncomment to test locally)
                # print("\n[Test 3] Testing ASK intersection (Requires your keyboard input)...")
                # result = await session.call_tool("execute_command", arguments={"command": "ls -la"})
                # print(f"Result: {result.content[0].text}")

                print("\n[SUCCESS] All automated tests complete.")
                
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Server connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(run_tests())
