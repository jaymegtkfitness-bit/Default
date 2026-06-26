---
description: Create a complete health & wellness course following the proven Educational Architecture. Generates a full course outline then writes every lesson script. Usage: /course-creation [topic] — e.g. /course-creation peptides
---

You are building a health & wellness course on the topic: **$ARGUMENTS**

Work through the two phases below in order. Do not skip ahead to lesson scripts before the outline is complete and confirmed.

---

## PHASE 1 — COURSE OUTLINE

Create the file `courses/[topic-slug]/00-course-outline.md` with the following structure. Replace all bracketed placeholders with content specific to the topic.

```
# [Course Title: outcome-focused, not topic-focused]

## Transformation Promise
**Before**: [specific pain state the student is in right now]
**After**: [specific outcome they'll have after completing this course]

## Who This Is For
[2-3 sentences: the person, their situation, what they're struggling with]

## Who This Is NOT For
[1-2 sentences: set honest expectations]

## What You'll Need
[Tools, labs, or resources — keep it short, 3-5 bullets max]

## Estimated Time
[Total course hours, plus average lesson length]

---

## MODULE 0: YOUR WAKE-UP CALL
*Purpose: Make the problem real, make the solution believable, set up the system*

- **Lesson 0.1** — The Problem Nobody's Talking About
- **Lesson 0.2** — What's Actually Possible
- **Lesson 0.3** — How to Use This Course

## MODULE 1: THE SCIENCE MADE SIMPLE
*Purpose: Build foundational understanding without overwhelm*

- **Lesson 1.1** — What Is [Topic] and Why Does It Run Your Life?
- **Lesson 1.2** — How the System Works (Plain-English Mechanism)
- **Lesson 1.3** — The Key Players — Who Does What
- **Lesson 1.4** — Your Body's Feedback Loops — What Symptoms Are Telling You

## MODULE 2: WHAT GOES WRONG — AND WHY
*Purpose: Help students recognize themselves in the problem; eliminate myths*

- **Lesson 2.1** — Root Causes: What Disrupts This System in Modern Life
- **Lesson 2.2** — Are YOU Affected? Self-Assessment + Lab Markers to Request
- **Lesson 2.3** — The Big Myths (What Conventional Medicine Gets Wrong)
- **Lesson 2.4** — Hidden Disruptors: The Overlooked Factors That Sabotage Everything

## MODULE 3: THE SOLUTION FRAMEWORK
*Purpose: Give students a clear, evidence-based roadmap before any implementation*

- **Lesson 3.1** — The Hierarchy of Interventions (Lifestyle → Nutrition → Supplements → Clinical)
- **Lesson 3.2** — What the Research Actually Shows (No Hype)
- **Lesson 3.3** — Why One Size Doesn't Fit All — Finding Your Path
- **Lesson 3.4** — Building Your Protocol — The Decision Framework

## MODULE 4: IMPLEMENTATION
*Purpose: Translate knowledge into specific, time-phased action*

- **Lesson 4.1** — Phase 1 Foundation (Days 1–30): The Non-Negotiables
- **Lesson 4.2** — Phase 2 Optimization (Days 30–90): Layering In Interventions
- **Lesson 4.3** — Phase 3 Maintenance: What to Sustain Long-Term
- **Lesson 4.4** — Tracking and Measurement: What to Monitor and How Often
- **Lesson 4.5** — Your First 7 Days: The Quick-Start Action Plan

## MODULE 5: TROUBLESHOOTING & ADVANCED STRATEGIES
*Purpose: Handle the "it's not working" moment; reward students who want to go deeper*

- **Lesson 5.1** — When Results Stall: The Most Common Obstacles
- **Lesson 5.2** — Individual Variation: Why Your Response May Differ
- **Lesson 5.3** — When to Bring in a Practitioner (and What to Ask For)
- **Lesson 5.4** — Advanced Strategies: For Those Ready to Go Deeper

## MODULE 6: YOUR LONG-TERM HEALTH BLUEPRINT
*Purpose: Integrate the course into the student's broader health picture; create forward momentum*

- **Lesson 6.1** — Bringing It All Together
- **Lesson 6.2** — Your Long-Term Monitoring Schedule
- **Lesson 6.3** — What's Next: The Natural Next Step in Your Health Journey
- **Lesson 6.4** — Your 90-Day Action Plan (The Complete Roadmap)
```

Adapt lesson titles to be specific to the topic. Add a topic-relevant subtitle to each module that makes the arc feel coherent (e.g. for gut health: Module 1 might be "The Gut Is Your Second Brain — Here's Why That Matters"). You may add one extra lesson per module if the topic genuinely requires it; do not pad.

---

## PHASE 2 — LESSON SCRIPTS

After the outline file is written, write every lesson script. Create one file per lesson at:

`courses/[topic-slug]/module-0X-[module-slug]/lesson-0X-X-[lesson-slug].md`

Use this exact template for every lesson:

---

```markdown
# Lesson [X.X]: [Title]

**Module**: [Module Name]  
**Estimated Duration**: [X minutes]  
**Learning Objective**: By the end of this lesson you will be able to [one specific, testable thing].

---

## HOOK
*(30–60 seconds — open with a question, a provocative fact, or a story the target student lives)*

[Write the hook. Make it personal and specific. Do not start with "Welcome to lesson X."]

---

## CORE CONTENT

### [Key Point 1 Title]

[Explanation in plain language. Every complex concept gets at least one analogy grounded in everyday experience. Define clinical terms immediately when used. Keep paragraphs to 3 sentences max.]

### [Key Point 2 Title]

[Continue. Aim for 3–5 key points per lesson. Prefer depth on fewer points over breadth on many.]

### [Key Point 3 Title]

[Continue.]

*(Add Key Points 4–5 only if the topic genuinely requires them.)*

---

## THE AHA MOMENT

*The single reframe that changes how the student thinks about this forever:*

[Write the insight. This is not a summary — it's the moment things click. It often takes the form: "So the real reason [symptom/problem] happens is not [what people think] — it's [the underlying truth]."]

---

## YOUR ACTION STEP

*One concrete thing to do in the next 24 hours:*

[Specific, measurable action. Not "think about" or "consider" — something they can physically do or check off. Example: "Pull up your most recent bloodwork and locate your [marker]. Write it down alongside today's date."]

---

## KEY TAKEAWAYS

1. [Takeaway 1 — restate the most important concept from this lesson]
2. [Takeaway 2]
3. [Takeaway 3 — end with the one thing that sets up the next lesson]

---

*Next lesson: [X.X] — [Next Lesson Title]*
```

---

## WRITING STANDARDS (apply to every word you write)

**Voice**: Warm, direct, credible. Like a knowledgeable friend who did the research so the student doesn't have to. Not clinical. Not hype.

**Reading level**: 8th grade target. If a curious 14-year-old couldn't follow it, simplify.

**Analogies**: Mandatory for every complex biological mechanism. Ground abstract science in everyday objects or experiences (kitchens, plumbing, traffic, orchestras — whatever fits).

**Tone on risk**: Matter-of-fact. Never fear-mongering. Present consequences of dysfunction clearly, then pivot immediately to what the student can do about it.

**Evidence**: Reference research directionally ("A 2023 review found...", "Studies consistently show...") without burying students in citations. No academic hedging like "it may be possible that."

**Action bias**: Every lesson ends with something the student can DO, not just know. Knowledge without action is wasted.

**No filler**: Cut phrases like "In this lesson we'll explore..." or "Great question!" or "As we discussed earlier..." Start sentences with the idea, not a warm-up.

**Health/wellness specificity**: Assume the reader is health-conscious but not a clinician. Always define acronyms and clinical terms on first use. Spell out lab marker names before using abbreviations.

---

## DIRECTORY CONVENTIONS

| Item | Path |
|---|---|
| Course outline | `courses/[topic-slug]/00-course-outline.md` |
| Module folder | `courses/[topic-slug]/module-0X-[module-slug]/` |
| Lesson script | `courses/[topic-slug]/module-0X-[module-slug]/lesson-0X-X-[lesson-slug].md` |

Topic slug rules: lowercase, hyphens only, no special characters (e.g. "gut-health", "peptides", "hormone-health").

---

## EXECUTION ORDER

1. Write `00-course-outline.md` first. Output the full file.
2. Then write lesson scripts in order: Module 0 → Module 1 → ... → Module 6.
3. Write each lesson file completely before moving to the next.
4. After all files are written, print a summary table listing every file created.
