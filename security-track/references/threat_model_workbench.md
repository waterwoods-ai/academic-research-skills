# Threat Model Workbench (Custom — Security Track)

> The single field template + stress tests for building a threat model that
> survives a Big-4 panel. Used when writing the Threat Model section, filling
> an S2 RQ card or S3 Contribution Card, and by reviewer personas R4/R1.
> The Threat Model is the most common place ML/NLP-to-security transfers
> fail — a strong method with weak security framing dies here.

## The 11 fields (fill every one; "N/A — because …" is an answer, silence is not)

1. **Assets** — what is being protected (data, model, control loop, key,
   availability of a service). Name them concretely.
2. **Adversary goal** — what the attacker ultimately wants to achieve.
3. **Adversary knowledge** — white-box / gray-box / black-box, AND *why that
   level is realistic for the deployment scenario*. A white-box assumption
   with no deployment justification is a standard reject. State exactly what
   is known: model architecture? parameters? training data? system config?
4. **Adversary capabilities** — what the attacker can DO: query? modify
   input? control the network? control a client? modify training data?
   inject a physical signal?
5. **Adversary access** — where the attacker sits: remote / same-LAN /
   co-located app / physical / supply-chain. Post-segmentation era,
   "attacker on the same LAN" needs justification.
6. **Constraints** — query budget, perturbation budget, physical constraints,
   time/compute budget, access constraints. Bound the attacker.
7. **Trust assumptions** — which components are trusted; TCB size.
8. **System assumptions** — deployment configuration, defenses already
   present, operating conditions assumed.
9. **Out-of-scope attacks** — state them explicitly. Reviewers respect
   declared boundaries and punish silent ones.
10. **Attack success criteria** — the objective, measurable condition under
    which the attack counts as succeeding. Write it so a third party could
    check it.
11. **Security impact** — which property is actually violated:
    **confidentiality / integrity / availability / authenticity / privacy**.
    Name the one(s). This field is where a "results" claim becomes a
    "security" claim.

## Three stress tests (a threat model must pass all three)

Run these against your own threat model before a reviewer does:

1. **Custom-fit test** — Is the threat model designed *so that the attack
   works*, rather than describing a realistic adversary? If the model looks
   reverse-engineered from the desired result, R4 will say so.
2. **Weaker-attacker test** — If you *reduce* the attacker's capability or
   knowledge, does the attack still succeed? If it only works at the exact
   stated capability, the contribution is fragile.
3. **Stronger-attacker test** — If you *increase* the capability, does the
   research become trivial? ("attacker can write firmware but somehow
   cannot read the key" — inconsistent capability is a fatal flaw.)

## The "so what" test (turns a result into a security contribution)

A statement like:

> "We can cause the classifier to make a mistake."

is not, by itself, a sufficient security contribution. You must answer:

> **So what security property has actually been violated — and for whom,
> under what realistic conditions?**

If you cannot name the violated property from field 11 and tie it to a
realistic deployment, the work reads as an ML paper with a security label,
not a security paper. (See `security_framing_protocol.md` for the full
framing-risk check.)

## Domain specifics

- **CPS**: physical-access and supply-chain assumptions must be stated;
  quantify the physical consequence, not just protocol-level success.
- **IoT**: state whether the attack needs local network, internet exposure,
  or only pairing-time access; device/vendor scope bounds generality.
- **AI security**: specify the attack surface (training data / model weights
  / query API / physical sensor channel) and whether the setting is
  adaptive (attacker aware of the defense). Non-adaptive-only evaluation is
  a standard reject for defenses.
