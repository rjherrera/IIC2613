from classifier.label_image import *
from hallway import *

# files = ['test_files/arroz_lider.jpg', 'test_files/arroz_bonanza.jpg', 'test_files/vinagre_traverso.jpg',
#          'test_files/cereal_bar.jpg']
N_CLASSES = 3
SHOW_DISTANCE = False

parser = argparse.ArgumentParser()
parser.add_argument('-hf', '--hallway_file', help='File with hallway candidates (one per line), to classify')
parser.add_argument('-nc', '--n_classes', type=int, help='Amount of top classes to show when classifying a product')
parser.add_argument('-sd', '--show_distance', action='store_true',
                    help='Show the minkowski distance from the prediction vector to the neighbor chosen.')
args = parser.parse_args()

if not args.hallway_file:
    print('You must specify a file to test. Execute with -h for more information.')
    sys.exit(0)
input_file = args.hallway_file

if args.n_classes:
    N_CLASSES = args.n_classes

if args.show_distance:
    SHOW_DISTANCE = True

with open(input_file) as f:
    rows = [i.strip().split(',') for i in f]

# Product Classifier
model_file = 'classifier_files/retrained_graph.pb'
label_file = 'classifier_files/retrained_labels.txt'
input_height = 299
input_width = 299
input_mean = 128
input_std = 128
input_layer = 'Mul'
output_layer = 'final_result'

graph = load_graph(model_file)
for files in rows:
    output_classes = []
    print('-' * 60)
    for file_name in files:
        t = read_tensor_from_image_file(file_name,
                                        input_height=input_height,
                                        input_width=input_width,
                                        input_mean=input_mean,
                                        input_std=input_std)

        input_name = 'import/' + input_layer
        output_name = 'import/' + output_layer
        input_operation = graph.get_operation_by_name(input_name);
        output_operation = graph.get_operation_by_name(output_name);

        with tf.Session(graph=graph) as sess:
            results = sess.run(output_operation.outputs[0],
                               {input_operation.outputs[0]: t})
        results = np.squeeze(results)

        top_k = results.argsort()[-N_CLASSES:][::-1]
        labels = load_labels(label_file)
        output_classes += [labels[top_k[0]]]
        print('Top %d classes for %r:' % (N_CLASSES, file_name))
        for i in top_k:
            print('\t' + labels[i] + ':', results[i])

    # Hallway KNN
    print('\n############# ANSWER #############')
    # print('Prediction for %r -> %r:' % (files, output_classes))
    sample = list(map(lambda x: 1 if x in output_classes else 0, clases))
    distance, index = neighbors.kneighbors([sample])
    print('\tInput: %r' % ','.join(files))
    print('\tHallway:', hallways[index[0][0]][0])
    if SHOW_DISTANCE:
        print('\tDistance:', distance[0][0])
    print('############# ANSWER #############\n')