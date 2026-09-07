# compliance-judge.md — layer 2 of the eval (the one binary call)

`checks.py` verifies everything mechanical: coverage, valid severity, that every citation resolves to a provision that exists in `reference/`, that FLAG/FAIL findings name an open decision, and that the header counts are honest. It cannot verify the one thing that needs judgment:

> **Does the cited provision actually support the finding's classification?**

A citation can resolve (the provision exists) and still be the wrong provision, or support a different class than the one assigned. That call is made here, by a human or by an agent loaded with this file, on a short sample, not on every line. This is Torres's rule for an LLM-as-judge: one simple binary task, aligned with your own judgment.

## The question

For a sampled finding, read three things: the dossier quote, the cited provision text in `reference/`, and the assigned class. Then answer one question:

> Given the provision text, is the assigned class (**CLEAR PASS / NARROW FLAG / CLEAR FAIL**) the correct one for what the dossier quote shows?

- **Supported** (pass the judge): the provision says what the finding says it says, and the class follows the severity rule in `rules.md`:
  - CLEAR FAIL only where the dossier quote contradicts a mandatory element of the cited provision.
  - CLEAR PASS only where the dossier quote explicitly satisfies it.
  - NARROW FLAG where the dossier is silent, ambiguous, or partial on it.
- **Not supported** (fail the judge): wrong provision for the point; or the class is too strong (FAIL asserted without a quotable contradiction) or too weak (silence marked PASS).

If not supported, name the fix: the right provision, or the right class, or the dossier evidence that is actually missing.

## The test that keeps the judge honest

The failure this auditor most needs to avoid is the one the DSK itself warns about: a rigid automated judgment on ambiguous text. So the sharp test is:

> Read the dossier quote alone. Could a reasonable DSB read it the other way? If yes, the honest class is **NARROW FLAG**, and a CLEAR FAIL or CLEAR PASS on that same quote is **not supported**.

Silence is the trap in both directions. "The vendor says data is secure" does not *satisfy* the training-exclusion provision (so not a PASS) and does not *contradict* it (so not a FAIL). It is silent. NARROW FLAG.

## Worked calls

| Finding (dossier quote → cited provision → class) | Call | Why |
|---|---|---|
| "AutoDecide entscheidet vollautomatisch, kein Freigabeschritt" → `[DSGVO-Art22-1]` → CLEAR FAIL | **supported** | Art. 22(1) forbids solely automated decisions with legal effect; the quote is a direct contradiction, and DSK 1.6 gives the same example as a Verstoß. |
| "Daten werden sicher und vertraulich verarbeitet" → `[DSK-OH-1.9]` → NARROW FLAG | **supported** | 1.9 asks for an explicit training exclusion; a generic security claim is silent on it, which is exactly a gap, not a violation. |
| "Daten werden sicher verarbeitet" → `[DSK-OH-1.9]` → CLEAR FAIL | **not supported** | class too strong: nothing in the quote contradicts the provision; downgrade to NARROW FLAG. |
| "AVV nach Art. 28 liegt vor, Unterauftragnehmer auf Anfrage" → `[DSGVO-Art28-2]` → CLEAR PASS | **not supported** | class too strong: 28(2) presumes the list is disclosed with change-notification; "auf Anfrage" leaves it unshown. NARROW FLAG. |

## How to run it

Take the report and its `checks.py` output. Sample the findings (at minimum: every CLEAR FAIL, and one NARROW FLAG and one CLEAR PASS at random). For each, open the cited provision in `reference/`, apply the question, record supported / not-supported and the fix. The decision to change the report stays human, like every gate in this system.
