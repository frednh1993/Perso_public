import os
import fitz as PyMuPDF
from io import BytesIO
from transformers import AutoModelForObjectDetection, DetrFeatureExtractor, TableTransformerForObjectDetection
from huggingface_hub import hf_hub_download
from PIL import Image
import torch
import matplotlib.pyplot as plt
from transformers import TableTransformerForObjectDetection
PDF_TO_TEST_I = '206.3-UCAP'

# Path of the PDF file to extract.
relative_path = os.path.join('.','inputs_outputs','pdf_sources',PDF_TO_TEST_I+'.pdf')
absolute_path = os.path.abspath(relative_path)

# Path of the PDF file to extract.
relative_path_png = os.path.join('.','inputs_outputs','pdf_sources',PDF_TO_TEST_I+'_png')
absolute_path_png = os.path.abspath(relative_path_png)

# colors for visualization
COLORS = [[0.000, 0.447, 0.741], [0.850, 0.325, 0.098], [0.929, 0.694, 0.125],
          [0.494, 0.184, 0.556], [0.466, 0.674, 0.188], [0.301, 0.745, 0.933]]


def browse_png (folder):
  if not os.path.exists(folder):
    print("Le dossier spécifié n'existe pas.")
    return
  
  png = os.listdir(folder)
  return png


def create_folder(folder_path):
  try:
    os.mkdir(folder_path)
    print(f"Folder '{folder_path}' created successfully.")
    return folder_path
  except FileExistsError:
    print(f"Folder '{folder_path}' already exists.")
    return folder_path


def convert_pdf_to_png_format(pdf_path):

  pdf_document = PyMuPDF.open(pdf_path)

  folder_path_png = create_folder(absolute_path_png)
  
  for page_number in range(pdf_document.page_count):
    page = pdf_document.load_page(page_number)
    
    # Convert the page to a pixmap
    pixmap = page.get_pixmap()

    # Save the pixmap as a PNG file
    output_file_path = f"{absolute_path_png}\\page_{page_number + 1}.png"
    # output_file_path = os.path.join(absolute_path_png, 'page_'+{page_number + 1}+'.png')
    
    image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
    bytes_io = BytesIO()
    image.save(output_file_path, "PNG")

    # print(f"Page {page_number + 1} converted to {output_file_path}")
    
  return folder_path_png


def plot_results(pil_img, scores, labels, boxes):
    # To create a new figure object (width, height).
    plt.figure(figsize=(16,10))
    
    # To display an image represented as a PIL Image object.
    plt.imshow(pil_img)
    
    # Get the current Axes instance.
    ax = plt.gca()
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()
    origin_coordinates = (x_min, y_min)
    
    colors = COLORS * 100
    
    for score, label, (xmin, ymin, xmax, ymax),c  in zip(scores.tolist(), labels.tolist(), boxes.tolist(), colors):
        ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                   fill=False, color=c, linewidth=3))
        text = f'{model.config.id2label[label]}: {score:0.2f}'
        ax.text(xmin, ymin, text, fontsize=15,
                bbox=dict(facecolor='yellow', alpha=0.5))
    plt.axis('off')
    plt.show()
   
    


# Table detection

model = TableTransformerForObjectDetection.from_pretrained("microsoft/table-transformer-detection")
feature_extractor = DetrFeatureExtractor()

# - 1 -
# pdf format to png
png_folder = convert_pdf_to_png_format(absolute_path)
png_images = browse_png(png_folder)

for png_image in png_images :

  png_image_path = os.path.join(png_folder,png_image)
  image = Image.open(png_image_path).convert("RGB")
  width, height = image.size
  image.resize((int(width*0.5), int(height*0.5)))

  # - 2 -
  # feature_extractor = DetrFeatureExtractor()
  encoding = feature_extractor(image, return_tensors="pt")
  encoding.keys()
  print(encoding['pixel_values'].shape)
  # dict_keys(['pixel_values', 'pixel_mask'])

  # - 3 -
  # model = TableTransformerForObjectDetection.from_pretrained("microsoft/table-transformer-detection")

  with torch.no_grad():
    outputs = model(**encoding)
    
  # - 4 -
  # rescale bounding boxes
  width, height = image.size
  # List[Dict]`: A list of dictionaries, each dictionary containing the scores, labels and boxes for an image in the batch as predicted by the model.
  results = feature_extractor.post_process_object_detection(outputs, threshold=0.7, target_sizes=[(height, width)])[0]

  plot_results(image, results['scores'], results['labels'], results['boxes'])
  print("end")



# # Table structure recognition
# # - 1 -
# ile_path = hf_hub_download(repo_id="nielsr/example-pdf", repo_type="dataset", filename="example_table.png")
# image = Image.open(file_path).convert("RGB")
# width, height = image.size
# image.resize((int(width*0.5), int(height*0.5)))

# # - 2 -
# encoding = feature_extractor(image, return_tensors="pt")
# encoding.keys()
# # dict_keys(['pixel_values', 'pixel_mask'])

# # - 3 -
# model = TableTransformerForObjectDetection.from_pretrained("microsoft/table-transformer-structure-recognition")

# # - 4 -
# with torch.no_grad():
#   outputs = model(**encoding)

# # - 5 -
# target_sizes = [image.size[::-1]]
# results = feature_extractor.post_process_object_detection(outputs, threshold=0.6, target_sizes=target_sizes)[0]
# plot_results(image, results['scores'], results['labels'], results['boxes'])

# # - 6 -
# model.config.id2label