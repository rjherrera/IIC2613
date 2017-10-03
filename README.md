# Tarea 1 - Bloques Cooperativos y Competitivos

**Semestre:** 2017, Segundo semestre

**Entrega:** 2 de Octubre, hasta las 23:59.

**Nombre:** Raimundo Herrera

---

| Parte 1 | Parte 2 | Bonus |
| ------- | ------- | ----- |
| Si      | Si      | No    |

## Tests

Para esta parte hice los tests entregados, bajo la situación inicial de 7 bloques.

```prolog
%% Object Declaration (problem-specific)
block(B) :- member(B,[a,b,c,d,e,f,g]).

color(rob, B) :- member(B, [blue]).
color(bor, B) :- member(B, [red]).

%% Initial Situation (problem-specific)
holds(F,s0) :- member(F,[clear(a),on(a,b),on(b,c),ontable(c),ontable(d),on(e,d),on(f,e),clear(f),ontable(g),clear(g)]).
holds(color(B,white),s0) :- block(B).
```

### Parte 1

```prolog
?- time((legal(S),holds(on(b,d),S),holds(on(c,b),S),holds(on(a,c),S))).
% 247,833,541 inferences, 26.293 CPU in 26.871 seconds (98% CPU, 9425795 Lips)
S = do(move_to_block(a, c), do(move_to_block(c, b), do(move_to_block(b, d), do(move_to_block(e, f), do(move_to_table(f), do(move_to_block(a, g), s0)))))) ;
% 7,594,304 inferences, 0.797 CPU in 0.804 seconds (99% CPU, 9532045 Lips)
S = do(move_to_block(a, c), do(move_to_block(c, b), do(move_to_block(b, d), do(move_to_table(e), do(move_to_table(f), do(move_to_block(a, g), s0)))))) 
```


```prolog
?- time((legal(S),holds(color(d,blue),S),holds(on(b,d),S),holds(color(b,red),S),holds(ontable(d),S))).
% 4,441,787,940 inferences, 445.954 CPU in 451.800 seconds (99% CPU, 9960199 Lips)
S = do(move_to_block(b, d), do(paint(bor, b, red), do(paint(rob, d, blue), do(move_to_table(b), do(move_to_block(e, f), do(move_to_block(f, a), do(move_to_block(a, g), s0))))))) ;
% 235,923 inferences, 0.033 CPU in 0.035 seconds (95% CPU, 7200678 Lips)
S = do(move_to_block(b, d), do(paint(rob, d, blue), do(paint(bor, b, red), do(move_to_table(b), do(move_to_block(e, f), do(move_to_block(f, a), do(move_to_block(a, g), s0))))))) 
```

```prolog
?- time((legal(S),holds(color(c,blue),S),holds(on(b,c),S),holds(color(b,red),S),holds(color(d,red),S))).
% 147,185,614 inferences, 13.890 CPU in 14.155 seconds (98% CPU, 10596658 Lips)
S = do(move_to_block(b, c), do(paint(bor, b, red), do(paint(bor, d, red), do(paint(rob, c, blue), do(move_to_table(b), do(move_to_block(a, f), s0)))))) ;
% 87,775 inferences, 0.014 CPU in 0.014 seconds (99% CPU, 6327038 Lips)
S = do(paint(bor, d, red), do(move_to_block(b, c), do(paint(bor, b, red), do(paint(rob, c, blue), do(move_to_table(b), do(move_to_block(a, f), s0)))))) 
```

### Parte 2

```prolog
?- time((plies(Actions,SitSet),holdsAll(color(c,blue),SitSet))).
% 1,693,616 inferences, 0.170 CPU in 0.173 seconds (98% CPU, 9964323 Lips)
Actions = [move_to_block(a, f), move_to_block(b, a), paint(rob, c, blue)],
SitSet = [do(paint(rob, c, blue), do(move_to_block(b, a), do(move_to_block(a, f), s0))), do(paint(rob, c, blue), do(move_to_block(b, a), do(paint(bor, c, red), do(move_to_block(a, f), s0)))), do(paint(rob, c, blue), do(move_to_block(b, a), do(paint(bor, d, red), do(move_to_block(a, f), s0)))), do(paint(rob, c, blue), do(move_to_block(b, a), do(paint(bor, g, red), do(move_to_block(a, f), s0)))), do(paint(rob, c, blue), do(paint(bor, c, red), do(move_to_block(b, a), do(move_to_block(..., ...), s0)))), do(paint(rob, c, blue), do(paint(bor, c, red), do(move_to_block(..., ...), do(..., ...)))), do(paint(rob, c, blue), do(paint(..., ..., ...), do(..., ...))), do(paint(..., ..., ...), do(..., ...)), do(..., ...)|...] ;
% 293,657 inferences, 0.040 CPU in 0.042 seconds (95% CPU, 7429840 Lips)
Actions = [move_to_block(a, f), move_to_block(b, g), paint(rob, c, blue)],
SitSet = [do(paint(rob, c, blue), do(move_to_block(b, g), do(move_to_block(a, f), s0))), do(paint(rob, c, blue), do(move_to_block(b, g), do(paint(bor, c, red), do(move_to_block(a, f), s0)))), do(paint(rob, c, blue), do(move_to_block(b, g), do(paint(bor, d, red), do(move_to_block(a, f), s0)))), do(paint(rob, c, blue), do(move_to_block(b, g), do(paint(bor, g, red), do(move_to_block(a, f), s0)))), do(paint(rob, c, blue), do(paint(bor, c, red), do(move_to_block(b, g), do(move_to_block(..., ...), s0)))), do(paint(rob, c, blue), do(paint(bor, c, red), do(move_to_block(..., ...), do(..., ...)))), do(paint(rob, c, blue), do(paint(..., ..., ...), do(..., ...))), do(paint(..., ..., ...), do(..., ...)), do(..., ...)|...] .
```

Creo que hay un bug, me di cuenta muy tarde, que se come unos pasos.

### Extras P1

Corrí unos cuantos tests del issue [#2](https://github.com/IIC2613/Syllabus/issues/2), solo con una ejecución por test.

```prolog
?- time((legal(S),holds(on(b,d),S),holds(on(c,b),S),holds(on(a,c),S))).
% 247,833,474 inferences, 22.176 CPU in 22.211 seconds (100% CPU, 11175609 Lips)
S = do(move_to_block(a, c), do(move_to_block(c, b), do(move_to_block(b, d), do(move_to_block(e, f), do(move_to_table(f), do(move_to_block(a, g), s0)))))) .
```

```prolog
?- time((legal(S),holds(color(d,blue),S),holds(on(b,d),S),holds(color(b,red),S),holds(ontable(d),S))).
% 4,441,787,940 inferences, 403.827 CPU in 407.541 seconds (99% CPU, 10999225 Lips)
S = do(move_to_block(b, d), do(paint(bor, b, red), do(paint(rob, d, blue), do(move_to_table(b), do(move_to_block(e, f), do(move_to_block(f, a), do(move_to_block(a, g), s0))))))) .
```

```prolog
?- time((legal(S),holds(color(c,blue),S),holds(on(b,c),S),holds(color(b,red),S),holds(color(d,red),S))).
% 147,185,614 inferences, 14.122 CPU in 14.304 seconds (99% CPU, 10422193 Lips)
S = do(move_to_block(b, c), do(paint(bor, b, red), do(paint(bor, d, red), do(paint(rob, c, blue), do(move_to_table(b), do(move_to_block(a, f), s0)))))) .
```


## Dificultades y sugerencias

En la parte 1 creo que faltó explicitar que había que hacer los effects para paint, ya que como se decía explcitamente "complete esto, complete lo otro", uno pensaba que no había que completar algo más, pero claro, no es la gracia que a uno le digan todo. En la parte 2, me costó un poco entender que era lo pedido en cuanto al plies, quizás vendría bien una explicación más extensa, el turn se entiende bien, los possAll y holdsAll también. 
