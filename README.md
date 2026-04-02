# Smalltown Boost

3-layer architecture for reliable, repeatable operations.

## Architecture

### Layer 1: Directives (What to do)
- **Location**: `directives/`
- Living documentation of procedures and SOPs
- Written in Markdown
- Define goals, inputs, tools, outputs, and edge cases

### Layer 2: Orchestration (Decision making)
- **Your agent** - intelligent routing and decision-making
- Reads directives, calls execution tools in the right order
- Handles errors, asks for clarification
- Updates directives with learnings

### Layer 3: Execution (Doing the work)
- **Location**: `execution/`
- Deterministic Python scripts
- API calls, data processing, file operations, database interactions
- Reliable, testable, fast

## Directory Structure

```
.
├── directives/          # SOPs and instructions
├── execution/           # Python scripts (deterministic tools)
├── .tmp/               # Intermediate files (generated, never committed)
├── .env                # Environment variables (secrets, not committed)
├── .env.template       # Template for .env
└── .gitignore          # Git ignore rules
```

## Getting Started

1. **Set up environment variables**: Copy `.env.template` to `.env` and fill in your values
2. **Create a directive**: Add an SOP in `directives/` describing what you want to accomplish
3. **Implement execution scripts**: Add Python scripts in `execution/` to do the work
4. **Test**: Run scripts with test inputs
5. **Iterate**: Fix issues, update directives, test again

## Key Principles

- **Check for tools first**: Before writing a script, check if one exists
- **Self-anneal when things break**: Fix scripts, test, update directives
- **Deliverables in cloud**: Google Sheets, Slides, etc. (not local files)
- **Intermediates in .tmp/**: All temporary files go here

## Philosophy

LLMs are probabilistic, business logic is deterministic. This architecture fixes that mismatch by:
- Pushing complexity into reliable, tested code
- Using natural language for decision-making, not execution
- Continuously improving the system through feedback loops
