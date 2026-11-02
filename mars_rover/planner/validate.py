"""Independent plan validator: re-simulates the plan on the LIFTED domain
(no grounding / pruning), checks every precondition, prints each state."""
import sys
from pddl_parser import Domain, Problem, subst

def fmt(state, keys):
    return ", ".join("(%s)" % " ".join(f) for f in sorted(state) if f[0] in keys)

def main(dom_f, prob_f, plan_f, out_f):
    d, p = Domain(dom_f), Problem(prob_f)
    plan = []
    for line in open(plan_f):
        line = line.split(":", 1)[-1].strip() if line[:3].strip().rstrip(":").isdigit() else line.strip()
        if line.startswith("("): plan.append(line.strip("()").split())
    dyn = {a[0] for act in d.actions.values() for a in act.add + act.dele}
    state = set(p.init); out = []
    P = lambda s="": out.append(s)
    P("VALIDATION of %s on %s" % (plan_f, prob_f)); P("=" * 60)
    P("Initial dynamic state:"); P("  " + fmt(state, dyn)); ok = True
    for i, step in enumerate(plan, 1):
        act = d.actions[step[0]]
        b = {pn: v for (pn, _), v in zip(act.params, step[1:])}
        missing = [subst(x, b) for x in act.pre if subst(x, b) not in state]
        P(); P("Step %d: (%s)" % (i, " ".join(step)))
        if missing:
            P("  FAILED - unsatisfied preconditions: %s" % missing); ok = False; break
        P("  preconditions OK (%d checked)" % len(act.pre))
        for x in act.dele: state.discard(subst(x, b))
        for x in act.add: state.add(subst(x, b))
        P("  rover-at: %s | bays: %s" % (
            [f[2] for f in state if f[0] == "rover-at"],
            {f[1]: "empty" for f in state if f[0] == "bay-empty"} |
            {f[2]: f[1] for f in state if f[0] == "in-bay"}))
    P(); P("=" * 60); P("FINAL STATE (dynamic facts):"); P("  " + fmt(state, dyn)); P()
    rocks = sorted(o for o, t in p.objects if t == "rock")
    for g in p.goal:
        P("  goal %-28s %s" % ("(%s)" % " ".join(g), "SATISFIED" if g in state else "NOT SATISFIED"))
    ok = ok and all(g in state for g in p.goal)
    P(); P("All %d rocks at base : %s" % (len(rocks), all(("rock-at", r, "base") in state for r in rocks)))
    P("Both bays empty      : %s" % all(("bay-empty", b) in state for b, t in p.objects if t == "bay"))
    P("Rover at base        : %s" % (("rover-at", "curiosity", "base") in state))
    P("Drill carried        : %s" % any(f[0] == "has-drill" for f in state))
    P(); P("PLAN VALID: %s  (length %d)" % (ok, len(plan)))
    open(out_f, "w").write("\n".join(out) + "\n"); print("\n".join(out))

main(*sys.argv[1:5])
