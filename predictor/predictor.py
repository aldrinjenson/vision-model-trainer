from fastai.vision.all import *
import gradio as gr

title = "Remember your memories"
description = "Try taking a photo and see if it rings a bell!"
article = "<p style='text-align: center'><a href='https://aldrinjenson.me' target='_blank'>Created by Aldrin Jenson</a></p>"
examples = []
interpretation = 'default'
enable_queue = True


def predict(img):
    learn = load_learner('export.pkl')
    labels = learn.dls.vocab
    img = PILImage.create(img)
    pred, pred_idx, probs = learn.predict(img)
    print("New prediction made")
    return {labels[i]: float(probs[i]) for i in range(len(labels))}


interface = gr.Interface(fn=predict, inputs=gr.components.Image(shape=(512, 512)), outputs=gr.components.Label(
    num_top_classes=2), title=title, description=description, article=article, examples=examples, interpretation=interpretation)
interface.launch(share=True, enable_queue=enable_queue)
