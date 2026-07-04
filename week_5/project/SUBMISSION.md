# Research Desk/Code Scout – Week 5 Submission

## Overview

Week 5 presents the final version of the coding agent that I have been building throughout the five-week course. The Week 4 version already supported conversations with an LLM, maintained conversation history, and could use tools such as command execution, file operations, web search, paper search, and a todo system to complete coding tasks.

For Week 5, my goal was not simply to add more tools, but to make the agent **extendable**. Instead of requiring code changes every time I wanted to add new functionality, I implemented two extension mechanisms:

- **Skills**, which allow the agent to learn new workflows by simply adding a new `SKILL.md` file to the `skills/` directory.
- **Model Context Protocol (MCP)** support, which allows the agent to connect to external tool servers maintained by other developers instead of shipping every tool inside the agent itself.

I also added several quality-of-life improvements, including agent status and help commands, making it easier to inspect the currently available capabilities.

The result is an agent that is significantly more modular than the Week 4 version. New skills can be added without modifying Python code, and entirely new categories of tools can be integrated through MCP by editing configuration instead of rewriting the agent.
## Features Added in Week 5

### 1. Skills System

The biggest architectural change in Week 5 was adding support for **Skills**. Instead of hardcoding workflows directly into the agent, skills are stored as markdown files inside the `skills/` directory. Each skill contains metadata and instructions describing when and how it should be used.

To support this, I implemented:

- `load_all_skills()` to automatically discover every available skill.
- `load_skill()` to retrieve the contents of a specific skill on demand.
- A `skills/` directory that can be extended without modifying the agent itself.

This means that adding a new skill no longer requires editing Python code. A user only needs to create another folder containing a `SKILL.md` file, and the agent automatically discovers it the next time it starts.

As examples, I implemented two skills:

- **commit** – guides the agent through creating safe, high-quality Git commits while encouraging tests before committing.
- **review** – provides a structured checklist for reviewing code before it is committed or merged.

These skills demonstrate how procedural knowledge can be added to the agent independently of its source code.

---

### 2. Model Context Protocol (MCP)

The second major addition was support for the **Model Context Protocol (MCP)**.

Rather than writing GitHub functionality directly into the agent, I implemented a generic MCP interface capable of connecting to external MCP servers. Server configuration is stored in `config.json`, while authentication is provided through environment variables, ensuring that no secrets are committed to the repository.

The implementation consists of:

- an MCP configuration loader,
- an MCP client responsible for connecting to servers,
- a generic `mcp_call` tool that allows the agent to invoke any tool exposed by a configured MCP server.

For demonstration, I connected the agent to the **GitHub MCP server**, allowing it to perform tasks such as searching repositories, reading pull requests, listing issues, and using many other GitHub tools without implementing each feature manually.

One important design decision was making MCP tool invocation generic. Instead of creating one Python function per GitHub operation, the agent exposes a single `mcp_call` interface capable of executing any tool advertised by the server. This makes the implementation easily extensible to future MCP servers.

---

### 3. User Experience Improvements

To make the agent easier to inspect and use, I added two REPL commands:

- `/help` – displays the available interactive commands.
- `/status` – shows the currently loaded skills, configured MCP servers, and the major capabilities available in the agent.

These commands make it easier for a user to understand what the agent can currently do without inspecting the source code.
## Testing

I tested every major feature individually before integrating it into the main agent. This made it much easier to isolate bugs and verify that each component worked correctly before building on top of it.

### Skills

The Skills system was tested in several stages:

- Verified that `load_all_skills()` correctly discovered every skill inside the `skills/` directory.
- Verified that `load_skill()` successfully loaded the contents of an individual `SKILL.md` file.
- Confirmed that adding a new skill required no code changes and that it was automatically detected by the loader.
- Tested the agent's ability to retrieve and use the loaded skill when requested.

Both the `commit` and `review` skills were successfully detected and loaded.

### MCP

The MCP implementation was also tested incrementally.

First, I tested the configuration system by verifying that:

- `config.json` was loaded correctly.
- Environment variables were substituted correctly from `.env`.
- The GitHub Personal Access Token was successfully passed to the GitHub MCP server.

Next, I created a standalone test client that verified:

- Connection to the GitHub MCP server.
- Session initialization.
- Discovery of all available GitHub tools.
- Successful execution of MCP tool calls.

Finally, I integrated MCP into the main agent through the generic `mcp_call` tool and verified that the agent itself could invoke GitHub tools.

One end-to-end test was:

```
Use the mcp_call tool to search GitHub repositories for modelcontextprotocol/python-sdk.
```

The agent successfully:

1. Connected to the GitHub MCP server.
2. Discovered the available GitHub tools.
3. Executed the `search_repositories` tool.
4. Retrieved repository information.
5. Summarized the results into a natural-language response.

### User Interface

The additional REPL commands were tested manually.

- `/help` correctly displayed the available interactive commands.
- `/status` correctly displayed the loaded skills, configured MCP servers, and major capabilities of the agent.

Throughout development, I intentionally left diagnostic output such as discovered MCP tools visible because it provides clear evidence that the server connection and tool discovery process completed successfully. This made debugging easier during development and also demonstrates the internal workflow of the agent during testing.
## Cool Feature Demonstration

The most significant new capability added in Week 5 is support for **Model Context Protocol (MCP)**. Instead of implementing GitHub functionality directly inside the agent, the agent can dynamically connect to an external MCP server and use the tools that server provides.

For this project, I configured the GitHub MCP server.

### Task

Search GitHub for the official Python SDK for the Model Context Protocol.

### Requirements

Before running the agent, create a `.env` file containing:

```text
OPENROUTER_API_KEY=<your OpenRouter API key>
GITHUB_PAT=<your GitHub Personal Access Token>
SERPER_API_KEY=<optional, only required for web search>
```

The GitHub MCP server is configured inside `config.json`. No authentication credentials are stored in the repository.

### Steps

1. Install the project dependencies.

```bash
pip install -r requirements.txt
```

2. Start the agent.

```bash
python agent.py
```

3. Enter the following prompt.

```text
Use the mcp_call tool to search GitHub repositories for modelcontextprotocol/python-sdk.
```

### Expected Behaviour

The agent should:

1. Decide to invoke the `mcp_call` tool.
2. Connect to the GitHub MCP server.
3. Discover the available GitHub tools.
4. Execute the `search_repositories` MCP tool.
5. Retrieve information about the repository.
6. Produce a natural-language summary of the results.

During execution, the terminal also displays the discovered GitHub tools and the successful MCP connection, making it easy to verify that the MCP integration is functioning correctly.

This demonstration shows that the agent can extend its capabilities without modifying its own code. By connecting to an external MCP server, it gains access to dozens of GitHub operations that were never implemented directly inside the project.
## Challenges and Design Decisions

During development, I encountered several implementation challenges that required changes to my initial design.

### Skills

The Skills system itself was relatively straightforward, but I wanted it to be completely extensible. Instead of hardcoding available skills, I implemented automatic discovery through `load_all_skills()`. This means that adding a new skill only requires creating another folder containing a `SKILL.md` file, with no changes to the Python source code.

### MCP Package Name Conflict

One of the first issues I encountered during MCP integration was a namespace conflict. I had initially created my own package named `mcp`, but this conflicted with the official Python MCP SDK, which uses the same package name.

Python imported my local package instead of the SDK, causing import errors. I resolved this by renaming my implementation to `mcp_manager`, allowing both my code and the official SDK to coexist without conflicts.

### Authentication

Another important consideration was authentication. Rather than storing API keys inside the repository, I followed the configuration-as-code approach introduced in this week's lessons.

The GitHub Personal Access Token is loaded from environment variables through `.env`, while the MCP server configuration is stored separately in `config.json`. This keeps sensitive information out of source control and allows different users to configure the project using their own credentials.

### MCP Integration

My initial design attempted to keep a persistent connection to the GitHub MCP server for the entire lifetime of the agent. While this worked in isolated tests, it introduced issues because the agent itself is primarily synchronous while the MCP SDK uses asynchronous resource management.

To simplify the architecture, I redesigned the integration so that the agent establishes an MCP connection only when an MCP tool is invoked. The connection is created, the requested tool is executed, and the connection is then closed. This approach fits naturally into the existing tool-dispatch architecture while satisfying the project requirements.

Overall, these challenges reinforced the importance of modular design and separating configuration, communication, and application logic into independent components.
## Future Improvements

Although the agent is now significantly more capable than the Week 4 version, there are several improvements I would like to make in the future.

The first improvement would be support for multiple MCP servers running simultaneously. At the moment, the implementation is generic enough to support different servers through `config.json`, but I would like the agent to automatically discover, manage, and switch between multiple MCP servers without any additional user intervention.

I would also like to expand the Skills system by writing more practical skills for everyday development tasks. Examples include deployment checklists, release workflows, documentation generation, and project setup. Since the Skills framework is already in place, these additions would require little or no modification to the Python code.

Finally, I would like the agent to make even better decisions about when to use Skills versus MCP tools. At the moment, both extension mechanisms work independently, but a tighter integration could allow the agent to automatically select the most appropriate capability for a given task.

---

## Final Reflection

Looking back over the five weeks, the biggest change was not simply adding more features, but changing how the agent is designed.

In Week 1, the project consisted of a single API call. Over the following weeks it gradually evolved into a conversational assistant, then a coding agent capable of using tools, and finally an extensible platform that can gain entirely new capabilities without changing its core implementation.

The Skills system demonstrated how procedural knowledge can be added by writing markdown files instead of Python code. The MCP integration demonstrated how external tools maintained by other developers can be incorporated into the agent through a common protocol rather than being implemented from scratch.

The biggest lesson I learned during this project was the importance of modular design. Separating configuration, skills, tools, MCP communication, and the agent itself made development much easier and allowed new functionality to be added with minimal changes to the existing codebase.

Overall, I am satisfied with how the project evolved. The agent is considerably more capable than the Week 4 version while remaining modular, configurable, and straightforward to extend in the future. Thank you so much guys for conducting this wonderful track! :)
