# Method-Change Provenance Guard (Custom — Security Track)

> Fires whenever a method is proposed, changed, improved, replaced, or a
> rescue method is offered — INCLUDING when experiments underperform (S6
> improvement loop) and when responding to a reviewer's requested change.
> A method born in the improvement loop is NOT exempt from the same
> topic-selection + novelty verification that S3 applies to the first
> proposal. This guard exists because the single highest-risk moment for
> accidental duplication / renamed prior art is exactly when a failing
> result pressures the loop to grab a known method and rename it.

## When it fires

- experiments miss the frozen criteria and a substitute mechanism is proposed
- a reviewer asks for a change and the response introduces a new mechanism
- any "let's instead do X" that changes the method's *mechanism* (not tuning)

## The three checks (all must pass before the change is accepted)

### 1. Scenario fidelity — does the substitute still solve the ORIGINAL problem?

Restate the original threat model and the original problem. Does the new
method address the SAME threat model at the SAME point in the pipeline, or
did it silently redefine the problem into an easier one?

Worked example (IoT OTA): the original problem is *model parameters altered
BEFORE signing, so the signature is valid over malicious parameters*; the
proposed method was behavior-based detection at the MCU. A "separate
signature" scheme addresses build/provenance integrity — a DIFFERENT point
in the pipeline — and does not by itself solve "the first signing already
covered tampered parameters." Switching to it is a silent goalpost move.
Name the drift; do not let a substitute quietly change the problem.

### 2. Prior-art identity — is the "new" method a rename?

Strip the new name. Search for the closest established method/framework.
**Naming a mechanism does not make it novel** — calling it "D-Crypto" does
not distinguish it from in-toto / SLSA / TUF / Uptane / Sigstore. If, once
renamed, it matches published prior art, it is a RENAME, not a contribution.

### 3. Honest outcome — one of two, never a silent rename

- **ADOPT + CITE**: "we apply <in-toto / SLSA / …> to <this setting>." The
  contribution then drops to systems/application novelty at best (see
  novelty typing in `security_framing_protocol.md`). State it honestly.
- **GENUINE DELTA**: name the nearest prior art, state precisely what
  differs, prove the delta matters — then re-verify it is NOVEL-WITHIN-
  SEARCH like any S3 claim (real retrieval against Big-4 + tier-2).

## Domain anchor — supply-chain / OTA integrity

Before claiming any new signing / attestation / integrity / provenance
scheme, position against these established frameworks: **in-toto, SLSA,
TUF, Uptane, Sigstore, Notary**. (Uptane specifically targets automotive /
IoT OTA.) A "new" scheme in this space that is not positioned against them
will be read as a rename.

## Output

Append to `method_changelog.md` for the change: nearest prior art +
verdict (RENAME / GENUINE-DELTA / ADOPT-AND-CITE) + a one-line
scenario-fidelity note. A change with verdict RENAME is not an improvement
— it is either dropped or re-labeled as ADOPT-AND-CITE with the novelty
claim removed.
