# Continuous Conversation Context Auto-Sync Protocol — DMIT Platform

## 1. Operating Principle
Every conversation turn with the user that introduces new product decisions, biometric scoring rules, design preferences, UI alterations, or bug resolutions must immediately sync to the living `memory-bank/` files. Never allow conversational context to evaporate across session resets or context compactions.

---

## 2. Synchronization Mapping
When any of the following occur during conversation, update the corresponding `memory-bank/` document immediately:

| Event / Information Type | Target File in `memory-bank/` |
| :--- | :--- |
| Active task focus, user priorities, immediate next steps | `activeContext.md` |
| Completed features, bug fixes, milestone completions | `progress.md` |
| Architectural decisions, Table 1.1 weightings, UI tokens | `systemPatterns.md` |
| Dependencies, ports, Python packages, Next.js configs | `techContext.md` |
| Target user personas, ethical guidelines, counselor flows | `productContext.md` |

---

## 3. Execution Discipline
- Keep updates concise, structured, and factual.
- Do not ask the user for permission to record their decisions in memory bank; update automatically as part of good operational hygiene.
