from huggingface_hub import hf_hub_download
from PIL import Image
from transformers import DetrFeatureExtractor
from transformers import DetrForObjectDetection
import torch
import matplotlib.pyplot as plt


file_path = hf_hub_download(repo_id="nielsr/example-pdf", repo_type="dataset", filename="example_pdf.png")
image = Image.open(file_path).convert("RGB")
width, height = image.size
image.resize((int(width*0.5), int(height*0.5)))


feature_extractor = DetrFeatureExtractor()
encoding = feature_extractor(image, return_tensors="pt")
encoding.keys()

print(encoding['pixel_values'].shape)



model = DetrForObjectDetection.from_pretrained("nielsr/detr-table-detection")



with torch.no_grad():
  outputs = model(**encoding)
  


# colors for visualization
colors = ["red", "blue", "green", "yellow", "orange", "violet"]

def plot_results(pil_img, prob, boxes):
    plt.figure(figsize=(32,20))
    plt.imshow(pil_img)
    ax = plt.gca()
    for p, (xmin, ymin, xmax, ymax) in zip(prob, boxes.tolist()):
        cl = p.argmax()
        ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                   fill=False, color=colors[cl.item()], linewidth=3))
        text = f'{model.config.id2label[cl.item()]}: {p[cl]:0.2f}'
        ax.text(xmin, ymin, text, fontsize=15,
                bbox=dict(facecolor='yellow', alpha=0.5))
    plt.axis('off')
    plt.show()
    


# keep only predictions of queries with 0.9+ confidence (excluding no-object class)
probas = outputs.logits.softmax(-1)[0, :, :-1]
keep = probas.max(-1).values > 0.9

# rescale bounding boxes
target_sizes = torch.tensor(image.size[::-1]).unsqueeze(0)
postprocessed_outputs = feature_extractor.post_process(outputs, target_sizes)
bboxes_scaled = postprocessed_outputs[0]['boxes'][keep]

plot_results(image, probas[keep], bboxes_scaled)
print("The End")