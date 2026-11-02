"""Fast A* (bitmask states) with an admissible, problem-structure heuristic.
h(s) = (#collect/deposit/pick-drill actions still unavoidable)
     + (lower bound on remaining moves from directed shortest-path distances)
Both parts count disjoint action types, so the sum is admissible."""
import sys, time, heapq
from collections import deque
from pddl_parser import Domain, Problem
from search import ground

def main(dom_f, prob_f, out_f):
    d, p = Domain(dom_f), Problem(prob_f)
    facts, G, init, goal = ground(d, p)
    idx = {f: i for i, f in enumerate(facts)}
    bit = lambda f: 1 << idx[f] if f in idx else 0
    ops = [(n, sum(1 << i for i in pre), sum(1 << i for i in add), sum(1 << i for i in dele)) for n, pre, add, dele in G]
    S0 = sum(1 << i for i in init); GM = sum(1 << i for i in goal)
    locs = [o for o, t in p.objects if t == "location"]
    rocks = [o for o, t in p.objects if t == "rock"]
    rover = [o for o, t in p.objects if t == "rover"][0]
    # directed distances from connected facts
    adj = {l: [] for l in locs}
    for f in p.init:
        if f[0] == "connected": adj[f[1]].append(f[2])
    dist = {}
    for s in locs:
        dist[s] = {s: 0}; q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in dist[s]: dist[s][v] = dist[s][u] + 1; q.append(v)
    INF = 10**6
    D = lambda a, b: dist[a].get(b, INF)
    hard = {r for r in rocks if ("hard", r) in p.init}
    drill = [o for o, t in p.objects if t == "drill"][0]
    drill_loc = [f[2] for f in p.init if f[0] == "drill-at"][0]
    rock_at = {(r, l): bit(("rock-at", r, l)) for r in rocks for l in locs}
    at_base = {r: bit(("rock-at", r, "base")) for r in rocks}
    in_bay = {r: sum(bit(("in-bay", r, b)) for b, t in p.objects if t == "bay") for r in rocks}
    rov_at = {l: bit(("rover-at", rover, l)) for l in locs}
    has_drill = bit(("has-drill", rover, drill))
    rock_loc = {r: [f[2] for f in p.init if f[0] == "rock-at" and f[1] == r][0] for r in rocks}

    def h(s):
        cur = next(l for l in locs if s & rov_at[l])
        non, mv = 0, D(cur, "base")
        have = bool(s & has_drill)
        need_drill = False
        for r in rocks:
            if s & at_base[r]: continue
            if s & in_bay[r]: non += 1; continue
            non += 2; L = rock_loc[r]
            if r in hard and not have:
                need_drill = True
                m = D(cur, drill_loc) + D(drill_loc, L) + D(L, "base")
            else:
                m = D(cur, L) + D(L, "base")
            mv = max(mv, m)
        if need_drill: non += 1
        return non + mv

    t0 = time.perf_counter(); expanded = generated = 0
    g = {S0: 0}; parent = {S0: None}; cnt = 0
    openl = [(h(S0), 0, S0)]
    while openl:
        f, _, s = heapq.heappop(openl)
        if f - h(s) > g[s]: continue  # stale entry
        expanded += 1
        if GM & s == GM:
            plan = []; x = s
            while parent[x]: x, op = parent[x]; plan.append(ops[op][0])
            plan.reverse(); secs = time.perf_counter() - t0; break
        gs = g[s] + 1
        for i, (n, pre, add, dele) in enumerate(ops):
            if pre & s == pre:
                t = (s & ~dele) | add
                if t not in g or gs < g[t]:
                    g[t] = gs; parent[t] = (s, i); generated += 1
                    cnt += 1; heapq.heappush(openl, (gs + h(t), cnt, t))
    lines = ["; Domain  : %s" % dom_f, "; Problem : %s" % prob_f,
             "; Search  : A* with admissible structural heuristic (optimal)",
             "; Grounded: %d facts, %d operators" % (len(facts), len(ops))]
    for i, a in enumerate(plan, 1): lines.append("%2d: %s" % (i, a))
    lines += ["; Plan length: %d actions (unit cost)" % len(plan), "; States expanded : %d" % expanded,
              "; States generated: %d" % generated, "; Planning time  : %.4f s" % secs]
    open(out_f, "w").write("\n".join(lines) + "\n"); print("\n".join(lines))
main(*sys.argv[1:4])
