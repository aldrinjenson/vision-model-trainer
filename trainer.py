import fastbook
from fastai import *
from fastbook import *
from fastai.vision.all import *
from fastai.vision.widgets import *
import os


os.getcwd()
os.path.join(os.getcwd(), 'images')


path = os.path.join(os.getcwd(), 'images')
dls = ImageDataLoaders.from_folder(path, item_tfms=Resize(
    128), batch_tfms=aug_transforms(), valid_pct=0.2, seed=23, bs=16)
dls.valid_ds.items[:3]


dls.show_batch()

exit(0)
# learn = vision_learner(dls, resnet34, metrics=accuracy)
learn.fine_tune(5)


interp = ClassificationInterpretation.from_learner(learn)
interp.plot_top_losses(5, nrows=1)


cleaner = ImageClassifierCleaner(learn)
cleaner


# deleteFromCleaner()
# moveFromCleaner()


# def deleteFromCleaner():
#     deletedFiles = []
#     for idx in cleaner.delete():
#         try:
#             cleaner.fns[idx].unlink()
#             deletedFiles.append((cleaner.fns[idx], idx))
#         except:
#             print("Error in deleting")
#     print(len(deletedFiles), " files deleted")


# def moveFromCleaner():
#     movedFiles = []
#     for idx, cat in cleaner.change():
#         target = path+'/'+cat
#         try:
#             shutil.move(str(cleaner.fns[idx]), target)
#             print('File not found error')
#     print(len(movedFiles), " files moved")


uploader = widgets.FileUpload()
uploader


img = PILImage.create(uploader.data[0])
actor, s, probs = learn.predict(img)
print(actor, s, probs)
print(f"AI says that this is: {actor}.")
print(f"Probability it's {actor}: {probs[1].item():.6f}")


cwd = os.getcwd()
print(cwd)
learnPath = Path(cwd)
print(learnPath)
learn.path = learnPath


learn.export()


path = Path()
path.ls(file_exts='.pkl')


learn_inf = load_learner('export.pkl')


uploader = widgets.FileUpload()
uploader


img = PILImage.create(uploader.data[0])
actor, _, probs = learn_inf.predict(img)
print(f"AI says that this is: {actor}.")
print(f"Probability it's {actor}: {probs[1].item():.6f}")


img = PILImage.create(uploader.data[0])
learn_inf.predict(img)


learn_inf.dls.vocab
