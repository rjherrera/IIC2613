# Tarea 2

**Raimundo Herrera Sufán - 14632152**

# Tabla de contenidos
1. [Uso rápido](#uso-rápido)
2. [Archivos incluidos](#archivos-incluidos)
3. [Decisiones de diseño](#decisiones-de-diseño)
4. [Reentrenamiento](#reentrenamiento)
5. [Clasificación por imagen](#clasificación-por-imagen)
6. [Librerías requeridas](#librerías-requeridas)

---

## Uso rápido

Para ejecutar un testeo rápido del programa en cuestión (con las libreras especificadas en la sección [Librerías requeridas](#librerías-requeridas), basta con ejecutar:

```bash
python3 main.py -hf final_test.txt -nc 1
```

Más detalle sobre lo que significan los parámetros y archivos de la tarea en la siguiente sección, de modo que el uso de [main](main.py) también se explica con más detenimiento.

## Archivos incluidos

Se incluye a continuación descripciones para conocer la utilidad de los archivos/directorios incluidos:

* En primer lugar se amplió el set de datos con el objetivo de tener una mayor variedad de imágenes por clase. También se hizo para poder subsanar un requerimiento de parte del código utilizado, el cual consistía en tener al menos un número similar a 40 fotos por clase. Para la ampliación se utilizó el script [duplicator](duplicator.py), el cual entrega, por cada imagen del set de datos, 5 imágenes nuevas, que consisten en modificaciones al contraste de las mismas, para simular distintas condiciones de luminosidad, para lo cual se utilizó la librería Pillow. Para correrlo basta con ejecutar `python3 duplicator.py` en consola.

    **IMPORTANTE**: el archivo 'pasillos.txt' no debe estár en la carpeta 'datasets' (o en su defecto cualquier archivo que no sean los directorios e imágenes dentro de ellos).

* En segundo lugar, para entrenar se debe incluir bajo la carpeta [dataset](dataset) todas las imagenes ordenadas como fueron entregadas. El nombre de la carpeta ha de ser `dataset` en la raíz, las subcarpetas deben permanecer igual. El link para descargar el dataset exacto utilizado está en drive [dataset.zip](https://drive.google.com/file/d/1_0qAwVzN7fXdaISKlUxJgzvCDP9JTFSc/view?usp=sharing) y basta con descomprimirlo en la raíz del repositorio. Para más información sobre el reentrenamiento referirse a la [sección](#reentrenamiento) correspondiente.

* En tercer lugar, para entrenar se incluyen los scripts del modelo utilizado, que es el basado en estos dos tutoriales: [How to Retrain Inception's Final Layer for New Categories](https://www.tensorflow.org/tutorials/image_retraining) y [TensorFlow For Poets](https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/). Esto se hace bajo la carpeta [classifier](classifier). Ahí se encuentran los archivos principales. Se deben utilizar para reentrenar la red y/o para clasificar imágenes de a una, sin embargo, como en la raíz se incluye otro programa que se aprovecha de los archivos, estos no deberían tocarse.

* En cuarto lugar se incluye el archivo [hallway](hallway.py), el cual es el archivo que realiza la clasificación final en pasillos. El flujo es muy simple, toma el archivo [pasillos](pasillos.txt) y genera vectores con cada fila. Estos vectores tienen 71 coordenadas (1 por cada clase, es decir, arroz1, aceite10, sal2, etc.), donde cada una es 1 o 0 según si se corresponde a una de esas clases. Luego, toma la fila nueva a clasificar, hace el mismo mapeo a vector y clasifica.

* En quinto lugar, está el archivo principal [main](main.py). Este archivo "wrappea" todos los avances anteriores, de modo que corresponde a el programa final. Este programa recibe un archivo de texto, cuyas lineas corresponden a las ubicaciones de imágenes que componen un potencial pasillo. Luego, para cada linea se ejecuta el clasificador de TensorFlow para obtener la clase a la que se predice que pertenece cada imagen. Una vez que se tienen las clases de todas las imágenes, se introduce este output como input para el KNN mencionado anteriormente, el cual finalmente entrega el pasillo correspondiente. Este archivo recibe 3 argumentos por linea de comandos:

    ```bash
    python3 main.py -hf <input_file> -nc <number_of_classes> -sd <show_distance>
    ```

    Donde `-hf` es el shortcut para `--hallway_file` correspondiente al archivo de input descrito anteriormente, es obligatirio. Luego `-nc` es el shortcut para `--n_classes` correspondiente a la cantidad de clases que se desean mostrar en el momento de clasificar una imagen, es opcional, y por defecto se muestran 3 con su porcentaje de certeza respectivo. Finalmente `-sd` es el shortcut para `--show_distance` correspondiente a si se desea mostrar la distancia _minkowski_ existente entre el vector a predecir y el elegido como vecino más cercano al realizar el KNN, es opcional, por defecto no se muestra.

* En sexto lugar, bajo la carpeta [classifier_files](classifier_files) se incluyen los datos del modelo una vez entrenado. Se omiten (en el .gitignore) muchos de los archivos generados en esta carpeta, y solo se incluyen los archivos principales del modelo entrenado: [retrained_graph](classifier_files/retrained_graph.pb) (usando git LFS) que es el archivo que guarda el modelo en sí, y es utilizado para las predicciones, y [retrained_labels](classifier_files/retrained_labels.txt) que tiene los nombres de las clases, es decir los nombres de las carpetas.

* En séptimo lugar se incluyen unos pocos archivos para hacer testeo del programa:
    * [final_test](final_test.txt): archivo para ser utilizado como _input_file_ del archivo principal
    * [test_files](test_files): imágenes externas al dataset en la carpeta misma, e imágenes sacadas del dataset bajo las subcarpetas [pasillo0](test_files/pasillo0) y [pasillo1](test_files/pasillo1), para tener coherencia con el archivo de input mencionado.

* Como extra, se incluye el archivo [retrain_stdout](retrain_stdout.txt) para tener registro de como se entrenó la red, y los scores tanto de los crossvalidation y entropy por step, como del accuracy final (al final del archivo).


## Decisiones de diseño

A la hora de optar por que utilizar en esta tarea, decidí investigar sobre cuales eran los mejores rendimientos en clasificación de imágenes, y cuales eran los sistemas ms robustos existentes. Un amigo había preguntado en clases al profesor si se podía utilizar Transfer Learning, y ante su afirmativa respuesta decidí, cuando me salieron positivas respuestas sobre eso en mi búsqueda, que era una buena opción a analizar.

La base de la decisión es que los modelos realmente robustos de clasificación de imágenes toman mucho tiempo de entrenamiento y ya han sido entrenados por otras personas, como es este caso utilizando sets de categorías como ImageNet. Con la técnica de Transfer Learning, se puede aprovechar eso y modificar únicamente los parámetros deseados ya que se entrena únicamente la última capa, sin modificar nada de lo anterior. El modelo de entrenamiento en el que se basa el sistema escogido es InceptionV3 [(referencia)](https://www.tensorflow.org/tutorials/image_recognition), el cual, a grandes rasgos consiste de una red neuronal profunda de tipo convolucional (_deep cnn_), validada contra el set de categorías mencionado anteriormente.

La razón por la cual Transfer Learning funciona, en términos simples, es porque es muy probable que la información obtenida al entrenar una red para clasificar entre más de 1000 categorías es normalmente útil para nuevos tipos de objetos a clasificar, por lo que con reentrenar la última capa normalmente se obtienen buenos resultados. Se entrena por medio de la creación de _bottlenecks_, los cuales corresponden a los parámetros de la penúltima capa para cada imagen.

Para evitar _overfitting_, el programa utilizado, basado en el link provisto anteriormente [TensorFlow For Poets](https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/), realiza _crossvalidation_ y realiza 4000 pasos para entrenar la última capa, tomando en cada uno de ellos aleatoriamente 10 imagenes y comparando la predicción del modelo sobre ellas con el etiquetado real, para así actualizar por _backpropagation_ los pesos de la última capa, obteniendo también así los scores para cada paso, mejorando sustancialmente cada iteración. Este método de evaluación, se dice en la documentación, es de lo mejor en cuanto a una predicción de los resultados reales que tendrá el modelo.

Como se recomienda en los tutoriales realizados, cambié tanto el modelo en el cual basarme, como ciertos parámetros para el reentrenamiento. El primer modelo probado fue el de MobileNet y con 500 pasos, este era el setup recomendado para un análisis lightweight del problema, sin embargo, si bien los resultados eran buenos, no eran tan buenos como se podía esperar de un modelo tan robusto. También se probó con otros steps, el recomendado de 4000, y con otro modelo, con varios steps. Finalmente se optó por el que obtena mejor rendimiento, InceptionV3 con 4000 steps (el recomendado por el tutorial). Además se optó por el mismo ya que fue el único que fue capaz de clasificar correctamente imagenes de Google como las provistas en la carpeta [test_files](test_files), donde destaca el caso del [arroz líder](test_files/arroz_lider.jpg) ya que siendo un elemento con colores distintos y bastante diferente de los arroces presentes en el dataset, es capaz de catalogarlo correctamente (aún cuando la seguridad del clasificador sea bastante poca.

El accuracy total obtenido tras reentrenar la red con las categorías de la tarea, es de un 99.1%.

Para la parte final, es decir la de la clasificación en pasillos, se optó por conectar el modelo anterior con un clasificador no supervisado, el KNN. Lo que se hizo a grandes rasgos es clasificar cada imagen de las entregadas como input en una categora, y con esto, entregar un input al KNN para que este decidiera, en base a los pasillos entregados en el archivo [pasillos.txt](pasillos.txt), determinara cual es el mejor fit para dicho "candidato a pasillo". 

El KNN se configuró simplemente entregándole un vector por cada fila del documento, donde el vector tiene 71 entradas, correspondientes a los 71 tipos de alimentos (arroz1, aceite4, etc.), y cada entrada representa si ese alimento está en esa fila (que representa un pasillo) o no, con un 1 en el caso de estar y un 0 en caso contrario. Esos 55 vectores son bastante sparse, ya que cuentan con alrededor de 6 valores positivos (1) y por ende alrededor 65 negativos (0).

Para clasificar se realiza la misma transformación para este candidato a pasillo (siendo cada elemento de esta "fila" la predicción del modelo anterior), y se _fittea_ al modelo KNN, de modo que entregue un resultado, que es un pasillo que tiene la distancia _minkowskiana_ mínima a un pasillo real representado por el tranining-set del modelo. La distancia de _Minkowski_ suele ser una mejor medida cuando se habla de una métrica usada en espacios de mayor dimensión, y constituye de cierto modo una generalización entre distancia _Manhattan_ y _Euclideana_.

## Reentrenamiento

Para reentrenar basta con ubicarse en la raíz del repositorio y ejecutar:

```bash
python3 -m classifier.retrain  --bottleneck_dir=classifier_files/bottlenecks --model_dir=classifier_files/models/ --summaries_dir=classifier_files/training_summaries/inceptionv3 --output_graph=classifier_files/retrained_graph.pb --output_labels=classifier_files/retrained_labels.txt --image_dir=dataset
```

Considerando que los archivos generados no serán commiteados al repositorio, excepto los dos importantes, de los cuales 1 será manejado por git LFS. Es importante ya haber obtenido el dataset del link provisto anteriormente.

## Clasificación por imagen

Para poder clasificar una imagen en alguna de las clases, sin tener que pasarle al programa principal un archivo con pasillos, es posible utilizar uno de los scripts incluidos en la carpeta anteriormente mencionada, para esto basta con estar en la raíz y ejecutar:

```bash
python3 -m classifier.label_image --graph=classifier_files/retrained_graph.pb --labels=classifier_files/retrained_labels.txt --input_layer="Mul" --input_width=299 --input_height=299 --image=<image_to_classify>
```

Donde basta con reemplazar `<image_to_classify>` por la imagen deseada para ver su categorización.

## Librerías requeridas

* TensorFlow
* Pillow
* Numpy
* Scikit-learn
* Scipy

Se incluye un archivo [requirements](requirements.txt) consistente con el virtual env utilizado para el desarrollo de la tarea.


