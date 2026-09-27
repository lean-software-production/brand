---
name: listen
description: Use when asked to listen, catch up, or do what was just said out loud - reads the room's recent voice transcript and acts on the instruction in it
---

# Listen

Read what the room has said and do it. They are talking faster than they
can type; this is how a spoken instruction reaches you.

## Run It

```sh
.claude/skills/listen/scripts/recent-transcript      # since the last run
.claude/skills/listen/scripts/recent-transcript 15   # last 15 minutes
```

With no argument it resumes from where the previous run stopped, so
consecutive calls cover every word said while you were working. Pass
minutes to override.

## Read All Of It

A window that starts mid-sentence has cut something off, and what it cuts
off is usually the beginning of the topic — where the decision was made.
Widen until you can see the discussion start.

**Before acting, re-read for these. They are the ones that get missed:**

- **Deletions.** "I don't value that", "I'd rather that went away", "drop
  it." Removing something you already wrote is as much an instruction as
  adding something, and it is easy to skim past agreement.
- **Answers to your own questions.** Fold them in; do not re-ask.
- **Held-back ideas.** "Not yet", "too sophisticated for now", "next
  iteration." A deferral is a decision. Record it, do not build it.
- **Open questions they left open.** Do not close them by picking one.
  Say they are still open.

Speech-to-text is lossy: expect mangled jargon and read through it.
"Rough loop", "route loop" and "Ralph loop" are the same thing.

## Act On It

1. Take the decision they landed on, not the options they explored on the
   way. Discarded ideas sound identical to chosen ones in a transcript.
2. Say in one line what you heard before you do it, so a mishearing is
   caught cheaply.
3. Do it. Ask only if two readings would send you somewhere genuinely
   different.
4. Report what you heard but did **not** act on, and why. That is where a
   miss becomes visible.

If they were talking to each other and there is no instruction, say what
you heard and stop.
