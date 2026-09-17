---
name: just-cmd
description: >-
  Execute registered custom tools, tasks, and system gateways. When the user asks for any tool, task, 
  or automated action, always run `just-cmd --list` first to discover available recipes.
metadata:
  hermes:
    tags: [just-cmd, tools, cli, justfile, runner, gateway]
  source: dan88c/just-cmd
  protocol: "1.00"
---

# just-cmd

Dispatcher for pre-registered custom tools, tasks, and gateways.

## Context Resolution

Resolve the working directory dynamically before preparing payloads or reading files:
```powershell
$workDir = (just-cmd path).Trim()

```

---

## Registration Protocol (Draft-Only)

New recipes are registered inside the working directory's `justfile` and are strictly edited by the employer, NEVER directly modified by the agent.

When asked to register a new recipe or a new tool:

1. Inspect the target script and identify its required working directory (`workdir`).
2. Draft the recipe format:
```just
# <Description>
<recipe-name> payload="<default_payload_path>":
    Set-Location "<workdir>"; & {{python_bin}} <script_path> {{payload}}

```

3. Output the draft recipe in a code block for the employer to add.
4. STOP and await employer confirmation. DO NOT write or append to `justfile` directly.

---

## Execution Protocol

1. **Recipe/Tool Discovery:**
* Run `just-cmd --list` to inspect available recipes and descriptions.
* Match the employer request against recipe names and comments.

2. **Prepare Payload:**
* Resolve working directory:
```powershell
$workDir = (just-cmd path).Trim()
```

* Write payload JSON to `$workDir\tmp_payload.json` (UTF-8, no BOM).

3. **Execute:**
```powershell
just-cmd <recipe-name> "$workDir\tmp_payload.json"

```
