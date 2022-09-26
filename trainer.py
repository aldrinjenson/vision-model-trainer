import fastbook
from fastai import *
from fastbook import *
from fastai.vision.all import *
from fastai.vision.widgets import *
import os


def train():
    print("inside train function")
    path = os.path.join(os.getcwd(), 'images')
    dls = ImageDataLoaders.from_folder(path, item_tfms=Resize(
        128), batch_tfms=aug_transforms(), valid_pct=0.2, seed=23, bs=16)
    dls.valid_ds.items[:3]

    learn = vision_learner(dls, resnet34, metrics=accuracy)
    print("going to learn")
    learn.fine_tune(5)

    cwd = os.getcwd()
    print(cwd)
    learnPath = Path(cwd+'/predictor')
    print(learnPath)
    learn.path = learnPath

    learn.export()
    print("Model exported")

    # learn_inf = load_learner('export.pkl')
    # print("Class Labels: ", learn_inf.dls.vocab)
    return "New Model trained"
