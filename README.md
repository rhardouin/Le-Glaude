# Le Glaude

[![PyPI Version](https://img.shields.io/pypi/v/le-glaude)](https://pypi.org/project/le-glaude)
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/release/python-3120/)
[![CI Status](https://github.com/rhardouin/Le-Glaude/actions/workflows/ci.yml/badge.svg)](https://github.com/rhardouin/Le-Glaude/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/rhardouin/Le-Glaude)](https://github.com/rhardouin/Le-Glaude/blob/main/LICENSE)


```
       _.---._
     .'       '.
 _.-'  O  O  O  '-._     << If Claude can code, wait 'til you see Le Glaude! >>
(___________________)
     /         \
    /___________\
```

## Silicon Valley gave us Claude. France strikes back with Le Glaude.

Le Glaude is a humorous TUI coding assistant providing a conversational interface to your codebase. It allows you to use natural language to explore, modify, and interact with your projects through a powerful set of tools.

> [!WARNING]
> Le Glaude is usable by everyone, but the humor is deeply rooted in French culture. References come from the movie [La Soupe aux choux](https://en.wikipedia.org/wiki/La_Soupe_aux_choux), where the main character is named 'Le Glaude'—which is simply the rustic, countryside pronunciation of 'Le Claude'. Think of him as the original, organic AI of the French terroir. **As such, the loading messages ("easter eggs") are entirely in French.**

### One-line install (recommended)

**Linux and macOS**

```bash
curl -LsSf https://raw.githubusercontent.com/rhardouin/Le-Glaude/main/scripts/install.sh | bash
```

**Windows**

Support for Windows is experimental.

First, install uv
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then, use uv command below.

### Using uv

```bash
uv tool install le-glaude
```

### Using pip

```bash
pip install le-glaude
```

## Features

- **Interactive Chat**: A conversational AI agent that understands your requests and breaks down complex tasks.
- **Powerful Toolset**: A suite of tools for file manipulation, code searching, version control, and command execution, right from the chat prompt.
  - Read, write, and patch files (`read_file`, `write_file`, `search_replace`).
  - Execute shell commands in a stateful terminal (`bash`).
  - Recursively search code with `grep` (with `ripgrep` support).
  - Manage a `todo` list to track the agent's work.
- **Project-Aware Context**: Le Glaude automatically scans your project's file structure and Git status to provide relevant context to the agent, improving its understanding of your codebase.
- **Advanced CLI Experience**: Built with modern libraries for a smooth and efficient workflow.
  - Autocompletion for slash commands (`/`) and file paths (`@`).
  - Persistent command history.
  - Beautiful Themes.
- **Highly Configurable**: Customize models, providers, tool permissions, and UI preferences through a simple `config.toml` file.
- **Safety First**: Features tool execution approval.

## Quick Start

1. Navigate to your project's root directory:

   ```bash
   cd /path/to/your/project
   ```

2. Run Glaude:

   ```bash
   glaude
   ```

3. If this is your first time running Glaude, it will:

   - Create a default configuration file at `~/.glaude/config.toml`
   - Prompt you to enter your API key if it's not already configured
   - Save your API key to `~/.glaude/.env` for future use

4. Start interacting with the agent!

   ```
   > Can you find all instances of the word "TODO" in the project?

   🤖 The user wants to find all instances of "TODO". The `grep` tool is perfect for this. I will use it to search the current directory.

   > grep(pattern="TODO", path=".")

   ... (grep tool output) ...

   🤖 I found the following "TODO" comments in your project.
   ```

## Usage

### Interactive Mode

Simply run `glaude` to enter the interactive chat loop.

- **Multi-line Input**: Press `Ctrl+J` or `Shift+Enter` for select terminals to insert a newline.
- **File Paths**: Reference files in your prompt using the `@` symbol for smart autocompletion (e.g., `> Read the file @src/agent.py`).
- **Shell Commands**: Prefix any command with `!` to execute it directly in your shell, bypassing the agent (e.g., `> !ls -l`).

You can start Glaude with a prompt with the following command:

```bash
glaude "Refactor the main function in cli/main.py to be more modular."
```

**Note**: The `--auto-approve` flag automatically approves all tool executions without prompting. In interactive mode, you can also toggle auto-approve on/off using `Shift+Tab`.

### Programmatic Mode

You can run Glaude non-interactively by piping input or using the `--prompt` flag. This is useful for scripting.

```bash
glaude --prompt "Refactor the main function in cli/main.py to be more modular."
```

by default it will use `auto-approve` mode.

### Slash Commands

Use slash commands for meta-actions and configuration changes during a session.

## Configuration

Le Glaude is configured via a `config.toml` file. It looks for this file first in `./.glaude/config.toml` and then falls back to `~/.glaude/config.toml`.

### API Key Configuration

Le Glaude supports multiple ways to configure your API keys:

1. **Interactive Setup (Recommended for first-time users)**: When you run Le Glaude for the first time or if your API key is missing, Le Glaude will prompt you to enter it. The key will be securely saved to `~/.glaude/.env` for future sessions.

2. **Environment Variables**: Set your API key as an environment variable:

   ```bash
   export MISTRAL_API_KEY="your_api_key"
   ```

3. **`.env` File**: Create a `.env` file in `~/.glaude/` and add your API keys:

   ```bash
   MISTRAL_API_KEY=your_api_key
   ```

   Le Glaude automatically loads API keys from `~/.glaude/.env` on startup. Environment variables take precedence over the `.env` file if both are set.

**Note**: The `.env` file is specifically for API keys and other provider credentials. General Le Glaude configuration should be done in `config.toml`.

### Custom System Prompts

You can create custom system prompts to replace the default one (`prompts/cli.md`). Create a markdown file in the `~/.glaude/prompts/` directory with your custom prompt content.

To use a custom system prompt, set the `system_prompt_id` in your configuration to match the filename (without the `.md` extension):

```toml
# Use a custom system prompt
system_prompt_id = "my_custom_prompt"
```

This will load the prompt from `~/.glaude/prompts/my_custom_prompt.md`.

### Custom Agent Configurations

You can create custom agent configurations for specific use cases (e.g., red-teaming, specialized tasks) by adding agent-specific TOML files in the `~/.glaude/agents/` directory.

To use a custom agent, run Glaude with the `--agent` flag:

```bash
glaude --agent my_custom_agent
```

Le Glaude will look for a file named `my_custom_agent.toml` in the agents directory and apply its configuration.

Example custom agent configuration (`~/.glaude/agents/redteam.toml`):

```toml
# Custom agent configuration for red-teaming
active_model = "Gros Choux Bio (devstral-2)"
system_prompt_id = "redteam"

# Disable some tools for this agent
disabled_tools = ["search_replace", "write_file"]

# Override tool permissions for this agent
[tools.bash]
permission = "always"

[tools.read_file]
permission = "always"
```

Note: this implies that you have setup a redteam prompt named `~/.glaude/prompts/redteam.md`

### MCP Server Configuration

You can configure MCP (Model Context Protocol) servers to extend Le Glaude's capabilities. Add MCP server configurations under the `mcp_servers` section:

```toml
# Example MCP server configurations
[[mcp_servers]]
name = "my_http_server"
transport = "http"
url = "http://localhost:8000"
headers = { "Authorization" = "Bearer my_token" }
api_key_env = "MY_API_KEY_ENV_VAR"
api_key_header = "Authorization"
api_key_format = "Bearer {token}"

[[mcp_servers]]
name = "my_streamable_server"
transport = "streamable-http"
url = "http://localhost:8001"
headers = { "X-API-Key" = "my_api_key" }

[[mcp_servers]]
name = "fetch_server"
transport = "stdio"
command = "uvx"
args = ["mcp-server-fetch"]
```

Supported transports:

- `http`: Standard HTTP transport
- `streamable-http`: HTTP transport with streaming support
- `stdio`: Standard input/output transport (for local processes)

Key fields:

- `name`: A short alias for the server (used in tool names)
- `transport`: The transport type
- `url`: Base URL for HTTP transports
- `headers`: Additional HTTP headers
- `api_key_env`: Environment variable containing the API key
- `command`: Command to run for stdio transport
- `args`: Additional arguments for stdio transport

MCP tools are named using the pattern `{server_name}_{tool_name}` and can be configured with permissions like built-in tools:

```toml
# Configure permissions for specific MCP tools
[tools.fetch_server_get]
permission = "always"

[tools.my_http_server_query]
permission = "ask"
```

### Enable/disable tools with patterns

You can control which tools are active using `enabled_tools` and `disabled_tools`.
These fields support exact names, glob patterns, and regular expressions.

Examples:

```toml
# Only enable tools that start with "serena_" (glob)
enabled_tools = ["serena_*"]

# Regex (prefix with re:) — matches full tool name (case-insensitive)
enabled_tools = ["re:^serena_.*$"]

# Heuristic regex support (patterns like `serena.*` are treated as regex)
enabled_tools = ["serena.*"]

# Disable a group with glob; everything else stays enabled
disabled_tools = ["mcp_*", "grep"]
```

Notes:

- MCP tool names use underscores, e.g., `serena_list` not `serena.list`.
- Regex patterns are matched against the full tool name using fullmatch.

### Custom Glaude Home Directory

By default, Le Glaude stores its configuration in `~/.glaude/`. You can override this by setting the `GLAUDE_HOME` environment variable:

```bash
export GLAUDE_HOME="/path/to/custom/glaude/home"
```

This affects where Le Glaude looks for:

- `config.toml` - Main configuration
- `.env` - API keys
- `agents/` - Custom agent configurations
- `prompts/` - Custom system prompts
- `tools/` - Custom tools
- `logs/` - Session logsRetryTo run code, enable code execution and file creation in Settings > Capabilities.

## Editors/IDEs

Le Glaude can be used in text editors and IDEs that support [Agent Client Protocol](https://agentclientprotocol.com/overview/clients). See the [ACP Setup documentation](docs/acp-setup.md) for setup instructions for various editors and IDEs.

## Resources

- [CHANGELOG](CHANGELOG.md) - See what's new in each version
- [CONTRIBUTING](CONTRIBUTING.md) - Guidelines for feedback and bug reports

## License

Copyright 2025 Mistral AI
Copyright 2026 Le Glaude - Romain Hardouin

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the [LICENSE](LICENSE) file for the full license text.
