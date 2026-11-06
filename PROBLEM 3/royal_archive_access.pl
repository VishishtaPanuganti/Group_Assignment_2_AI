% Problem 3: Royal Archive Access Verification

% Step 1: Predicate logic representation
% Predicates: archivist/1, verifies/2, trusted/1, access/2,
% permitted/2, inspects/2, hidden_mark/2, stored/1, sealed/1.
% Constants: mira, scroll_7. Variables: X, R.

% Facts
archivist(mira).
access(mira, scroll_7).
inspects(mira, scroll_7).
hidden_mark(mira, scroll_7).
stored(scroll_7).

% Rules
trusted(X) :-
    archivist(X),
    verifies(X, _).

permitted(X, R) :-
    trusted(X),
    access(X, R).

verifies(X, R) :-
    inspects(X, R),
    hidden_mark(X, R).

sealed(R) :-
    stored(R).

% Step 2: Negation of the goal
% Goal: trusted(mira).
% Negated goal: not trusted(mira).

% Step 3: Implication removal
% A -> B becomes NOT A OR B.
% Example:
% archivist(X) AND verifies(X,R) -> trusted(X)
% becomes:
% NOT archivist(X) OR NOT verifies(X,R) OR trusted(X).

% Step 4: Negation movement
% Negations are moved inward using De Morgan's laws.

% Step 5: Standardization apart
% Variables in different clauses are independent.

% Step 6: Skolemization
% No existentially quantified variables are present,
% so no Skolem constants or functions are needed.

% Step 7: CNF clauses

cnf(c1, [neg(archivist(X)), neg(verifies(X, _)), pos(trusted(X))]).
cnf(c2, [neg(trusted(X)), neg(access(X, R)), pos(permitted(X, R))]).
cnf(c3, [neg(inspects(X, R)), neg(hidden_mark(X, R)), pos(verifies(X, R))]).
cnf(c4, [neg(stored(R)), pos(sealed(R))]).
cnf(c5, [pos(stored(scroll_7))]).
cnf(c6, [pos(access(mira, scroll_7))]).
cnf(c7, [pos(inspects(mira, scroll_7))]).
cnf(c8, [pos(hidden_mark(mira, scroll_7))]).
cnf(c9, [pos(archivist(mira))]).
cnf(c10, [neg(trusted(mira))]).

% Step 8: Resolution implementation

resolve_on(Atom, C1, C2, Result) :-
    select(pos(Atom), C1, Rest1),
    select(neg(Atom), C2, Rest2),
    append(Rest1, Rest2, Result).

resolve_on(Atom, C1, C2, Result) :-
    select(neg(Atom), C1, Rest1),
    select(pos(Atom), C2, Rest2),
    append(Rest1, Rest2, Result).

show_step(Number, C1, C2, Atom, Result) :-
    resolve_on(Atom, C1, C2, Result),
    format('Step ~w: ~w~n', [Number, Result]).

% Resolution refutation
prove :-
    nl,
    writeln('Royal Archive Resolution Refutation'),
    nl,

    % Ground instances of the clauses
    C3 = [neg(inspects(mira, scroll_7)),
          neg(hidden_mark(mira, scroll_7)),
          pos(verifies(mira, scroll_7))],

    C7 = [pos(inspects(mira, scroll_7))],
    C8 = [pos(hidden_mark(mira, scroll_7))],

    C1 = [neg(archivist(mira)),
          neg(verifies(mira, scroll_7)),
          pos(trusted(mira))],

    C9 = [pos(archivist(mira))],
    C10 = [neg(trusted(mira))],

    % Step 1: Resolve with inspection fact
    show_step(1, C3, C7,
              inspects(mira, scroll_7), R1),

    % Step 2: Resolve with hidden-mark fact
    show_step(2, R1, C8,
              hidden_mark(mira, scroll_7), R2),

    % Step 3: Resolve with negated goal
    show_step(3, C1, C10,
              trusted(mira), R3),

    % Step 4: Resolve with archivist fact
    show_step(4, R3, C9,
              archivist(mira), R4),

    % Step 5: Resolve complementary verification literals
    show_step(5, R4, R2,
              verifies(mira, scroll_7), R5),

    ( R5 = [] ->
        writeln('Empty clause [] derived.'),
        writeln('Contradiction found.'),
        writeln('Therefore, Mira is trusted.')
    ;
        writeln('Proof failed.')
    ).