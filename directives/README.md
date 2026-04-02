# Directives (SOPs)

This directory contains Standard Operating Procedures written in Markdown that define:
- **Goals**: What we're trying to accomplish
- **Inputs**: What information/data is needed
- **Tools/Scripts**: Which execution scripts to use
- **Outputs**: What the expected result is
- **Edge Cases**: Known limitations and special conditions

## Structure

Each directive is a self-contained SOP:

```markdown
# Directive Name

## Goal
What this procedure accomplishes

## Inputs
- Required data or parameters

## Process
Steps and decision points

## Tools/Scripts
- `execution/script_name.py` - What it does

## Outputs
Where results go and what format

## Edge Cases
Known limitations or special handling
```

## Updating Directives

When you discover API constraints, better approaches, or edge cases:
1. Fix the script
2. Test it
3. Update this directive with learnings
4. System is now stronger for next time
