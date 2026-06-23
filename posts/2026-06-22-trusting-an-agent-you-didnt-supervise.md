---
title: How I trust an agent I didn't supervise
date: 2026-06-22
author: Peter Johnston
tags: claude code, agents, verification, code review, llm, workflow, architecture
description: "A few days ago I wrote up the architecture of the agent system I run my day job on. The obvious follow-up question — the one I kept getting and kept asking myself — is the uncomfortable one: if an agent writes a letter to a customer or a change to production and you don't read it line by line, why do you trust it? This is the verification doctrine that answers that."
---

A few days ago I wrote up [the architecture of the agent system I run my day job
on](/posts/2026-06-16-running-my-day-job-on-claude-code.html) — where state lives,
how it gets written, how the work splits across agents. That post ended on a line I
believe: the agents are the cleverest part of the setup and the least important.
The scaffolding is what makes it trustworthy.

But "trustworthy" was doing a lot of quiet work in that sentence, and a few people
called me on it. Here is the uncomfortable version of the question. An agent writes
a letter that goes to a customer. Another writes a code change that lands on the
website behind the whole operation. If the point of the system is that I'm *not*
reading every letter and every diff line by line — and if I were, I'd have saved no
time at all — then why do I trust any of it?

That's a fair question and the honest answer isn't "the model is good." The model
is good and also confidently wrong often enough that "it's good" is not a plan.
The answer is a *process*, and the process is the subject of this post. None of it
is clever. All of it is about putting the right kind of doubt in the right place.

## The thing you can't do is the thing that doesn't scale

Start from the trap. The instinct, when an agent hands you work, is to read it
carefully. And you should — the first ten times, while you're calibrating. But
careful reading is exactly the cost you were trying to remove. If every generated
letter needs a full proofread and every code change needs a line-by-line review
from me, the agent is a very expensive way to produce a first draft that I then do
the real work on. At volume, *I* become the bottleneck, and a bottleneck that gets
tired and skims at 6pm is worse than no bottleneck at all.

So the goal can't be "I verify everything." The goal has to be: build a process
that earns the right to *not* read a given piece of output, and reserve my
attention for the cases the process flags. Everything below is in service of that
one shift — moving the verification off my desk and into the system, without
moving it onto the same agent that did the work.

That last clause is the whole game.

## The author is the worst reviewer of its own work

The single most important rule is the one that sounds like bureaucracy: **the agent
that produces a piece of work never signs off on it.** Verification is always a
*different* agent.

This isn't process for its own sake. An LLM reviewing its own output is the worst
possible reviewer of it, for the same reason a writer can't proofread their own
draft an hour after writing it. It shares all the context that produced the
mistake. It has already convinced itself the approach is right — that's why it
wrote it that way. Ask the same agent "is this correct?" and the warm context that
generated the bug is the very thing now grading it. You get a confident yes, in the
same voice, for the same wrong reasons.

So in my setup the builder and the verifier are structurally separate agents with
*separate contexts*. The agent that writes a code change hands a branch to a
different agent whose entire job is to review it — and that reviewer comes in cold,
sees only the diff and the requirement, and has none of the author's investment in
the approach being right. The agent that generates a customer document is followed
by a readiness audit that checks the result against the source facts, not against
the generator's reasoning. Fresh eyes, fresh context, no skin in the game.

I gave these agents names and personalities to keep them straight in my head, but
the role is what matters: *builder*, *verifier*, *gate*. The flow looks like this —
and as on every post here, the diagram is compiled from its TikZ source at build
time, not pasted in as an image:

```tikzpicture
\begin{tikzpicture}[
  font=\small,
  >={Stealth[length=2.4mm]},
  box/.style={draw, rounded corners=2pt, align=center, minimum height=13mm, thick},
  build/.style={box, fill=blue!8, draw=blue!55!black, minimum width=26mm},
  verify/.style={box, fill=violet!10, draw=violet!60!black, minimum width=27mm},
  gate/.style={box, fill=orange!13, draw=orange!72!black, minimum width=24mm},
  world/.style={box, fill=green!10, draw=green!55!black, minimum width=27mm},
  flow/.style={->, thick, black!75},
  bounce/.style={->, thick, red!58!black, dashed},
  lbl/.style={font=\scriptsize, align=center},
]
  \node[build]  (b) at (0,0)    {Builder\\[-1pt]{\scriptsize writes the work}};
  \node[verify] (v) at (4.8,0)  {Verifier\\[-1pt]{\scriptsize fresh context,}\\[-1pt]{\scriptsize tries to refute}};
  \node[gate]   (g) at (9.6,0)  {Gate\\[-1pt]{\scriptsize fixed checklist}};
  \node[world]  (w) at (14.0,0) {Out\\[-1pt]{\scriptsize customer \(\cdot\) main \(\cdot\) prod}};

  \draw[flow] (b) -- node[lbl,above]{draft} (v);
  \draw[flow] (v) -- node[lbl,above]{survives} (g);
  \draw[flow] (g) -- node[lbl,above]{clears} (w);

  \draw[bounce] (v) to[bend right=22] node[lbl,below,pos=0.5]{refuted \(\rightarrow\) fix} (b);
  \draw[bounce] (g) to[bend right=32] node[lbl,below,pos=0.5]{bounced \(\rightarrow\) fix} (b);
\end{tikzpicture}
```

The dashed arrows are the part that earns the trust. Work doesn't flow one way and
out the door; it bounces back. A verifier that refutes the change sends it back to
the builder with specifics. A gate that catches a problem bounces it too. Nothing
reaches the right-hand box on its first pass by default — it reaches there by
*surviving*.

## Verification is adversarial, or it's theater

Separating the reviewer from the author buys you nothing if you then tell the
reviewer "check this over." A reviewer asked to confirm will confirm. It reads the
work, the work looks plausible — LLM output almost always looks plausible, that's
the entire problem — and it nods. You've added a step and no safety.

The fix is a framing flip that costs nothing and changes everything: **the verifier's
job is to refute, not to confirm.** It's told to assume the work is wrong until it
fails to break it. Default verdict: rejected. Find the bug, find the line item that
doesn't match the source, find the case where this 500s in production — and only if
you genuinely can't, pass it. A skeptic told "tear this apart" finds things a
proofreader told "look it over" sails straight past, and they are the *same model*
on the *same diff*. The only difference is which way the burden of proof points.

For the work where being wrong is expensive, I push this further into a small panel:
several independent verifiers, each coming at it from a different angle — does it
reproduce, is it correct, does it hold up under the domain's hard rules — and the
change only survives if it survives a *majority* of them. Redundant skeptics catch
different failure modes than one skeptic looking harder. It's more tokens. It's
worth it precisely where it's worth it, which brings up the next point.

## The gate is a checklist, not a judgment

Adversarial review is good at "is this *right*." It's unreliable at "did we forget
the boring thing that breaks production." Those are different failures and they need
different instruments.

So the last step before anything irreversible is a *gate*, and the gate is
deliberately dumb. It runs a fixed checklist, the same way, every time. For a code
change: does the build pass, do the tests pass, does the linter pass — on the merged
result, not the branch in isolation — and then a standing list of the specific
landmines I've been bitten by before. The env var that has to be wired in four
places or the deploy succeeds and then 500s. The migration that has to land before
the code that reads the new field. None of that is a judgment call, which is exactly
why it belongs in a checklist and not in an agent's discretion. A checklist run
identically a hundred times will catch the thing a tired reviewer skims past on the
hundred-and-first.

This mirrors the [single write-gate from the architecture
post](/posts/2026-06-16-running-my-day-job-on-claude-code.html): put the strictness
where the intelligence isn't. The verifier is smart and adversarial and a little
different every run. The gate is rigid and identical and unimpressed. You want both,
and you want them to be different things.

## Match the rigor to the cost of being wrong

If every piece of work went through a refute panel and a full gate, I'd have rebuilt
the bottleneck somewhere else — in tokens and latency instead of my attention. So
verification is *tiered*, and the tier is set by one question: how bad is it if this
is wrong, and how hard is it to undo?

- **Cheap and reversible** — a draft I'm going to read anyway, a throwaway analysis,
  an edit to a scratch file — gets a light check or none. Reversible work doesn't
  need a tribunal.
- **Outward-facing or irreversible** — a letter going to a customer, a change merging
  to the main branch, anything touching production — gets the full sequence: fresh-eyes
  refutation, then the gate, then a human seam if there's any ambiguity left.

The triggers are the boundaries where something leaves my control: the moment a
document gets sent, the moment code lands where users hit it, the moment a number
gets committed that other people will rely on. Up to that line, the cost of a
mistake is a re-run. Past it, the cost is a phone call to apologize, or a customer
reading something with their name spelled wrong. The rigor follows the
irreversibility, not the size of the task.

## Verification isn't free, so don't re-pay for it

A thing I got wrong early: treating each review as a fresh spawn. When a verifier
bounces a change and the builder fixes it, the natural-looking move is to spin up a
*new* verifier to check the fix. Don't. That new agent comes in cold, re-reads the
entire change from scratch, and re-derives everything it already established the
first time — you pay full price for a delta the size of a few lines.

The cheaper and better move is to continue the *same* verifier, which still has the
context from round one and only has to look at what changed. A delta review on a
warm context. The principle generalizes: spin up real parallel machinery — multiple
agents talking to each other — only for the contained bursts that genuinely need it,
like a tight bounce-fix-recheck loop on a hot change. The rest of the time, a
sequential hand-off is cheaper and just as safe. Verification you can't afford to run
is verification you'll skip, and skipped verification is the whole failure mode.

## What this looks like when I run it by hand

I've described this as if it were all wired together, and a lot of it is. But the
honest truth is that the core loop is something I still run manually, across two open
sessions — and the manual version is where the doctrine came from. I automated what
I'd already been doing with my hands.

It goes like this. I make a change in one session. Then I open a *second* session,
point it at the recent changes, and tell it to be a critic: review this, find the
flaws, assume I got something wrong. I ask that reviewer to write its findings to a
`.md` file — not to tell me in chat, but to produce a written report. The first
session then reads that file and implements the fixes against it. Then I go back to
the *second* session — still warm, still holding everything it found — and ask the
question that closes the loop: were all of these actually resolved?

Two details in there matter more than they look.

The first is the **`.md` file as the hand-off.** The reviewer and the fixer are
different sessions that can't talk to each other directly, so the findings report is
the contract between them. Because it's a written artifact and not a chat message, it
survives, I can read it myself, and the fixer works against a fixed list instead of a
vibe. It's the same instinct as everything else here — make the important thing a
durable object, not a conversation.

The second is **going back to the reviewer that's still warm** instead of opening a
third session to re-check. The session that found the problems only has to confirm a
small delta, and it already knows what to look for — the warm delta re-review from a
few paragraphs up, except here *I'm* the message bus, carrying the fix notice from the
builder back to the critic by hand.

When the change is bigger, this spreads out across time and devices. I'll cut the
findings into `gh` issues, push a branch, and juggle the back-and-forth from the
Claude Code app on my phone — fix in one thread, re-review in another, in the gaps
between other things. And the capstone is a fresh pass: cut the PR, then hand the
*whole* PR to a brand-new session that never saw any of the iteration and ask it to
review cold. Warm re-review is the right tool for confirming a specific fix; a cold
read of the finished whole catches what the warm thread had already talked itself
into accepting. It's iteration of iteration — and then the part no agent does for me.

## Where the human is still the gate

None of this removes me; it relocates me. I no longer sit in the path of every
letter and every diff. I sit at the places a checklist and a skeptic can't cover:

- **Taste and intent.** "Is this correct" is verifiable. "Is this the right thing to
  build at all," "is this the right tone for this customer," "are we even solving the
  real problem" — those aren't refutable claims, they're judgment, and they stay
  mine.
- **Irreversible *and* ambiguous.** When something is both hard to undo and not
  clear-cut, every layer above is designed to *stop and ask* rather than resolve it.
  That's not a limitation I'm tolerating; it's the point. A system tuned to surface
  the genuinely uncertain cases — and to handle the certain ones without me — is one
  that spends my attention where it's actually worth something.
- **Live behavior.** The gate proves the build is green and the tests pass; it can't
  prove the thing actually *works* when I click through it. The last step before I
  believe a change is me running it for real. Every layer above raises my confidence
  on paper; live testing is the only one that touches the running thing, and nothing
  substitutes for it.

So I read maybe one document in ten now, and they're the ten percent the system
flagged or the ones where the stakes told me to look anyway. The other nine I trust —
not because I checked them, but because something that wasn't their author tried to
break them and couldn't.

## The meta-lesson

The architecture post's lesson was that the scaffolding matters more than the
intelligence. This is the same lesson aimed at trust specifically: **you don't trust
an agent because it's smart, you trust a process that assumes it isn't.** The agent
that builds is optimistic by construction — it just convinced itself this was right.
Everything downstream of it is built to be pessimistic on purpose: a reviewer that
starts from "this is wrong," a gate that starts from "this will break prod," a human
who starts from "is this even the right thing." The intelligence proposes. The doubt,
arranged carefully and kept away from the thing it's doubting, is what lets you walk
away from the output without reading it.
