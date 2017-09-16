:- dynamic astar_expansions/1.
:- multifile holds/2.

%% A version of holds that will be used by A*
holds(F,List) :- is_list(List),member(F,List).

astar_is_goal(State) :-
    goal_state(G),
    \+ (member(F,G), \+ member(F,State)).

astar_action_cost(_,1).
astar_infinity(10000).

% gets the g value of the state
getG(State,G) :- term_hash(State,Key), recorded(Key,astar_node(State,G,_,_,_)),!.
getG(_,INF) :- astar_infinity(INF).

% records a state, its g-value and its situation. Heuristic function is computed unless the state was known.
recordState(State,G,Hist,H,Key) :-
    term_hash(State,Key),
    (recorded(Key,astar_node(State,_,H,_,_),Reference) ->
	 erase(Reference)
     ;
         astar_heuristic(State,H)),
    recorda(Key,astar_node(State,G,H,Hist,not_closed)).

astar_count_expansions :-
    astar_expansions(E),
    Ep is E+1,
    retract(astar_expansions(E)),
    assert(astar_expansions(Ep)).

astar_print_stats :-
    astar_expansions(Expansions),
    writef("A* expansions=%q",[Expansions]).

astar_clean_memory :-
    forall(recorded(K,astar_node(_,_,_,_,_),Ref),erase(Ref)),
    retractall(astar_expansions(_)).

astar(Plan) :-
    astar_clean_memory,
    astar_get_state(s0,State),
    recordState(State,0,s0,H,Key),
    assert(astar_expansions(0)),
    empty_heap(E),
    add_to_heap(E,H,State-Key,Open),
    astar_(Open,Plan).

%% astar(Open,Hist): is true when Hist is the history that achieves the goal.
astar_(Open,Plan) :-
    get_from_heap(Open,_,State-StateKey,Open2),
    recorded(StateKey,astar_node(State,G,H,Sit,Status),TermRef),
    (Status=closed ->
	 astar_(Open2,Plan)
     ;
         % following two lines mark this state as closed
         erase(TermRef),
         recorda(StateKey,astar_node(State,G,H,Sit,closed)),
     
         (astar_is_goal(State) ->
	      Plan=Sit,
	      astar_print_stats
	  ;
             astar_count_expansions,
	     %             astar_successors(Sit,SuccPairs),
	     astar_successors(State,Sit,SuccPairs),
             astar_insert(SuccPairs,G,Open2,NewOpen),
             astar_(NewOpen,Plan))).

astar_insert([],_,O,O).
astar_insert([[State,do(A,Sit)]|SuccPairs],ParentG,Open,NewOpen) :-
    astar_action_cost(A,ActionCost),
    getG(State,OldG),
    NewG is ParentG+ActionCost,
    (NewG < OldG ->
	 recordState(State,NewG,do(A,Sit),H,StateKey),
	 F is NewG+H,
	 add_to_heap(Open,F,State-StateKey,NextOpen)
     ;
         NextOpen=Open),
    astar_insert(SuccPairs,ParentG,NextOpen,NewOpen).

astar_successors(CurState,Hist,SuccPairs) :-
    findall([State,do(A,Hist)],(poss(A,CurState),astar_get_state(do(A,CurState),State)),SuccPairs).

astar_get_state(Situation,State) :- findall(F,holds(F,Situation),L), sort(L,State).
