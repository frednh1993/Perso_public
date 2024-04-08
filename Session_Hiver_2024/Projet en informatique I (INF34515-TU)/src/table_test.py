from transformers import TableTransformerForObjectDetection
from PIL import Image
from transformers import DetrFeatureExtractor
import torch
import matplotlib.pyplot as plt

import numpy as np


feature_extractor = DetrFeatureExtractor()
model = TableTransformerForObjectDetection.from_pretrained("microsoft/table-transformer-structure-recognition")

# colors for visualization
COLORS = [[0.000, 0.447, 0.741], [0.850, 0.325, 0.098], [0.929, 0.694, 0.125],
          [0.494, 0.184, 0.556], [0.466, 0.674, 0.188], [0.301, 0.745, 0.933]]

def plot_results(pil_img, scores, labels, boxes):
    # To create a new figure object (width, height).
    plt.figure(figsize=(16,10))
    
    # To display an image represented as a PIL Image object.
    plt.imshow(pil_img)
    
    # Get the current Axes instance.
    ax = plt.gca()
    colors = COLORS * 100
    
    for score, label, (xmin, ymin, xmax, ymax),c  in zip(scores.tolist(), labels.tolist(), boxes.tolist(), colors):
      if label != 2:
        continue
      
      ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                  fill=False, color=c, linewidth=3))
      text = f'{model.config.id2label[label]}: {score:0.2f}'
      ax.text(xmin, ymin, text, fontsize=15,
              bbox=dict(facecolor='yellow', alpha=0.5))
    plt.axis('off')
    plt.show()
    
def plot_results_2(pil_img, boxes):
    # To create a new figure object (width, height).
    plt.figure(figsize=(16,10))
    
    # To display an image represented as a PIL Image object.
    plt.imshow(pil_img)
    
    # Get the current Axes instance.
    ax = plt.gca()
    colors = COLORS * 100
    
    for (xmin, ymin, xmax, ymax),c  in zip(boxes.tolist(), colors):
   
      ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                  fill=False, color=c, linewidth=3))
    plt.axis('off')
    plt.show()
    


image = Image.open("table2.png").convert("RGB")
# image.show()

encoding = feature_extractor(image, return_tensors="pt")
# print(encoding.data["pixel_values"])

with torch.no_grad():
  outputs = model(**encoding)
# print(outputs.logits)

target_sizes = [image.size[::-1]]
results = feature_extractor.post_process_object_detection(outputs, threshold=0.6, target_sizes=target_sizes)[0]
plot_results(image, results['scores'], results['labels'], results['boxes'])
print(model.config.label2id)


tensor_np = np.array([[15.6750, 507.0435, 498.6588, 526.7598]])
plot_results_2(image, tensor_np)
print("End")