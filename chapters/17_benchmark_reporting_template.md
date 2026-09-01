# **Benchmark Reporting Template**

Use this appendix to publish a blockchain scalability result another team can reproduce. Replace every prompt; do not leave a field blank without explaining why it does not apply.

## **1. Claim**

State one falsifiable result:

> System ___ at commit/version ___ sustained ___ completed operations per second for ___ minutes under workload ___ while p99 ___ latency remained below ___, with ___ validators/operators and the following injected faults: ___.

Name the completion boundary: sequencer acceptance, block inclusion, execution, certification, proof acceptance, settlement finality, destination execution, or another precisely defined event.

## **2. System Under Test**

| Field | Value |
|---|---|
| Repository and commit | |
| Protocol/config version | |
| VM and compiler | |
| State/database backend | |
| Consensus implementation | |
| Proof/fault system | |
| DA path and retention | |
| Bridge/messaging version | |
| Build flags and dependencies | |
| Date tested | |

Attach configuration files and a machine-readable dependency lock. Identify local patches not present in the named commit.

## **3. Topology and Control**

| Role | Count | Independent operators | Regions/providers | Client diversity |
|---|---:|---:|---|---|
| Validators | | | | |
| Sequencers | | | | |
| Provers/challengers | | | | |
| DA nodes/retrievers | | | | |
| Relayers | | | | |
| RPC/indexing nodes | | | | |

List upgrade, pause, bridge, and emergency keys separately. A process count is not an operator count.

## **4. Hardware and Network**

For every machine class, report:

```text
CPU model, sockets, physical/logical cores
memory capacity and speed
storage device, filesystem, capacity, and measured IOPS/bandwidth
network interface and measured bandwidth
operating system and kernel
container or virtual-machine limits
power or accelerator settings
```

Report network shaping between regions: round-trip latency distribution, bandwidth cap, packet loss, jitter, and clock synchronization. State whether nodes share one host, switch, cloud account, or availability zone.

## **5. Initial State**

| Property | Value |
|---|---:|
| Accounts/objects | |
| Contracts | |
| Live state bytes | |
| History bytes | |
| Working-set bytes | |
| Snapshot/sync source | |
| Cache warm-up rule | |

Publish a state generator or snapshot commitment. A short in-memory test does not represent a chain whose working set exceeds memory.

## **6. Workload**

| Transaction class | Share | Input bytes | Reads | Writes | Execution cost | Success target |
|---|---:|---:|---:|---:|---:|---:|
| Transfer | | | | | | |
| Contract call | | | | | | |
| Deployment | | | | | | |
| Cross-domain message | | | | | | |
| Other | | | | | | |

Describe key popularity, account skew, contract contention, value distributions, bursts, invalid transactions, and retries. Publish generator code, seed, and transaction templates.

## **7. Offered-Load Schedule**

Do not run only at one selected rate. Record a sweep:

| Phase | Duration | Offered load | Purpose |
|---|---:|---:|---|
| Warm-up | | | fill caches and queues |
| Low load | | | baseline |
| Ramp steps | | | locate capacity knee |
| Sustained target | | | validate SLO |
| Overload | | | observe admission/backpressure |
| Recovery | | | drain queues and reconcile |

State whether rejected client submissions remain in offered load and how open-loop versus closed-loop generation affects pressure.

## **8. Metrics**

Report time series and summary distributions for:

- submitted, accepted, included, executed, successful, proved, and finalized operations;
- p50, p90, p95, p99, and maximum latency at each boundary;
- mempool, batch, publication, proof, message, and withdrawal queue depth and age;
- CPU, memory, storage, network, and accelerator utilization;
- block/batch size, gas or compute units, data bytes, proof time, and state growth;
- leader changes, reorgs, retries, aborted speculative work, and errors;
- fees paid by users and subsidies paid by operators or treasury.

Define aggregation windows and missing-sample handling. Retain raw results.

## **9. Fault Schedule**

| Time | Fault | Scope | Duration | Expected invariant |
|---|---|---|---:|---|
| | leader or sequencer loss | | | no conflicting finality |
| | network delay/partition | | | safety preserved |
| | prover/challenger loss | | | accepted state remains valid |
| | DA withholding/retrieval loss | | | unavailable data not accepted |
| | database restart | | | persisted state and nonces survive |
| | relayer loss/replay | | | eventual delivery and execute-once |
| | key/upgrade test | | | delay, alert, cancellation/exit |

Record the actual observed start and end, not only the test script's requested times.

## **10. Results Table**

| Offered load | Completed throughput | p50 | p95 | p99 | Error rate | Oldest queue | Limiting resource |
|---:|---:|---:|---:|---:|---:|---:|---|
| | | | | | | | |

Plot offered load against completed throughput, p99 latency, error rate, and queue age. The sustainable capacity is the highest region where objectives remain satisfied and queues do not trend upward.

## **11. Resource Envelope**

For each resource `r`, compute:

```text
utilization_r = demand_r / capacity_r
```

Document how capacity was measured and which headroom policy applies. Identify the first tight constraint under typical, burst, and recovery workloads. Do not sum unrelated utilization percentages.

## **12. Finality and User Journey**

Follow at least one transaction and one withdrawal through all identifiers and timestamps:

```text
client submission
sequencer or mempool receipt
block/batch inclusion
canonical data publication
proof/challenge state
settlement inclusion and finality
message relay
withdrawal execution
```

Show what the user interface reported at each boundary and whether retrying was safe.

## **13. Recovery Results**

For every fault, publish:

| Fault | Detection time | User impact | Safety result | Recovery time | Manual action | Residual backlog |
|---|---:|---|---|---:|---|---:|
| | | | | | | |

Verify final state, supply, consumed messages, pending withdrawals, and proof/data queues after recovery. Restarting services is not recovery until end-to-end state reconciles.

## **14. Reproduction Package**

A release artifact should contain:

```text
README with exact commands
source commits and dependency lock
configuration and topology
state generator or snapshot commitment
workload generator and seed
fault-injection scripts
raw metrics and logs
analysis notebook or scripts
plots and final report
checksums for every artifact
```

Remove secrets and personal data without removing evidence needed to reproduce the result. Describe redactions.

## **15. Limitations and Conclusion**

State which environments, workloads, and adversaries were not tested. Separate measured, simulated, and projected values. Name the operating envelope, first bottleneck, recovery cost, trust/control assumptions, and next experiment.

A useful conclusion is narrow:

> Under configuration ___ and workload ___, the system sustained ___ at p99 ___ through fault ___; performance became unstable when ___ queue/resource saturated. This result does not establish ___ and should be reassessed after ___.

The template is complete only when a skeptical team can rerun the test and reach the same interpretation, not merely the same headline number.
