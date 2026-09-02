# **Threat-Model Worksheets**

A scalability design distributes work across more roles, queues, contracts, and networks. The threat model should follow those interfaces. This appendix provides reusable worksheets for design reviews and incident exercises.

## **Start With Assets and Outcomes**

List what the system protects. Examples include base-layer escrow, L2 balances, ordering fairness, confidential transaction content, data needed for exit, governance authority, proof-signing keys, and the ability to make progress before a deadline.

For each asset, name an unacceptable outcome:

| Asset | Unacceptable outcome | Detection | Recovery |
|---|---|---|---|
| Bridge escrow | unbacked withdrawal | supply and message reconciliation | pause, contain, and repair under published process |
| Rollup state | invalid root accepted | independent execution or proof checks | challenge or reject before finality |
| Transaction data | accepted state cannot be reconstructed | retrieval and sampling failure | reject/halt; repair from independent peers |
| Channel balance | old state settles | breach monitor sees revoked commitment | submit newer state or penalty before deadline |
| Ordering | censor or reorder beyond policy | compare mempool/inbox and block evidence | forced inclusion, alternate sequencer, penalty |
| Upgrade authority | unauthorized or immediate rule change | key and timelock monitoring | cancel, exit, rotate under governance rules |

Do not label every outcome "fund loss." Liveness loss, indefinite lock, privacy disclosure, unfair ordering, and unaffordable recovery are distinct harms with different mitigations.

## **Role Worksheet**

Create one row for every actor and automated service:

| Role | Inputs observed | Action controlled | Can violate safety? | Can halt progress? | Replacement path |
|---|---|---|---|---|---|
| Sequencer | user transactions, order flow | inclusion and ordering | only if proof/contract permits invalid state | yes | L1 inbox or another sequencer |
| Prover | witness and execution trace | proof delivery | cannot forge under sound verifier | yes, by withholding | redundant permissionless prover |
| DA operator | batch shares | storage and delivery | may break recovery assumptions | yes | reconstruction, repair, alternate DA policy |
| Relayer | source events and proofs | message transport | no if destination fully verifies | yes if exclusive | permissionless replacement |
| Upgrade signer | proposed code and parameters | verifier/bridge changes | often yes | often yes | timelock, cancellation, user exit |

A role that cannot forge state may still create a severe user loss by blocking a time-sensitive exit. Evaluate safety, liveness, privacy, and ordering separately.

## **Trust Boundary Worksheet**

For each message crossing a boundary, record:

```text
producer and verifier
source and destination domains
canonical encoding and version
freshness: nonce, height, epoch, or expiry
commitment and inclusion proof
source finality rule
data availability requirement
replay and idempotence key
timeout and recovery
upgrade authority for both ends
```

Then mutate one field at a time. Try a valid message from the wrong chain, an old epoch, a duplicate nonce, a proof against a reorganized root, an unknown version, an expired promise, and a payload whose bytes do not match the committed hash.

A verifier should reject for a specific reason. "Invalid proof" is too broad for incident response when the real problem is an unavailable header or unsupported version.

## **Adversary Worksheet**

Describe capabilities rather than using only labels such as honest or malicious:

- controls less than, equal to, or more than a consensus threshold;
- delays, drops, reorders, duplicates, or selectively reveals network messages;
- corrupts participants before execution or adaptively after observing state;
- compromises one key, a signing quorum, a client implementation, or a cloud region;
- submits valid but expensive transactions to exhaust proving, storage, or retries;
- observes private order flow and trades before public inclusion;
- withholds data while answering selected samplers;
- exploits upgrade, pause, or recovery controls;
- causes correlated failures through shared libraries, hardware, RPC, or time sources.

For every capability, state which property still holds and which can fail. If safety requires fewer than one-third Byzantine weight and liveness requires eventual synchrony, write both conditions.

## **Economic Worksheet**

Security penalties must exceed plausible gain and remain enforceable. Record:

```text
value at risk
maximum gain from one violation
collateral available for penalty
time until collateral can exit
who proves the violation
who executes the penalty
correlated violator set
cost imposed on honest users during defense
```

A $1 million bond does not secure $100 million of extractable value when the violator can withdraw the bond before evidence finalizes. A challenge reward does not create an honest challenger when proof generation costs more than the reward or access is permissioned.

Rate limits bound loss per time but can extend honest withdrawals. Emergency pauses contain damage but place power in pause keys. Show both sides of every control.

## **Availability and Deadline Worksheet**

Time-sensitive protocols require explicit clocks and margins:

| Deadline | Starts at | Evidence of expiry | Congestion assumption | Miss consequence |
|---|---|---|---|---|
| Channel dispute | commitment inclusion | finalized block height | remedy fits before window closes | outdated state settles |
| Forced inclusion | L1 inbox acceptance | block/time rule | L1 has capacity under mass use | censorship continues |
| Fault proof | state proposal | settlement rule | challenger can retrieve data and submit | invalid state finalizes |
| Cross-domain refund | escrow finality | source timestamp/height | claim/refund ordering defined | double claim or long lock |
| Preconfirmation | signed promise | target slot/finality evidence | signer and evidence remain available | penalty or broken promise |

Test deadline paths with fee spikes, reorganization, clock skew, delayed evidence, and many users acting at once. Average inclusion time is not a safe deadline margin.

## **Upgrade Worksheet**

Inventory everything an upgrade can change: VM rules, circuit and verifier, bridge decoder, DA network, sequencer set, fee accounting, message domains, pause behavior, and escape paths.

For each change, record proposer, approver threshold, timelock, cancellation, code hash, audit evidence, activation boundary, in-flight message handling, state migration, old-version exit, and rollback policy.

An upgrade that changes a message format needs compatibility rules for already-open channels, escrows, deposits, and withdrawals. An escape hatch controlled by the same immediate key as the main verifier is not independent protection against that key.

## **Test-to-Claim Matrix**

Connect every external claim to evidence:

| Claim | Required test | Passing evidence |
|---|---|---|
| Invalid state cannot finalize | generate invalid roots/proofs and exercise dispute | verifier rejection or successful challenge before deadline |
| Sequencer cannot permanently censor | stop sequencer and use forced path | transaction or exit completes within stated bound |
| Data is available | shut publisher and selected peers | independent reconstruction from authenticated commitment |
| Messages execute once | duplicate and reorder valid proofs | one state transition and stable consumed identifier |
| Validator-set transition is safe | overlap epoch change with timeout/restart | no conflicting commit; light client authenticates new set |
| Proving keeps up | replay measured job distribution with worker loss | bounded queue and recovery within service-level objective (SLO) |
| Users can mass exit | invoke recovery at modeled scale under congestion | required population exits within window and budget |

If a test demonstrates only the normal path, narrow the claim. A successful proof verification does not demonstrate prover availability. A successful upload does not demonstrate data reconstruction. One user's exit does not demonstrate mass-exit capacity.

## **Review Output**

A completed threat model should produce:

1. architecture and trust-boundary diagrams;
2. asset/outcome and role matrices;
3. adversary and timing assumptions;
4. protocol invariants and domain-separated message formats;
5. economic and key-control analysis;
6. test-to-claim matrix with reproducible evidence;
7. residual risks, launch limits, and user-visible statuses;
8. incident runbooks and reassessment triggers.

Threat modeling is not complete when every risk has a mitigation. It is complete enough to act when assumptions, remaining exposure, detection, recovery, and ownership are explicit and testable.
