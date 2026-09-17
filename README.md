# just-cmd

[![Powered by just](https://img.shields.io/badge/powered%20by-casey%2Fjust-black?logo=gnubash&logoColor=white)](https://github.com/casey/just)

> *"Using `just` with AI agents is a game changer — until your local 35B model reads 'just' as an adverb and starts hallucinating. `just-cmd` fixes that with a single hard link."*

---

### The Pain Points

Task runners like `just` should be the ideal execution layer for local AI agents. But when running compact models (Hermes on Qwen 35B, 12GB VRAM, hard 65k context) in multi-turn agent loops on Windows, things fall apart:

1. **Path Hallucination:** Verbose paths like `C:\Users\...\demo\system-sentinel\sentinel.py` eat ~180 tokens per turn. By round 5, the model mangles backslashes and fabricates CLI flags.
2. **Adverb Confusion:** The model frequently reads `just run a check` as natural English prose (*"I will just run a check..."*) rather than an executable CLI tool, narrating instead of calling. (See the detailed token breakdown in the [Devlog from the wallop PoC](https://github.com/dan88c/wallop-bare/blob/main/DEVLOG.md)).
3. **Over-Engineering Trap:** Writing a custom Go orchestrator works, but compiling and maintaining a custom binary just to keep an alias table outside context is overkill.

Aliasing `just` to `just-cmd` via an NTFS hard link eliminates prose confusion, cuts invocation cost to ~8 tokens, and requires zero custom code.

---

### 1. Setup the `just-cmd` Link

First, install [casey/just](https://github.com/casey/just#installation) via your preferred package manager (Winget, Scoop, Chocolatey, or Cargo).

Because package paths vary and change across releases, locate your `just.exe` dynamically and create the hard link in your user `PATH` (e.g., `~/bin` or `~/.local/bin`):

**CMD (Run Once):**
```cmd
for /f "tokens=*" %i in ('where.exe just') do @mklink /H "%USERPROFILE%\bin\just-cmd.exe" "%i"
```

**PowerShell (Run Once):**
```powershell
cmd /c "mklink /H `"$HOME\bin\just-cmd.exe`" `"$((Get-Command just).Source)`""
```

*(Alternatively, run `where.exe just` to find the current binary path, then manually run `mklink /H <dest> <src>`.)*

**Why this over a shell alias?**
* **Universal availability:** Works across `cmd.exe`, PowerShell, Python `subprocess`, and bare agent sub-shells.
* **No startup penalty:** Direct NTFS pointer to the binary with zero shell wrapper latency.
* **Distinct token identity:** Prevents the LLM from confusing the tool name with the English adverb "just".

---

### 2. Pin the `justfile` Globally (Persistent across Reboots)

By default, `just` searches the current working directory. When AI agents wander across folders, they lose track of the recipes. Pin the location globally:

**PowerShell (Recommended) (Run once in project root):**

```**PowerShell :**
[Environment]::SetEnvironmentVariable("JUST_JUSTFILE", "$PWD\justfile", "User")

```

**CMD (Run once in project root):**

```cmd
setx JUST_JUSTFILE "%CD%\justfile"

```

Now, the agent can call `just-cmd <recipe>` from any directory, sub-process, or shell without needing `--justfile` flags.

>"Note: This sets a global override. If you work across multiple projects with different justfiles, consider setting this per agent session instead of globally."

---

### 3. Recipes

Task recipes are defined in [`./justfile`](./justfile). They encapsulate working directory switching and multi-service executions behind short names:

| Recipe | Description |
| --- | --- |
| `just-cmd check` | List all available tasks (`just-cmd --list`). |
| `just-cmd path` | Output the absolute directory path of the active `justfile`. |
| `just-cmd demo-sentinel` | Run hardware metric inspection via System Sentinel. |
| `just-cmd demo-calendar` | Run Calendar Gateway integration task. |
| `just-cmd demo-openclaw` | Run OpenClaw web parsing pipeline. |
| `just-cmd demo-all` | Sequentially execute all demo pipelines. |

---

### 4. Agent Tool Definition

Complete agent protocol, tool metadata, and human-in-the-loop registration rules are defined in [`./just-cmd/SKILL.md`](./just-cmd/SKILL.md). Tested and verified on Windows OS only using my local Hermes agent workflows.

* **Tool / Skill:** `just-cmd` (Hermes protocol)
* **Execution Pattern:** Agent runs `just-cmd --list` to discover tasks dynamically, resolves context via `just-cmd path`, and triggers recipes with `just-cmd <recipe-name> [payload]`.
* **Guardrail:** The agent drafts new recipes for review, strictly preventing unauthorized edits to your `justfile`.

Calls resolve deterministically through the global link, keeping your context window lean.



The model emits `just-cmd demo-sentinel`, context consumption stays minimal (~8 tokens), and execution remains deterministic.

---

## Acknowledgements

Architected as an exploration into AI Agent tool execution layers. Implementation details, and commands were developed using AI-assisted pair scripting.