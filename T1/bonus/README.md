# Bonus

Ejemplo de uso:

```prolog
$ swipl
?- [astar2,blocks].
Warning: /home/jabaier/cursos/ia/2017/tareas/t1_astar/astar2.pl:37:
	Singleton variables: [K]
true.

?- astar(Sit).
A* expansions=202
Sit = do(move(a, table, c), do(move(c, table, b), do(move(b, c, d), do(move(e, d, table), do(move(a, b, table), do(move(f, e, g), s0)))))).
```

Para entender el efecto de la heurística, abra el archivo `bloques.pl` y modifique la heurística que usa A* (`astar_heuristic`).