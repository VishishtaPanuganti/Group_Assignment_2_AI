"""Grounded STRIPS planner: BFS, A*(h_max), Greedy Best-First (h_add)."""
import sys, time, heapq
from collections import deque
from itertools import product
from pddl_parser import Domain, Problem, subst

def ground(domain, problem):
    """Ground actions; static preconditions (predicates no action changes) are
    checked against the initial state and removed."""
    changed = {a[0] for act in domain.actions.values() for a in act.add + act.dele}
    objs = problem.objects
    facts_idx, facts = {}, []
    def fid(f):
        if f not in facts_idx:
            facts_idx[f] = len(facts); facts.append(f)
        return facts_idx[f]
    for f in problem.init:
        if f[0] in changed: fid(f)
    ops = []
    for act in domain.actions.values():
        doms = [[o for o, t in objs if t == pt] for _, pt in act.params]
        for combo in product(*doms):
            b = {p: v for (p, _), v in zip(act.params, combo)}
            pre = [subst(p, b) for p in act.pre]
            if any(p[0] not in changed and p not in problem.init for p in pre): continue
            pre = [p for p in pre if p[0] in changed]
            ops.append(("(%s %s)" % (act.name, " ".join(combo)),
                        pre, [subst(a, b) for a in act.add], [subst(d, b) for d in act.dele]))
    # keep only operators whose preconditions can ever be reached (relaxed reachability)
    reach = set(f for f in problem.init if f[0] in changed); ch = True
    while ch:
        ch = False
        for name, pre, add, dele in ops:
            if all(p in reach for p in pre):
                for a in add:
                    if a not in reach: reach.add(a); ch = True
    G = []
    for name, pre, add, dele in ops:
        if all(p in reach for p in pre):
            G.append((name, frozenset(fid(p) for p in pre),
                      frozenset(fid(a) for a in add), frozenset(fid(d) for d in dele)))
    init = frozenset(facts_idx[f] for f in problem.init if f[0] in changed)
    goal = frozenset(fid(g) for g in problem.goal)
    return facts, G, init, goal

def make_heuristic(kind, G, goal):
    pre_of = [g[1] for g in G]; add_of = [g[2] for g in G]
    def h(state):
        cost = {f: 0 for f in state}
        changed = True
        while changed:
            changed = False
            for i in range(len(G)):
                pre = pre_of[i]
                if not all(p in cost for p in pre): continue
                c = (max((cost[p] for p in pre), default=0) if kind == "hmax"
                     else sum(cost[p] for p in pre)) + 1
                for a in add_of[i]:
                    if a not in cost or c < cost[a]:
                        cost[a] = c; changed = True
        if any(g not in cost for g in goal): return float("inf")
        vals = [cost[g] for g in goal]
        return max(vals, default=0) if kind == "hmax" else sum(vals)
    return h

def search(G, init, goal, strategy):
    h = {"bfs": None, "astar": make_heuristic("hmax", G, goal),
         "gbfs": make_heuristic("hadd", G, goal)}[strategy]
    t0 = time.perf_counter()
    expanded = generated = evaluated = 0
    parent = {init: None}; g = {init: 0}
    def extract(s):
        plan = []
        while parent[s] is not None:
            s, op = parent[s]; plan.append(G[op][0])
        return plan[::-1]
    def succ(s):
        for i, (n, pre, add, dele) in enumerate(G):
            if pre <= s: yield i, (s - dele) | add
    if strategy == "bfs":
        q = deque([init])
        while q:
            s = q.popleft(); expanded += 1
            if goal <= s: return extract(s), expanded, generated, time.perf_counter() - t0
            for i, t in succ(s):
                if t not in parent:
                    parent[t] = (s, i); generated += 1; q.append(t)
        return None, expanded, generated, time.perf_counter() - t0
    cnt = 0; hc = {init: h(init)}
    f0 = hc[init] if strategy == "gbfs" else hc[init]
    openl = [(f0, 0, cnt, init)]; closed = set()
    while openl:
        f, _, _, s = heapq.heappop(openl)
        if s in closed: continue
        if strategy == "astar" and f - hc[s] != g[s] and False: continue
        closed.add(s); expanded += 1
        if goal <= s: return extract(s), expanded, generated, time.perf_counter() - t0
        for i, t in succ(s):
            ng = g[s] + 1
            if strategy == "gbfs":
                if t in parent: continue
                parent[t] = (s, i); g[t] = ng; generated += 1
                hc[t] = h(t); cnt += 1
                heapq.heappush(openl, (hc[t], 0, cnt, t))
            else:
                if t not in g or ng < g[t]:
                    g[t] = ng; parent[t] = (s, i); generated += 1
                    if t not in hc: hc[t] = h(t)
                    cnt += 1
                    heapq.heappush(openl, (ng + hc[t], hc[t], cnt, t))
    return None, expanded, generated, time.perf_counter() - t0

if __name__ == "__main__":
    dom_f, prob_f, strat, out_f = sys.argv[1:5]
    d, p = Domain(dom_f), Problem(prob_f)
    facts, G, init, goal = ground(d, p)
    plan, exp, gen, secs = search(G, init, goal, strat)
    label = {"bfs": "Breadth-First Search (optimal)",
             "astar": "A* with admissible h_max (optimal)",
             "gbfs": "Greedy Best-First Search with h_add (satisficing)"}[strat]
    lines = ["; Domain  : %s" % dom_f, "; Problem : %s" % prob_f, "; Search  : %s" % label,
             "; Grounded: %d facts, %d operators" % (len(facts), len(G))]
    if plan is None: lines.append("; NO PLAN FOUND")
    else:
        for i, a in enumerate(plan, 1): lines.append("%2d: %s" % (i, a))
        lines.append("; Plan length: %d actions (unit cost)" % len(plan))
    lines += ["; States expanded : %d" % exp, "; States generated: %d" % gen,
              "; Planning time  : %.4f s" % secs]
    open(out_f, "w").write("\n".join(lines) + "\n"); print("\n".join(lines))
