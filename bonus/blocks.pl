%% blocks.pl
%% Description : A situation calculus-based planner/reasoner for blocksworld
%% Author      : Jorge Baier <jabaier@ing.puc.cl>
%% URL         : http://web.ing.puc.cl/~jabaier/blocks.pl 
%% Institution : Pontificia Universidad Católica de Chile, Chile
%% Copyright   : you choose
%% Warranties  : none


%% Object Declaration (problem-specific)
block(B) :- member(B,[a,b,c,d,e,f,g]).

%% Initial Situation (problem-specific)
holds(F,s0) :- member(F,
		      [on(a,b),on(b,c),on(c,table),
		       on(d,table),on(e,d),on(f,e),
		       on(g,table)]).

%% goal state
goal_state([on(b,d),on(c,b),on(a,c)]).

%% heuristics for A*
null_heuristic(_,0).
goal_counting(State,N) :-
    goal_state(Goal),
    findall(F,(member(F,Goal),\+ member(F,State)),L),
    length(L,N).

%%
%astar_heuristic(S,H) :- null_heuristic(S,H).
astar_heuristic(S,H) :- goal_counting(S,H).


%% Blocks World Preconditions (domain-specific)
poss(move(X,Y,Z),S) :-
    holds(on(X,Y),S),
    (Z=table; block(Z),\+ holds(on(_,Z),S)),
    X\=Z,Y\=Z,
    \+ holds(on(_,X),S).

%% Blocks World Effects (domain-specific)
is_negative_effect(move(X,Y,_),on(X,Y)).
is_positive_effect(move(X,_,Z),on(X,Z)).


%%%%% Situation Calculus Successor State Axiom a la Reiter (domain-independent)
holds(F,do(A,S)) :-
    holds(F,S),
    \+ is_negative_effect(A,F).

holds(F,do(A,_)) :-
    is_positive_effect(A,F).


%%%%% Legal Situations are those produced by executing
%%%%% generates situations in a breadth-first manner

legal(s0).
legal(do(A,S)) :-
    legal(S),
    poss(A,S).

% If you want to generate a plan use a query like
% legal(S),holds(on(b,a),S).
