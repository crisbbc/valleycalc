# Golden Valley Masterdoc parity audit

## Scope and authority

- Source of truth: `rules/[🌻Golden Valley Masterdoc].pdf` (27 pages).
- Website reviewed: `index.html` and its referenced presentation/assets.
- At the user's direction, the dedicated **CLASSes** tables on pages 14–15 override the conflicting early summary on pages 8–9.
- At the user's direction, page 16's colored-icon memberships override the conflicting text trios on page 9.
- A missing topic in the Masterdoc is not treated as a contradiction with a website-only feature.

### Decision record

- Class conflict prompt: “Which values should govern the fixes?” User answer: **Dedicated section (Recommended)**.
- Soul conflict prompt: “Visual inspection found page 16's colored icons conflict with page 9's text trios. Which exact memberships should the website use?” User answer: **Page 16 icons (Recommended)** — Versatile: Patience/Enthusiasm/Insight; Durable: Integrity/Perseverance/Will; Passionate: Justice/Bravery/Mindfulness; Attentive: Kindness/Loyalty/Protectiveness.

## Requirement-to-implementation checklist

| Masterdoc location | Requirement or content | Website mapping | Result |
| --- | --- | --- | --- |
| Pages 1–2 | Lore heading and placeholder lore text | No lore feature | Not applicable; no actionable rule |
| Pages 3–4 | SOULs heading; no extractable rules on page 4 | Soul picker in `index.html` | Covered by the explicit Soul rules below |
| Page 5 | GAMEPLAY heading | No standalone requirement | Not applicable |
| Page 6 | Encounter ACTING/BATTLING turn order, skipped downed turns, formation adjustment, and enemy behavior | Character builder does not run encounters | Not applicable to this calculator |
| Pages 6–7 | FIGHT, SMITE, HEAL, BUFF, SKILL/SPELL, DEFEND, GUARD, TAUNT, and ITEMS mechanics | Class ACT names are displayed; combat effects/minigames are not simulated | Names covered; mechanics not applicable to this calculator |
| Page 8 | TP gain/loss, locked bar segments, skill costs, and Team Up Actions | No combat or TP runtime | Not applicable; character-specific TP values are not provided |
| Page 8 | Four-slot formation and target chances | No party/encounter runtime | Not applicable |
| Pages 8–9 | Early class summary | `classes` data | Superseded by pages 14–15 per user decision |
| Page 9 | Four numbered text Soul trios | No direct mapping; page 16 supplies conflicting colored-icon memberships | Superseded by page 16 icons per explicit user decision |
| Page 9 | DPS/TANK/HEALER/SUPPORT labels and unassigned passive-like prose | Class role summaries only | Not applicable; the extracted text provides no complete role rules or character assignments |
| Page 9 | Downed regeneration: EN 1 = 10%, +1 percentage point per additional EN | `calculateDerivedStats`: `9 + en`, rounded HP, half-HP recovery turn count | Match |
| Page 9 | Revive HP: HP 1 = 15%, +1 percentage point per additional HP | `calculateDerivedStats`: `14 + hp`, rounded HP | Match |
| Page 9 | Max overhealth: DF 1 = 20%, +1 percentage point per additional DF | `calculateDerivedStats`: `19 + df`, rounded HP | Match |
| Pages 9 and 11 | Examples imply each HP point grants 10 max HP | `calculateDerivedStats`: `hp * 10`; Field guide text | Match |
| Pages 10–11 | Every stat must be at least 1 | `MIN_STAT`, `isValid`, `setStat`, and numeric input minimum | Match |
| Page 11 | HP meaning and revive scaling | `definitions` and derived preview | Match |
| Page 11 | AT strengthens FIGHT and perfect zones | `definitions` Field guide text | Match |
| Page 11 | MG boosts skills/spells and TP gain while reducing TP loss | `definitions` Field guide text | Match |
| Page 11 | DF reduces damage and raises max overhealth | `definitions` and derived preview | Match |
| Page 11 | EN raises invincibility and downed regeneration | `definitions` and derived preview | Match |
| Page 12 | Max TP is 2–4 bars (200–400), but no assignment rule is given | No Max TP calculation | Not implementable from the Masterdoc; no parity claim made |
| Page 12 | INV scales with EN, but the default is left as `X` frames | Field guide states the qualitative relationship | Numeric calculation not implementable from the Masterdoc |
| Page 12 | Overhealth is capped and scales with DF | Derived max-overhealth preview | Match for the specified maximum; combat-time capping is not applicable |
| Page 12 | Two dangling recovery headings contain no values | Formulas use the complete values on page 9 | No actionable additional rule |
| Pages 13–15 | Classes govern bonuses and available ACTs | `classes`, class selector, bonus text, preview role, and ACT preview | Fixed and covered |
| Page 14 | Fighter: +6 AT, +2 MG; SMITE, SKILL/SPELL, DEFEND, ITEMS | `classes.Fighter` | Match |
| Page 14 | Healer: +6 MG, +2 DF, +3 HP; HEAL, SKILL/SPELL, DEFEND, ITEMS | `classes.Healer` | Fixed: HP 2→3, role, and ACTs |
| Page 14 | Guardian: +6 DF, +2 AT, +5 HP; FIGHT, SKILL/SPELL, GUARD, ITEMS | `classes.Guardian` | Fixed: role wording and ACTs |
| Page 15 | Caster: +4 MG, +2 DF, +2 EN; BUFF, SKILL/SPELL, DEFEND, ITEMS | `classes.Caster` | Fixed: replaced +4 EN with +2 DF/+2 EN, role, and ACTs |
| Page 15 | Cheerleader: +4 EN, +2 MG, +2 AT, +2 HP; FIGHT, SKILL/SPELL, TAUNT, ITEMS | `classes.Cheerleader` | Fixed: HP 1→2, role, and ACTs |
| Page 14 | Classes also govern future level-up stat growth | No leveling feature | Not applicable to this calculator |
| Page 16 | Versatile icons: Patience, Enthusiasm, Insight | `souls` group metadata and selected-Soul preview | Match; icon-defined membership selected by user |
| Page 16 | Durable icons: Integrity, Perseverance, Will | `souls` group metadata and selected-Soul preview | Match; icon-defined membership selected by user |
| Page 16 | Passionate icons: Justice, Bravery, Mindfulness | `souls` group metadata and selected-Soul preview | Match; icon-defined membership selected by user |
| Page 16 | Attentive icons: Kindness, Loyalty, Protectiveness | `souls` group metadata and selected-Soul preview | Match; icon-defined membership selected by user; `Freedom` display label corrected to `Will` |
| Page 16 | Each group has a descriptive quote | `soulGroups`; selected group and quote appear on the character card | Fixed |
| Page 16 | Souls grant passive abilities, but no actual passive mechanics are specified | No passive calculation | Not implementable from the Masterdoc |
| Pages 17–27 | Blank pages and headings for Status Effects, Calculations, Playable Characters, NPCs, and Enemies | No corresponding data supplied | Not applicable; no actionable requirements |

## Website-only features retained

The Masterdoc does not define the 25-point creation budget, character names, random builds, Human/Monster visual variants, PNG export, or presentation styling. None conflicts with an explicit Masterdoc rule, so these features remain unchanged.

## Confirmed issues fixed

1. Healer, Caster, and Cheerleader bonuses used the conflicting early-summary values.
2. All five class role summaries followed the early summary rather than the dedicated class section.
3. Class ACT loadouts were absent from the character preview.
4. The Masterdoc's `Will` Soul was displayed as `Freedom`.
5. Soul trio/group mappings and the page-16 group descriptions were absent from the character preview.
6. Page 9's text trios conflict with page 16's colored-icon memberships; the user selected page 16's exact icon-defined groups.

Changed files: `index.html`, `test_parity.py`, and `GOLDEN_VALLEY_PARITY_AUDIT.md`.

## Verification results

- `python test_parity.py`: passed in headless Firefox. The failing test harness exercises all five class selections, effective stat chips, roles, ACT loadouts, all 12 Soul selections/group mappings and quotes, and the `Will` label in the rendered UI.
- Inline JavaScript syntax (`node --check`): passed.
- Focused runtime checks: all 5 class specs, all 12 Soul mappings, 3 Masterdoc calculation examples, preview mappings, and stat validation passed.
- Persistent in-page self-checks cover class effective stats, roles, ACTs, Soul names/groups, derived stats, and stat validation.
- HTML parse, duplicate-ID check, and referenced static-asset check: passed (20 unique IDs; all referenced static assets present).
- `git diff --check`: passed.
- Primary HTML/Python/Markdown LSP diagnostics: clean.
- pi-lens diagnostics: clean after marking the generated inline `data:` SVG URL warning as a false-positive.
- The repository has no project manifest or separate build command; `test_parity.py` is the project-local verification entry point.

## Remaining exceptions

No confirmed applicable parity issue remains. Rules with placeholders (`X`/`Xxx`), missing assignments, combat-only runtime behavior, and empty document sections are explicitly classified above rather than guessed.
