# GTK Fitness — Course Creation System

This repository stores health & wellness courses built using a proven Educational Architecture.

## Skills

### `/course-creation [topic]`

Generates a complete course — outline + every lesson script — for a given health/wellness topic.

**Examples:**
```
/course-creation peptides
/course-creation gut health
/course-creation hormone health
/course-creation thyroid optimization
/course-creation metabolic health
```

**What it produces:**
- `courses/[topic]/00-course-outline.md` — full module and lesson map
- `courses/[topic]/module-0X-[name]/lesson-0X-X-[name].md` — one file per lesson with hook, core content, aha moment, action step, and key takeaways

## Educational Architecture

Every course follows the same 7-module arc:

| Module | Purpose |
|---|---|
| 0 — Wake-Up Call | Make the problem real; make the solution believable |
| 1 — Science Made Simple | Build foundational understanding without overwhelm |
| 2 — What Goes Wrong | Help students recognize themselves in the problem |
| 3 — Solution Framework | Evidence-based roadmap before any implementation |
| 4 — Implementation | Time-phased action across 3 phases (30/90/long-term) |
| 5 — Troubleshooting & Advanced | Handle stalls; reward students who go deeper |
| 6 — Long-Term Blueprint | Integrate into the bigger health picture |

Every lesson follows: **Hook → Core Content → Aha Moment → Action Step → Key Takeaways**

## Course Directory

Generated courses live in `courses/`:
```
courses/
  peptides/
    00-course-outline.md
    module-00-wake-up-call/
      lesson-00-1-the-problem-nobody-talks-about.md
      ...
    module-01-science-made-simple/
      ...
```
