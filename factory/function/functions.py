import math
from collections import Counter
from ast import literal_eval
import random

import os
from PIL import Image
from flask import url_for, current_app
import uuid

def counter_cosine_similarity(c1, c2):
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)


def length_similarity(c1, c2):
    lenc1 = sum(c1.values())
    lenc2 = sum(c2.values())
    return min(lenc1, lenc2) / float(max(lenc1, lenc2))

def similarity_score(l1, l2):
    c1, c2 = Counter(l1), Counter(l2)
    return length_similarity(c1, c2) * counter_cosine_similarity(c1, c2)


def get_list(string):
    a = [i.split('/')[-1] for i in literal_eval(string)]
    return a

def get_rand_question(sqllist, sentlist):

    random_val = random.choice(sqllist)

    if random_val in sentlist:
        return get_rand_question(sqllist, sentlist)

    return random_val


def check_containing(sql, sent):
    return set(sent).issubset(sql)


def add_pic(picture_upload, location, width, height):
    
    filename = picture_upload.filename
    
    ext_type = filename.split('.')[-1]
    storage_filename = str(uuid.uuid4()) + '.' + ext_type

    filepath = os.path.join(current_app.root_path, 'static/'+location, storage_filename)

    output_size = (width, height)

    pic = Image.open(picture_upload)
    pic.thumbnail(output_size)

    pic.save(filepath)

    return storage_filename