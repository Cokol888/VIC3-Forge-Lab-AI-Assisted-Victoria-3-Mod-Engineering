# Vanilla Rework audit seed (beta15)

This is the first structured inventory for the later legacy/vanilla CMP rework. It does not remove legacy functions yet.

## Confirmed audit items

- B2 `Tax Income` label maps to `country_government_dividends_efficiency_add`, so the visible name does not describe the actual mechanic. Economy 2.0 already corrected this.
- B3/B5 use dense `Shift/Alt/Ctrl/RMB` modifier semantics; the operation and magnitude are hidden in tooltips instead of being explicit controls.
- B5 political-strength modifiers are often perceived as direct clout controls. Politics 2.0 explicitly labels them as political-strength multipliers because clout is a relative result.
- B3 law modification has powerful direct effects (`activate_law`, `cancel_enactment`, `add_enactment_phase`, `add_enactment_setback`) but legacy UI does not consistently explain eligibility and persistence.
- Character health/popularity in legacy B3 are modifiers, not direct SET values. Politics 2.0 labels them as boosts.
- Power Bloc legacy functions are broad and partly destructive; beta15 only promotes cohesion to the new UI until membership/principles/leverage are audited.

## Vanilla Rework rule

For every legacy control record: visible label -> tooltip -> ScriptedGui -> effect/modifier -> scope -> persistence -> eligibility -> post-tick result -> save/load result. Misleading labels are renamed before visual redesign.
