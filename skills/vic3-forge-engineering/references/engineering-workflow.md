# Engineering Workflow

## Route the task

Use the smallest useful mode:

- FAST — local explanation or obvious small fix.
- ENGINEERING — design/implementation of a defined mechanic.
- INVESTIGATION — unknown cause or debugging.
- VALIDATION — prepared implementation needs proof.
- MIGRATION — game/mod/upstream version changes.

## State discipline

Typical progression:

`DISCOVERY -> CONTRACT_READY -> IMPLEMENTATION_READY -> CODE_PREPARED -> STATIC_VERIFIED -> RUNTIME_PENDING -> RUNTIME_VERIFIED -> REGRESSION_PENDING -> VERIFIED -> FROZEN`

Additional states:

`BLOCKED`, `INCONCLUSIVE`, `REVALIDATION_REQUIRED`, `INVALIDATED`.

Require evidence for transitions.

## Investigation loop

1. State the symptom.
2. Load existing evidence and rejected hypotheses.
3. Choose one causal question.
4. Define expected observations for competing outcomes.
5. Make the minimum diagnostic change/test.
6. Record the observation.
7. Mark hypothesis CONFIRMED, REJECTED, INCONCLUSIVE, or BLOCKED.
8. Update Engineering State if knowledge changed.
9. Select the next test by information gain.

After two consecutive INCONCLUSIVE iterations, reassess the model instead of adding random changes.

## Implementation loop

1. Lock design intent.
2. Confirm target environment.
3. Inspect exact current source and source-of-truth generator/registry.
4. Check frozen contracts.
5. Define minimal change set and rollback.
6. Implement.
7. Run appropriate static validators.
8. Keep status at `RUNTIME_PENDING` when runtime proof is still required.
9. Record regression budget.

## Evidence rules

Evidence should include claim, type, source, environment, and status when material.

Static validators may prove structure, deterministic generation, cross-reference integrity, registry consistency, and declared invariants. They do not prove Jomini rendering, game tick semantics, save/load behavior, AI behavior, or gameplay balance unless those are genuinely executed and observed.

## Active Horizon

Detailed work may cover:

- Active Gate
- Next Milestone

Keep later work queued unless explicitly requested.

## Frozen contracts

Do not change a FROZEN subsystem incidentally. If a change is necessary:

1. state why the frozen contract is insufficient;
2. identify affected evidence;
3. define revalidation scope;
4. implement only after the impact is explicit.

## Version change

When target game version/checksum or a locked upstream source changes:

1. identify dependent evidence;
2. mark it `REVALIDATION_REQUIRED`;
3. inspect official/script API delta;
4. revalidate affected contracts;
5. use `INVALIDATED` only when evidence proves the prior contract no longer holds.
