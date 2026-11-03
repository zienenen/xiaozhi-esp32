# Codex Skills

This directory contains reusable Codex skills maintained with the project.

## Install On Another Windows Device

After cloning this repository, copy the skill into the local Codex skills
directory:

```powershell
$source = Resolve-Path ".\codex-skills\software-project-lifecycle-copilot"
$destination = Join-Path $env:USERPROFILE ".codex\skills\software-project-lifecycle-copilot"
New-Item -ItemType Directory -Path $destination -Force | Out-Null
Get-ChildItem -LiteralPath $source | Copy-Item -Destination $destination -Recurse -Force
```

The same command updates an existing installation in place. Restart Codex after
installation. The skill can then be invoked explicitly as:

```text
$software-project-lifecycle-copilot
```

It also remains available for automatic selection when a task involves project
startup, lifecycle coordination, role boundaries, quality gates, or handoff.
