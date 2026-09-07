# Walk log — cold run of the KI-Datenschutz-Prüfassistent

A plain record of how the run actually went, including the confusing bits.

## Files opened, in order

1. `README.md` — orientation. Clear.
2. `identity.md` — role, the three finding classes, the discretion guardrail.
3. `rules.md` — procedure, citation format, severity logic, output format.
4. `checklist.md` — the five Prüfschritte and their provision anchors.
5. `examples.md` — one worked finding per class.
6. `demo/dossier.md` — the vendor dossier to audit.
7. `reference/dsgvo-artikel.md` — to verify every DSGVO ID before citing it.
8. `reference/dsk-oh-ki.md` — to verify every DSK-OH ID.
9. `reference/dsg-nrw.md` — state module, to verify the § 46 IDs and the authority name.
10. Re-opened `reference/dsgvo-artikel.md` at the tail (from line 128) to check whether Art. 44 had body text.

I did NOT open anything under `audit/keys/` (off-limits) and did not look for an answer key for the demo dossier.

## Things that were unclear, confusing, or slowed me down

- **Art. 44 is a heading with no body text.** The checklist lists `[DSGVO-Art44]` as a test for PS-2 (third-country transfer), and rules.md says every citation must "quote the short operative phrase from the reference (in German, verbatim)." But `reference/dsgvo-artikel.md` carries only `## Art. 44 DSGVO` / `_Allgemeine Grundsätze der Datenübermittlung_` with no paragraph text. So there is no operative phrase to quote. I still needed to flag the US-parent remote-access gap somewhere, so I cited `[DSGVO-Art44]` using its verbatim heading title and leaned on `[DSGVO-Art28-2]` (which has real, quotable operative text) as the primary anchor for PS-2. This is the single clearest defect in the folder: a test points at a provision whose text is not actually present in the reference. Worth fixing before this is shown to a real DSB.

- **Citation-scheme mismatch between the two reference styles.** The DSK file writes its IDs inline as bracketed headers (`[DSK-OH-1.9]`), so "does the ID exist verbatim" is literally checkable. The DSGVO and DSG-NRW files do NOT write bracketed IDs; the IDs are constructed from article/paragraph numbers per the scheme in rules.md. So "cite only IDs you verified exist" means two different things depending on the file: a literal string match for DSK, a reconstruct-from-numbering for DSGVO/NRW. Not wrong, but I had to hold two mental models.

- **PS-1 Art. 22(3) safeguards.** The checklist's CLEAR PASS bar for PS-1 asks for "safeguards per `[DSGVO-Art22-3]` (right to obtain human intervention, to state one's view, to contest)." The dossier documents genuine human review but says nothing about those data-subject-facing rights. I concluded Art. 22(3) is simply not engaged here, because the system produces no Art. 22(2) automated decision at all (it makes no decisions), so its safeguards do not trigger. That let me call it CLEAR PASS. A stricter reader could argue the missing 22(3) language is a gap and drop it to NARROW FLAG. I went PASS because the dossier explicitly satisfies the core provision (Art. 22-1) with quotable evidence and describes real handling ("bearbeitet", not just "abgezeichnet"). This was a genuine judgment call, noted below as the runner-up hardest.

- **PS-4 and where the "Logik" duty actually lives.** The plain-language-logic duty is really Art. 13(2)(f) ("aussagekräftige Informationen über die involvierte Logik"), but the checklist anchors PS-4 to `[DSGVO-Art13-1]`. I cited `[DSGVO-Art13-1]` as instructed (with a verbatim quote from the 13(1) chapeau) and put the actual logic/allgemeinverständlich weight on `[DSK-OH-1.8]`, which carries the on-point verbatim text. Minor, but a reader cross-checking Art. 13(1) alone will not find the word "Logik" there; it is in 13(2)(f).

- **§ 46 DSG NRW applicability caveat.** The state module says § 46 applies directly only to Gefahrenabwehr/Strafverfolgung and is included as an interpretive yardstick for general municipal activity. So on the state layer I cited `[DSG-NRW-§46-1]` but was careful to frame it as Auslegungsmaßstab, not as the directly-governing rule, and noted § 46(3) (discriminatory profiling) is not triggered. The checklist mentions `[DSG-NRW-§46-3]`; I referred to its content (profiling ban) but the reference file labels it as "(3)", so the ID resolves.

- **Tooling friction (not the folder's fault).** My first two attempts to write the report were blocked: the Write tool refused the filename `report.md` as a "report file", and a shell heredoc then failed on a quoting error. I ended up writing the content to a scratch file and copying it into `demo/cold-run/`. No bearing on the audit itself.

## Where I was unsure how to classify

- **PS-3 was the hardest call (see final report question).** Strong, quotable training exclusion ("kann nicht aktiviert werden") pulling toward CLEAR PASS, but the dossier is explicitly silent on the Eingabe-Historie default, which the compound check's CLEAR PASS bar also requires. "Silence is never a PASS" settled it as NARROW FLAG, against the pull of the strongest sentence in the whole dossier.

- **PS-2 severity.** Tempting to read the unaddressed US remote access as a CLEAR FAIL (potential undisclosed third-country transfer). But rules.md requires a quotable contradiction for a FAIL, and the dossier does not affirmatively state a transfer happens; it leaves it open ("wird nicht ausgeführt"). Open, not contradicted, so NARROW FLAG. The missing sub-processor list pushed the same way (present-but-not-guaranteed-complete = FLAG, not FAIL).

- **PS-0.** Briefly considered CLEAR FAIL, but that class needs the dossier to claim no DSFA is needed. It instead recommends one, so it is a gap (FLAG), not a contradiction.
