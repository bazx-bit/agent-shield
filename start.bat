@echo off
echo ===================================================
echo 🛡️ Agent-Shield MCP Firewall Booting Up...
echo ===================================================
echo Loading Policy Configuration from policy.yaml
echo Status: Active. Waiting for AI Agent connection via stdio...
echo.

:: We use -u for unbuffered output to ensure the MCP JSON-RPC protocol works perfectly.
python -u firewall.py

pause
