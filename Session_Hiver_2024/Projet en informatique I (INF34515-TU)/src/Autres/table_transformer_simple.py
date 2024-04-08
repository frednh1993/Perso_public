from huggingface_hub import hf_hub_download
from PIL import Image
from transformers import DetrFeatureExtractor, DetrForObjectDetection
import torch
import matplotlib.pyplot as plt
import fitz as PyMuPDF

PRINT_CASE = True




model_table = DetrForObjectDetection.from_pretrained("nielsr/detr-table-detection")
# model_structure = DetrForObjectDetection.from_pretrained("nielsr/detr-table-structure-recognition")
print(model_table)
print(model_table.config)

# colors for visualization
colors = ["red", "blue", "green", "yellow", "orange", "violet"]

def plot_results(pil_img, prob, boxes):
    plt.figure(figsize=(32,20))
    plt.imshow(pil_img)
    ax = plt.gca()
    for p, (xmin, ymin, xmax, ymax) in zip(prob, boxes.tolist()):
        cl = p.argmax()
        ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, fill=False, color=colors[cl.item()], linewidth=3))
        text = f'{model_table.config.id2label[cl.item()]}: {p[cl]:0.2f}'
        ax.text(xmin, ymin, text, fontsize=15, bbox=dict(facecolor='yellow', alpha=0.5))
    plt.axis('off')
    plt.show()
    
def plot_results_structure(pil_img, prob, boxes, class_to_show=0):
    plt.figure(figsize=(32,20))
    plt.imshow(pil_img)
    ax = plt.gca()
    for p, (xmin, ymin, xmax, ymax) in zip(prob, boxes.tolist()):
        cl = p.argmax()
        if cl.item() == class_to_show:
          ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                    fill=False, color=colors[cl.item()], linewidth=3))
          text = f'{model_structure.config.id2label[cl.item()]}: {p[cl]:0.2f}'
          ax.text(xmin, ymin, text, fontsize=15,
                  bbox=dict(facecolor='red', alpha=0.5))
        else:
          continue
    plt.axis('off')
    plt.show()
    
    
# - 1 - Loading image.
file_path = hf_hub_download(repo_id="nielsr/example-pdf", repo_type="dataset", filename="example_pdf.png")
image = Image.open(file_path).convert("RGB")
width, height = image.size
image.resize((int(width*0.5), int(height*0.5)))
    
    
# - 2 - Resize the image and ormalize it.
feature_extractor = DetrFeatureExtractor()
encoding = feature_extractor(image, return_tensors="pt")
encoding.keys()
if PRINT_CASE:
    print(encoding['pixel_values'].shape)
    
        
# - 3 - Send the pixel values and pixel mask through the model.
with torch.no_grad():
    outputs = model_table(**encoding)
    
    
# - 4 - Visualize the results
# keep only predictions of queries with 0.9+ confidence (excluding no-object class)
probas = outputs.logits.softmax(-1)[0, :, :-1]
keep = probas.max(-1).values > 0.9

# rescale bounding boxes
target_sizes = torch.tensor(image.size[::-1]).unsqueeze(0)
postprocessed_outputs = feature_extractor.post_process(outputs, target_sizes)
postprocessed_outputs = feature_extractor.post_process_object_detection(outputs, 0, target_sizes)
bboxes_scaled = postprocessed_outputs[0]['boxes'][keep]

plot_results(image, probas[keep], bboxes_scaled)
print("End")


# # - 5 - Table structure recognition
# # file_path = hf_hub_download(repo_id="nielsr/example-pdf", repo_type="dataset", filename="example_table.png")
# # image = Image.open(file_path).convert("RGB")
# # image = Image.open("/content/Screen Shot 2022-09-06 at 8.09.35 AM (1).png").convert("RGB")
# file_path_2063UCAP = "C:\\Users\\rmfbo\\source\\repos\\UQAR\\Team\\Projet_Informatique_I_Hiver_2024\\inputs_outputs\\pdf_sources\\206.3-UCAP.pdf"
# pdf_document = PyMuPDF.open(file_path_2063UCAP)  
# page = pdf_document.load_page(8)
# pixmap = page.get_pixmap(colorspace=PyMuPDF.csRGB)
# image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
# width, height = image.size
# image.resize((int(width*0.5), int(height*0.5)))

# # - 2 - Resize the image and ormalize it.
# feature_extractor = DetrFeatureExtractor()
# encoding = feature_extractor(image, return_tensors="pt")
# encoding.keys()
# if PRINT_CASE:
#     print(encoding['pixel_values'].shape)
    
# # - 6 - Prepare the image for the model.
# encoding = feature_extractor(image, return_tensors="pt")
# encoding.keys()

# with torch.no_grad():
#     outputs = model_cells(**encoding)
        
# # keep only predictions of queries with 0.9+ confidence (excluding no-object class)
# probas = outputs.logits.softmax(-1)[0, :, :-1]
# keep = probas.max(-1).values > 0.6

# # rescale bounding boxes
# target_sizes = torch.tensor(image.size[::-1]).unsqueeze(0)
# postprocessed_outputs = feature_extractor.post_process(outputs, target_sizes)
# bboxes_scaled = postprocessed_outputs[0]['boxes'][keep]
    
# plot_results_of_cells(image, probas[keep], bboxes_scaled, class_to_show=1)
    
# model_cells.config.id2label