# -*- coding: utf-8 -*-
"""
Temporary script to investigate viability of the Microsoft COCO dataset. 
"""

from pycocotools.coco import COCO
import pandas as pd
import matplotlib.pyplot as plt
import os
import urllib.request
import zipfile

def main():

    url = 'http://images.cocodataset.org/annotations/annotations_trainval2017.zip'
    zip_path = 'annotations_trainval2017.zip'

    if not os.path.exists('annotations/instances_val2017.json'):
        print('Downloading annotations (~250 MB)...')
        urllib.request.urlretrieve(url, zip_path)
        print('Extracting...')
        with zipfile.ZipFile(zip_path) as z:
            z.extractall('.')
        print('Done')

    coco = COCO('annotations/instances_train2017.json')   # use instances_val2017.json for the small split

    rows = []
    for cat in coco.loadCats(coco.getCatIds()):
        img_ids = coco.getImgIds(catIds=[cat['id']])          # images containing this class
        ann_ids = coco.getAnnIds(catIds=[cat['id']], iscrowd=None)  # individual boxes of this class
        rows.append((cat['name'], len(img_ids), len(ann_ids)))

    df = pd.DataFrame(rows, columns=['class', 'num_images', 'num_instances'])
    df = df.sort_values('num_images', ascending=False).reset_index(drop=True)

    print(df.to_string())

    plt.figure(figsize=(14, 5))
    plt.bar(df['class'], df['num_images'])
    plt.xticks(rotation=90)
    plt.ylabel('Number of images')
    plt.title('COCO train2017: images per class')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()