from PIL import Image
import os

def create_duplicates():
    for folder in [x for x in os.listdir('dataset') if x != '.DS_Store']:
        for image in (x for x in os.listdir('dataset/' + folder) if x != '.DS_Store'):
            path = 'dataset/' + folder + '/' + image
            name, extension = os.path.splitext(path)
            change_contrast_multi(Image.open(path), [-50, 50, 100, 150, 200], name)


def change_contrast(img, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))
    def contrast(c):
        value = 128 + factor * (c - 128)
        return max(0, min(255, value))
    return img.point(contrast)

def change_contrast_multi(img, steps, output):
    width, height = img.size
    canvas = Image.new('RGB', (width, height))
    for n, level in enumerate(steps):
        img_filtered = change_contrast(img, level)
        canvas.paste(img_filtered, (0, 0))
        canvas.save('%s_%s.png' % (output, n), 'PNG')

# basado en el código proporcionado en: https://stackoverflow.com/a/42054155

if __name__ == '__main__':
    create_duplicates()