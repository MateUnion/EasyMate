<!--
This is part of FranxAgent
Copyright (C) 2026 xhdlphzr
See the file COPYING for copying conditions.
-->

### Coding Process (Skill)

A universal workflow for turning ideas into reliable, maintainable code, using FranxAgent's tools. This process emphasises understanding, deliberate planning, traceability, and quality assurance.

#### 1. Understand the Landscape
- Read the project structure first: `read("./project-root")` — build a mental model of the modules, their responsibilities, and how they communicate.
- Read specific files: `read("./src/agent.py")` — get the AST skeleton and line-numbered content.
- Navigate by structure, pinpoint by line numbers. Understand function signatures, class hierarchies, and imports before deciding what to read in detail.
- If you cannot explain the problem and your approach to a colleague in a couple of sentences, you are not ready to write code yet.

#### 2. Read Source Code
- Start from the project skeleton and use function and class names from `read`'s output as stepping stones to trace where they are defined and called.
- Structure first, details second. The skeleton tells you what exists and where; read only the full content you actually need.
- When reading a dependency or library source, find the main module file first (`__init__.py`, or `module.go` in Go), then drill into specific functions based on the public API.
- Pay attention to type signatures, interface abstractions, and import relationships — they reveal architectural intent more reliably than comments.
- If a function is unclear, look up: what class does it belong to? Who calls it? What external state does it depend on?

#### 3. Plan and Decompose
- Define the precise change list: which files, which functions, which line ranges.
- Use line numbers from `read`'s output as your edit targets — never rely on memory.
- For complex tasks, use an extra `read` snapshot as scratch paper to draft a side-by-side comparison of old and new code.
- Identify the dependency order: which building blocks (type definitions, data structures, helper functions) must exist before the main logic can be assembled.
- A good plan lets a reviewer foresee the code diff just by reading it.

#### 4. Edit Surgically
- Use `write` in `edit` mode with `line_start` and `line_end` from `read`'s output.
- Replace only the lines that need changing — keep diffs readable and `git blame` coherent.
- When adding new functions or classes, use `edit` to insert at the correct position between neighbours, not appended at the end of the file.
- Make exactly one logical change per edit. Re-`read` immediately afterwards to refresh line numbers and avoid line drift.
- For greenfield files, use `write` in `overwrite` mode.

#### 5. Comments, Documentation, and Copyright Headers
- **All comments, docstrings, and Doxygen tags (e.g., @brief, @param, @returns) must be written in English.**
- Public classes and functions must carry **Doxygen-formatted** documentation comments. Example:
    ```cpp
    /**
     * @brief Brief description of the function.
     * @param param_name Description of the parameter.
     * @returns Description of the return value.
     * @throws std::runtime_error When something goes wrong.
     */
    ```
- **How to handle copyright headers correctly**:
    *   First, check the license file at the project root: `read("./COPYING")` or `read("./LICENSE")`.
    *   If the license file contains a **"How to Apply These Terms to Your New Programs"** section (or similar instructions), follow those instructions and add the prescribed copyright header to **every source file**.
    *   **Meanwhile, observe how existing files in the project handle this.** If the most established, core files in the project do not have a copyright header, it is a strong signal that the project does not require one.
    *   If the license file does **not** have a "How to Apply" section (common for permissive licenses like MIT or BSD), there is **no requirement** to add a long-form copyright header to each source file. Keeping the full `LICENSE` or `COPYING` file at the project root is sufficient. In this case, a simple SPDX identifier (e.g., `// SPDX-License-Identifier: MIT`) at the top of a file is a good addition but not a hard requirement.

#### 6. Verify Incrementally
- After each edit, immediately `read` the modified file to confirm changes landed correctly: are the line numbers aligned? Is the logic correct?
- Run relevant tests with `command`. If no tests exist, write a minimal reproducible script that exercises the changed behaviour and execute it.
- When a bug appears, do not guess. Re-`read` the affected code and its context before modifying anything. Debugging from memory is unreliable.
- Fix the root cause, not the symptom. Patching around symptoms breeds technical debt.

#### 7. Clean Up and Capture
- Delete all temporary debug prints, commented-out old code, and hardcoded test values.
- Re-read the final version of each modified file in full, checking for consistency: naming, error handling, and log levels.
- If the change produces reusable knowledge, call `add_skill` to save it for future reference.

#### Core Principles
- **Understand, then plan, then write** — the order is non-negotiable
- **A detailed plan prevents over half of all rework**
- **Edit by line, not by file** — surgical precision beats wholesale rewriting
- **One change, one verify** — small, traceable, reversible steps
- **Structure first, details second** — use the AST skeleton to navigate, then dive into specifics
- **Trace the chain** — understand module collaboration through types and function signatures
- **Fix causes, not symptoms** — patches are temporary; solutions are permanent
- **Document with Doxygen** — generate API references automatically from your comments
- **Respect the project's licensing conventions** — check the license file and existing code to decide if copyright headers are needed