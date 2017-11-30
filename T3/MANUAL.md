# Tarea 3

**Raimundo Herrera Sufán - 14632152**

# Tabla de contenidos
1. [Uso rápido](#uso-rápido)
2. [Archivos incluidos](#archivos-incluidos)
3. [Función objetivo](#función-objetivo)
4. [Librerías requeridas](#librerías-requeridas)

---

## Uso rápido

Para ejecutar un testeo rápido del programa en cuestión (con las libreras especificadas en la sección [Librerías requeridas](#librerías-requeridas), basta con ejecutar:

```bash
python3 tarea3.py test.txt
```

Más detalle sobre la ejecución y ciertos parámetros que pueden facilitar la corrección, junto con la descripción de archivos, se encuentra en la siguiente sección.

## Archivos incluidos

Se incluye a continuación descripciones para conocer la utilidad de los archivos incluidos:

* En primer lugar se incluye un archivo principal de ejecución de la tarea, el archivo [tarea3](tarea3.py). En este archivo se hace la lógica de lectura de los datos de entrada, junto con el _parseo_ de los argumentos. Además se inicializa el grafo de computo importado desde otro archivo, se realiza el descenso de gradiente y se imprime un resumen. Adicionalmente se incluye un código muy simple para _plotear_ los datos cuando sea pertinente verlos (se hizo para 2D), junto con la recta obtenida tras el descenso de gradiente. Esto con el fin de poder ver si lo que estaba haciendo daba resultados coherentes.

  Los parámetros que se pueden setear sin modificar el archivo son 2, el primero corresponde a si se desea o no mostrar un gráfico tras finalizar. El segundo corresponde al nivel de información que se desea imprimir, teniendo 3 posibilidades, la primera, de valor 0 cuando se desea imprimir información de debuggeo para ver pasos intermedios de la tarea; la segunda de valor 1 cuando se desea mostrar la información por mini-batch y epochs (es la que se setea por defecto); en 2 cuando solo se desean mostrar valores esenciales, es decir un print al principio, otro al final y un resumen.

    Para usar los parámetros:

    ```bash
    python3 tarea3.py test.txt --show_plot --log_level <numero>
    ```

    Donde por el hecho de incluir el _flag_ `show_plot` se mostrará un gráfico simple. Y `numero` ha de ser reemplazado por 0, 1 o 2. Recordar que ambos parámetros son opcionales y que la tarea funciona con la ejecución por defecto descrita al principio.

* En segundo lugar se incluye el archivo [graph](graph.py) que tiene toda la lógica del grafo de cómputo y del backpropagation. Este archivo a resumidas cuentas cuenta con la estructura de clases para cada _gate_ utilizada, junto con sus respectivos _backward_ y _forward_ para cada uno, y el caso global o de toda la "red", donde se puede observar el procedimiento de backpropagation, incluido dentro de la clase `ComputationalGraph`.

  Este archivo tiene las compuertas utilizadas, las cuales son 5, de suma, multiplicación, producto punto, máximo y sumatoria. Se trabaja en base a lo hecho en clases, mostrado por el profesor en sus ejemplos de backpropagation, usando la idea de Gates, Units, backward y forward.

* En tercer lugar se incluye un archivo de [test](test.txt) compartido por Freddie Venegas, el cual se puede probar con el programa y de hecho es el ejecutado por defecto.

* Finalmente el archivo de utilidades [utils](utils.py) el cual únicamente contiene una clase que corresponde a la implenentación de una modificación de `print`, realizada con el objetivo de poder tener distintos niveles de registro de información al hacer el output.

## Función objetivo

Al ser un SVM soft-margin, la función objetivo (F.O.) es la descrita en el enunciado de la tarea. Sin embargo, para poder realizar la minimización como era requerido, había que sacar las restricciones del problema y llevarlas a la F.O. Mi primer approach fue usar el _lagrangiano_ y el dual, pero el profesor aclaró que no era lo buscado.

Después el approach al que llegué usando el primal fue el de reemplazar los epsilon del segundo término de la F.O. por lo obtenido de transformar en igualdad la restricción, es decir, `1 - y(w·x + b)` para cada _i_. Luego, como existe la restricción de que los epsilon deben ser positivos, esa restricción combinada con la transformación anterior, convierte el segundo término en una sumatoria sobre _i_ del `max(0, 1 - y(w·x + b))`.

Con eso en mente, el problema en cuestión se convierte en la minimización de la norma al cuadrado de `w` ponderado por `lambda/2` más la sumatoria anteriormente explicada. En base a eso se construyó el grafo de cómputo.


## Librerías requeridas

* Numpy
* Matplotlib (opcional)

Como el _ploteo_ es un adicional, basta con no utilizar el flag para que la librería no se importe ni utilice.
