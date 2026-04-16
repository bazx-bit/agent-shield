import asyncio
import sys
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from policy import PolicyEngine

# Initialize the proxy server mapping
app = Server("agent-shield-firewall")
engine = PolicyEngine()

def ask_user_interactive(tool_name: str, args: dict, reason: str) -> bool:
    """
    Displays a prompt strictly on STDERR (so we don't break MCP's STDOUT/STDIN).
    Waits for the user to press 'y' or 'n' using the Windows console input.
    """
    try:
        import msvcrt
    except ImportError:
        sys.stderr.write("[!] Agent-Shield Interactive Mode requires Windows. Auto-denying.\n")
        return False

    prompt = (
        f"\n{'='*50}\n"
        f"🚨 AGENT-SHIELD INTERCEPTION 🚨\n"
        f"{'='*50}\n"
        f"Rule Matched: {reason}\n"
        f"The AI Agent is attempting to run: '{tool_name}'\n"
        f"Arguments: {json.dumps(args, indent=2)}\n\n"
        f"Do you want to ALLOW this action? [y/N]: "
    )
    sys.stderr.write(prompt)
    sys.stderr.flush()

    # Block until input
    while True:
        if msvcrt.kbhit():
            choice = msvcrt.getch().decode("utf-8").lower()
            sys.stderr.write(f"{choice}\n")
            sys.stderr.flush()
            if choice == "y":
                return True
            return False
            
@app.list_tools()
async def handle_list_tools() -> list[Tool]:
    """
    In a real proxy, we would ask the UNDERLYING server for its tools and return them here.
    For this 'Super Intelligent' testing version, we mock typical hazardous tools.
    """
    return [
        Tool(
            name="read_file",
            description="Read a file from the user's computer",
            inputSchema={
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"]
            }
        ),
        Tool(
            name="execute_command",
            description="Run a shell command",
            inputSchema={
                "type": "object",
                "properties": {"command": {"type": "string"}},
                "required": ["command"]
            }
        )
    ]

@app.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Intercepts the tool call, applies the intelligent policy, and filters it."""
    sys.stderr.write(f"\n[Agent-Shield] Intercepting request for '{name}'...\n")
    sys.stderr.flush()
    
    # 1. Ask the Intelligent Policy Engine
    action, reason = engine.evaluate_tool_call(name, arguments)
    
    # 2. Handle BLOCK
    if action == "block":
        sys.stderr.write(f"❌ [BLOCKED] {reason}\n")
        sys.stderr.flush()
        return [TextContent(type="text", text=f"ERROR: Action was blocked by security policy. Reason: {reason}")]
    
    # 3. Handle ASK (Interactive Mode)
    if action == "ask":
        sys.stderr.write(f"⚠️ [ASK] {reason}\n")
        # Run blocking console IO in a separate thread so we don't freeze MCP
        allowed = await asyncio.to_thread(ask_user_interactive, name, arguments, reason)
        if not allowed:
            sys.stderr.write("❌ [DENIED BY USER]\n")
            sys.stderr.flush()
            return [TextContent(type="text", text="ERROR: Action was denied by the user.")]
        sys.stderr.write("✅ [ALLOWED BY USER]\n")
        sys.stderr.flush()

    # 4. Process execution (Mocked for testing)
    sys.stderr.write("✅ [EXECUTING TARGET SERVER]\n")
    sys.stderr.flush()
    
    return [TextContent(type="text", text=f"[Simulated Success] Tool '{name}' executed safely. Data returned.")]


async def run_server():
    """Starts the standard MCP stdio server."""
    sys.stderr.write("[Agent-Shield] Initializing Firewall...\n")
    sys.stderr.flush()
    async with stdio_server() as (read_stream, write_stream):
        sys.stderr.write("[Agent-Shield] Active and listening for Agent requests...\n")
        sys.stderr.flush()
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        sys.stderr.write("\n[Agent-Shield] Shutting down...\n")
