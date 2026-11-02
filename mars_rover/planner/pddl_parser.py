"""Minimal PDDL parser for the STRIPS + :typing subset (conjunctive preconds,
add/delete effects, flat types)."""
import re
from itertools import product

def tokenize(text):
    text = re.sub(r";.*", "", text)
    return text.replace("(", " ( ").replace(")", " ) ").lower().split()

def parse_sexp(tokens):
    pos = 0
    def rec():
        nonlocal pos
        tok = tokens[pos]; pos += 1
        if tok == "(":
            lst = []
            while tokens[pos] != ")":
                lst.append(rec())
            pos += 1
            return lst
        return tok
    return rec()

def parse_typed_list(items):
    """['a','b','-','t','c'] -> [('a','t'),('b','t'),('c','object')]"""
    out, pending, i = [], [], 0
    while i < len(items):
        if items[i] == "-":
            t = items[i + 1]
            out += [(n, t) for n in pending]; pending = []; i += 2
        else:
            pending.append(items[i]); i += 1
    out += [(n, "object") for n in pending]
    return out

def conj_to_list(f):
    if not f: return []
    if f[0] == "and": return [x for x in f[1:]]
    return [f]

class Action:
    def __init__(self, name, params, pre, add, dele):
        self.name, self.params, self.pre, self.add, self.dele = name, params, pre, add, dele

class Domain:
    def __init__(self, path):
        sx = parse_sexp(tokenize(open(path).read()))
        self.name = sx[1][1]
        self.actions, self.types, self.requirements = {}, [], []
        for sec in sx[2:]:
            if sec[0] == ":requirements": self.requirements = sec[1:]
            elif sec[0] == ":types": self.types = [t for t, _ in parse_typed_list(sec[1:])]
            elif sec[0] == ":action":
                name = sec[1]; d = dict(zip(sec[2::2], sec[3::2]))
                params = parse_typed_list(d[":parameters"])
                pre = conj_to_list(d[":precondition"])
                add, dele = [], []
                for e in conj_to_list(d[":effect"]):
                    (dele if e[0] == "not" else add).append(e[1] if e[0] == "not" else e)
                self.actions[name] = Action(name, params, pre, add, dele)

class Problem:
    def __init__(self, path):
        sx = parse_sexp(tokenize(open(path).read()))
        self.name = sx[1][1]
        for sec in sx[2:]:
            if sec[0] == ":objects": self.objects = parse_typed_list(sec[1:])
            elif sec[0] == ":init": self.init = {tuple(f) for f in sec[1:]}
            elif sec[0] == ":goal": self.goal = [tuple(f) for f in conj_to_list(sec[1])]

def subst(atom, binding):
    return tuple([atom[0]] + [binding.get(a, a) for a in atom[1:]])
