%% Object Declaration (problem-specific)
block(B) :- member(B,[a,b,c,d,e,f,g]).

color(rob, B) :- member(B, [blue]).
color(bor, B) :- member(B, [red]).

%% Initial Situation (problem-specific)
holds(F,s0) :- member(F,[clear(a),on(a,b),on(b,c),ontable(c),ontable(d),on(e,d),on(f,e),clear(f),ontable(g),clear(g)]).
holds(color(B,white),s0) :- block(B).

%% %% Object Declaration (problem-specific)
%% block(B) :- member(B,[a,b,c,d]).

%% % colors available for rob and bor
%% color(rob,B) :- member(B,[blue]).
%% color(bor,B) :- member(B,[red]).

%% %% Initial Situation (problem-specific)
%% holds(F,s0) :- member(F,[on(a,b),on(b,c),ontable(c), ontable(d), clear(a), clear(d)]).
%% holds(color(B,white),s0) :- block(B).


poss(move_to_block(X,Z),S) :-
    holds(clear(X),S),
    holds(clear(Z),S),
    X\=Z
.

poss(move_to_table(X),S) :-
    holds(clear(X),S),
    \+ holds(ontable(X),S).

poss(paint(rob,B,C),S) :-
    color(rob,C),
    holds(clear(B), S)
.

poss(paint(bor,B,C),S) :-
    color(bor,C),
    holds(ontable(B), S)
.

%% Blocks World Preconditions (domain-specific)
%% action move_to_block(X,Z) moves block X on top of block Z


%% Blocks World Effects (domain-specific)
% is_conditional_negative_effect(Act,Cond,Fact)
% when Act is peformed and Cond holds, Fact becomes false
% is_conditional_positive_effect(Act,Cond,Fact)
% when Act is peformed and Cond holds, Fact becomes true

% block
is_conditional_negative_effect(move_to_block(X, _),on(X, Y),on(X, Y)).
is_conditional_negative_effect(move_to_block(X, _),ontable(X),ontable(X)).
is_conditional_negative_effect(move_to_block(_, Z),true,clear(Z)).
% table
is_conditional_negative_effect(move_to_table(X), on(X, Y), on(X, Y)).
% paint
is_conditional_negative_effect(paint(_, B, _), true, color(B, white)).


% block
is_conditional_positive_effect(move_to_block(X, Z), true, on(X, Z)).
is_conditional_positive_effect(move_to_block(X, _), on(X, Y), clear(Y)).
% table
is_conditional_positive_effect(move_to_table(X), on(X, Y), clear(Y)).
is_conditional_positive_effect(move_to_table(X), true, ontable(X)).
% paint
is_conditional_positive_effect(paint(_, B, C), true, color(B, C)).



holds(true,s0). % "true" always holds

holds(F,do(A,S)) :-
    holds(F,S),
    \+ (is_conditional_negative_effect(A,C,F), holds(C,S)).

holds(F,do(A,S)) :-
    is_conditional_positive_effect(A,C,F),holds(C,S).

% S is legal if it is the result of performing executable actions
legal(s0).
legal(do(A,S)) :-
    legal(S),
    poss(A,S).

% PART 2

controllable(A) :- member(A,[move_to_block(_,_),
                             move_to_table(_),
                             paint(rob,_,_)]).

uncontrollable(A) :- member(A,[paint(bor,_,_)]).

% possAll(Action,SituationSet)
% is true when poss(Action,S) holds for every S in SituationSet
%% possAll(Action, SitSet):- findall(S, poss(Action,S), SitSet).
possAll(_, []).
possAll(Action, [S|R]):- poss(Action, S), possAll(Action, R).

% holdsAll(F,SituationSet)
% is true when holds(F,S) is true for every S in Situation Set
%% holdsAll(F, SitSet):- findall(S, holds(F, S), SitSet).
holdsAll(_, []).
holdsAll(F, [S|R]):- holds(F, S), holdsAll(F, R).


% turn(agent, Actions, NewActions, SitSet, NewSitSet)
% assumes the agent has reached SitSet by
% applying the actions Actions in s0. It is true if there
% is a single action A that is possible in all situations SitSet
% NewSitSet contains the situations of the form do(A,S) for every
% S in SitSet.

turn(agent,Actions,NewActions,SitSet,SitSet2):-
    possAll(A, SitSet),
    controllable(A),
    findall(do(A, S),
            member(S, SitSet),
            SitSet2),
    append(Actions, [A], NewActions).

% turn(env,SitSet,SitSet2)
% SitSet2 c
turn(env,SitSet,SitSet2) :-
    findall(do(A, S),
            (possAll(A, SitSet),uncontrollable(A),member(S, SitSet)),
            SitSetWithAction),
    %append because env may do nothing.
    append(SitSet, SitSetWithAction, SitSet2)
.

plies([],[s0]).
plies(Actions,SitSet) :-
    plies(Acts,SS),
    turn(agent,Acts,Actions,SS,SitSetp),
    turn(env, SitSetp, SitSet)
.


