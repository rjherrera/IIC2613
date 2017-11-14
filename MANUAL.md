# Tarea 2

**Raimundo Herrera Sufán - 14632152**

# Tabla de contenidos
1. [Archivos incluidos](#archivos-incluidos)
2. [Decisiones de diseño](#decisiones-de-diseño)
3. [Reentrenamiento](#reentrenamiento)
4. [Clasificación por imagen](#clasificación-por-imagen)
5. [Librerías requeridas](#librerías-requeridas)

---

## Archivos incluidos

Se incluye a continuación descripciones para conocer la utilidad de los archivos/directorios incluidos:

* En primer lugar se amplió el set de datos con el objetivo de tener una mayor variedad de imágenes por clase. También, para poder subsanar un requerimiento de parte del código utilizado, el cual consistía en tener al menos un número similar a 40 fotos por clase. Para la ampliación se utilizó el script [duplicator](duplicator.py), el cual utilizando la librería Pillow entrega, por cada imagen del set de datos, 5 imágenes nuevas, que consisten en modificaciones al contraste de las mismas, para simular distintas condiciones de luminosidad. Para ejecutarlo basta con ejecutar `python3 duplicator.py` en consola.

    **IMPORTANTE**: el archivo 'pasillos.txt' no debe estár en la carpeta 'datasets' (o en su defecto cualquier archivo que no sean los directorios e imágenes dentro de ellos).

* En segundo lugar, para entrenar se debe incluir bajo la carpeta [dataset](dataset) todas las imagenes ordenadas como fueron entregadas. El nombre de la carpeta ha de ser `dataset` en la raíz, las subcarpetas deben permanecer igual. El link para descargar el dataset exacto utilizado está en drive [dataset.zip](https://drive.google.com/file/d/1_0qAwVzN7fXdaISKlUxJgzvCDP9JTFSc/view?usp=sharing) y basta con descomprimirlo en la raíz del repositorio.

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
    * [test_files](test_files): imágenes externas al dataset en la carpeta misma, e imágenes sacadas del dataset bajo las subcarpetas [pasillo0](test_files/pasillo0) y [pasillo1](test_files/pasillo0), para tener coherencia con el archivo de input mencionado.

* Como extra, se incluye el archivo [retrain_stdout](retrain_stdout.txt) para tener registro de como se entrenó la red, y los scores tanto de los crossvalidation y entropy por step, como del accuracy final.


## Decisiones de diseño


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


