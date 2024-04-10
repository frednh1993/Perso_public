from transformers import TableTransformerForObjectDetection
from PIL import Image, ImageDraw
from transformers import DetrFeatureExtractor
import torch
import matplotlib.pyplot as plt

import numpy as np
from tqdm.auto import tqdm
import easyocr
from io import BytesIO




feature_extractor = DetrFeatureExtractor()
model = TableTransformerForObjectDetection.from_pretrained("microsoft/table-transformer-structure-recognition")

# colors for visualization
COLORS = [[0.000, 0.447, 0.741], [0.850, 0.325, 0.098], [0.929, 0.694, 0.125],
          [0.494, 0.184, 0.556], [0.466, 0.674, 0.188], [0.301, 0.745, 0.933]]

 # - 11 - Apply OCR row by row
def apply_ocr(cell_coordinates):
    # let's OCR row by row
    data = dict()
    max_num_columns = 0    # FB_CHANGED !
    for idx, row in enumerate(tqdm(cell_coordinates)):
        row_text = []
        for cell in row["cells"]:
            # crop cell out of image
            cell_image = np.array(cropped_table.crop(cell["cell"]))
            # apply OCR
            result = reader.readtext(np.array(cell_image))
            if len(result) > 0:
                # print([x[1] for x in list(result)])
                text = " ".join([x[1] for x in result])
                row_text.append(text)

        if len(row_text) > max_num_columns:
            max_num_columns = len(row_text)

        data[idx] = row_text

        print("Max number of columns:", max_num_columns)

    # pad rows which don't have max_num_columns elements
    # to make sure all rows have the same number of columns
    for row, row_data in data.copy().items():
        if len(row_data) != max_num_columns:
            row_data = row_data + ["" for _ in range(max_num_columns - len(row_data))]
        data[row] = row_data

    return data

def isolate_table_cells(columns : list, rows : list):
    pass

def isolate_table_rows_and_columns(cells : list, labels : list):
    
    columns_tensors = []
    rows_tensors = []
    
    for index, label in enumerate(labels) : 
        
        match label:
            case 1:
                columns_tensors.append(cells[index])
            case 2:
                rows_tensors.append(cells[index])
            case 3:
                columns_tensors.append(cells[index])
            case _:
                pass
            
    return columns_tensors, rows_tensors

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
# outputs.logits.shape 

target_sizes = [image.size[::-1]]
results = feature_extractor.post_process_object_detection(outputs, threshold=0.6, target_sizes=target_sizes)[0]

cells_array = results['boxes'].tolist()
labels_array = results['labels'].tolist()
sorted_columns_array, sorted_rows_array  = isolate_table_rows_and_columns(cells_array, labels_array)
sorted_cells_2d_list : list[][] = isolate_table_cells(sorted_columns_array, sorted_rows_array)

# numpy_array = rows.numpy()
reader = easyocr.Reader(['en'])
# print(model.config.label2id)
# for tensor in numpy_array :
#   x1 = tensor[0]
#   y1 = tensor[1]
#   x2 = tensor[2]
#   y2 = tensor[3]

# numpy_array_r = row0.numpy()
# numpy_array_c = col0.numpy()
# test = numpy_array_r.tolist()
# sorted_cells_array = isolate_table_cells(cells_array, results_array)

# cropped_img_r = image.crop(test)
# cropped_img_r.show()
# png_buffer = BytesIO()
# cropped_img_r.save(png_buffer, format="PNG")

# result1 = reader.readtext(numpy_array_r)

# cropped_img_c = image.crop(numpy_array_r.tolist()[0], numpy_array_c[1], numpy_array_c[2], numpy_array_c[3])
# Image_test = Image.open(png_buffer)
# cropped_img_r.save("table_row.png")
# filepath = "C:\\Users\\rmfbo\\source\\repos\\UQAR\\Perso\\Session_Hiver_2024\\Projet en informatique I (INF34515-TU)\\table_row.png"
# totfilepath = "C:\\Users\\rmfbo\\source\\repos\\UQAR\\Perso\\Session_Hiver_2024\\Projet en informatique I (INF34515-TU)\\table2.png"
png_data = png_buffer.getvalue()
result1 = reader.readtext(png_data)
# result2 = reader.readtext(totfilepath)
# cropped_img_r.show()
isolate_table_cells(cells_array)
plot_results(image, results['scores'], results['labels'], results['boxes'])
# print(model.config.label2id)

# - 11 - Apply OCR row by row
# cell_coordinates = get_cell_coordinates_by_row(cells)
# len(cell_coordinates)
# len(cell_coordinates[0]["cells"])
# for row in cell_coordinates:
#     print(row["cells"])
# reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory
# data = apply_ocr(cell_coordinates)
# for row, row_data in data.items():
#     print(row_data)

# tensor_np = np.array([[15.6750, 507.0435, 498.6588, 526.7598]])
# plot_results_2(image, tensor_np)
# print("End")