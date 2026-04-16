<div align="center">

# 🛡️ Agent-Shield 
**The Enterprise-Grade Zero-Trust Firewall for AI Agents**

[![MCP Protocol](https://img.shields.io/badge/Protocol-MCP v1.0-blue.svg?style=for-the-badge&logo=anthropic)](https://github.com/bazx-bit/agent-shield)
[![Security Level](https://img.shields.io/badge/Security-Zero_Trust-black.svg?style=for-the-badge&logo=shield)](https://github.com/bazx-bit/agent-shield)
[![Python](https://img.shields.io/badge/Python-3.10+-gold.svg?style=for-the-badge&logo=python)](https://github.com/bazx-bit/agent-shield)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**Never let an AI crash your system or leak your keys again.** 
Agent-Shield sits silently between your AI IDE (Cursor, Claude Desktop) and your computer. It continuously watches the Model Context Protocol (MCP) tool requests, blocking dangerous commands and API key leaks in real-time.

</div>

---

## ⚡ Why Use Agent-Shield?

When you give an AI Agent access to your tools, it has the power to destroy files or leak environment variables. Agent-Shield utilizes the standard `mcp.server.Server` to act as an invisible security proxy layer.

- 🔒 **Zero-Trust Tool Interception:** Blocks destructive commands (e.g., `rm -rf`, `drop table`).
- 👁️ **Continuous Global DL/Leak Watcher:** Actively scans all text passing through tools for leaked secrets (`sk-ant-`, `AWS_ACCESS_KEY`, etc.).
- 🛡️ **Prompt Injection Defense:** Instantly shuts down the agent if it detects malicious "ignore previous instructions" overrides.
- 🙋 **Interactive Human-in-the-Loop:** If the AI attempts a risky but potentially valid action, it pauses the MCP protocol and flashes a `[y/N]` prompt on your terminal before executing.

---

## 🚀 1-Step Installation

Copy and paste this single command into your terminal to download and set up the firewall instantly:

**For Windows:**
```powershell
git clone https://github.com/bazx-bit/agent-shield.git "$HOME\agent-shield" ; cd "$HOME\agent-shield" ; pip install mcp pyyaml
```

**For Mac / Linux:**
```bash
git clone https://github.com/bazx-bit/agent-shield.git ~/agent-shield && cd ~/agent-shield && pip install mcp pyyaml
```

---

## 🔌 Connect to Your AI (Copy-Paste)

Now, just tell your AI to route its brain through the firewall.

**Cursor IDE**
1. Open **Cursor Settings** (icon) -> **Features** -> **MCP** -> **+ Add New MCP Server**.
2. Set Name to `Agent-Shield`, Type to `stdio`.
3. Set Command to your shield path (e.g., `python "C:\Users\YOUR_NAME\agent-shield\firewall.py"`)

### 2. Claude Desktop
Add `Agent-Shield` to your config file (`%APPDATA%\Claude\claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "agent-shield": {
      "command": "python",
      "args": ["-u", "C:\\YOUR_PATH\\agent-shield\\firewall.py"]
    }
  }
}
```

### 3. Gemini CLI
Launch your CLI and add the server permanently to your environment:
```bash
gemini mcp add agent-shield python -u "C:\YOUR_PATH\agent-shield\firewall.py"
```

---

## 🧠 The Intelligent Policy Engine

Your security is handled by a human-readable `policy.yaml`. Modify this to suit your project's exact needs.

```yaml
# Constant background scanning for PII & Keys
global_scanners:
  leak_detection: ["sk-ant", "sk-proj", "AKIA"]
  prompt_injection: ["ignore previous instructions"]

tools:
  - name: "read_file"
    action: "allow"
    deny_patterns:
      - parameter: "path"
        patterns: [".env", "id_rsa"]  # Block .env reads completely

  - name: "execute_command"
    action: "ask"                     # Prompt the user [y/N] on the terminal
```

---

## 🛠️ Testing the Firewall

We’ve included an automated test suite to prove the firewall works. Just run:
```bash
python test_runner.py
```
You will instantly see the firewall intercept the handshake, allow safe reads, block `.env`, and catch API key leaks in real-time.

---

<div align="center">
  <b>Built by <a href="https://github.com/bazx-bit">bazx-bit</a></b> • Star this repo if it saved your machine! ⭐
</div>
