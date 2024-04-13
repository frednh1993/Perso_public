from transformers import TableTransformerForObjectDetection
from PIL import Image, ImageDraw
from transformers import DetrFeatureExtractor
import torch
import matplotlib.pyplot as plt

import numpy as np
from tqdm.auto import tqdm
import easyocr
from io import BytesIO
import math




# feature_extractor_table = DetrFeatureExtractor()
# model_table = TableTransformerForObjectDetection.from_pretrained("microsoft/table-transformer-detection")
# print(model_table.config.id2label)

feature_extractor_structure = DetrFeatureExtractor()
model_structure = TableTransformerForObjectDetection.from_pretrained("microsoft/table-transformer-structure-recognition")
print(model_structure.config.id2label)

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

def check_equivalance_of_data(data1, data2, adjustment_factor=0):
    data1_floor = math.floor(data1)
    data1_ceil = math.ceil(data1)
    data2_floor = math.floor(data2)
    data2_ceil = math.ceil(data2)
    
    if(data1_floor == data2_floor or data1_floor == data2_ceil):
        return True
    if(data1_ceil == data2_floor or data1_ceil == data2_ceil):
        return True
    
    if(data1_floor - adjustment_factor == data2_floor or data1_floor - adjustment_factor == data2_ceil):
        return True
    if(data1_floor + adjustment_factor == data2_floor or data1_floor + adjustment_factor == data2_ceil):
        return True
    
    if(data1_ceil - adjustment_factor == data2_floor or data1_ceil - adjustment_factor == data2_ceil):
        return True
    if(data1_ceil + adjustment_factor == data2_floor or data1_ceil + adjustment_factor == data2_ceil):
        return True
    
    return False

def extract_values_from_cells_table(image : Image, sorted_cells_matrix) :
    reader = easyocr.Reader(['en'])
    dimensions = sorted_cells_matrix.shape
    num_rows, num_cols = dimensions
    values_matrix = np.zeros((num_rows, num_cols), dtype=object)
    PERCENTAGE_ADJUSTMENT_MARGIN = 5/100
    
    for row_idx in range(sorted_cells_matrix.shape[0]):
        for col_idx in range(sorted_cells_matrix.shape[1]):
            element = sorted_cells_matrix[row_idx, col_idx]
            if (element != 0):
                png_buffer = BytesIO()
                adjusted_element = (element[0], element[1], element[2], element[3])
                cell_image = image.crop(adjusted_element)
                resized_cell_image = cell_image.resize((cell_image.width * 2, cell_image.height * 2))
                resized_cell_image.show()
                resized_cell_image.save(png_buffer, format="PNG")
                png_buffer_bytes = png_buffer.getvalue()
                cell_value = reader.readtext(png_buffer_bytes)
                # TODO : Allow to continue even for the case where there is no value found.
                if cell_value != []:
                    data = cell_value[0][1]
                else:
                    data = ""
                values_matrix[row_idx, col_idx] = data
                
    return values_matrix

def isolate_table_cells(columns : list, rows : list):
    # Hypothesis that inputs are sorted from left to right and top to bottom.
    cols_nbr = len(columns)
    row_nbr = len(rows)
    cells_matrix = np.zeros((row_nbr, cols_nbr), dtype=object)
    
    for col_idx, column in enumerate(columns) :
        for row_idx, row in enumerate(rows) :
            if ( (column[0] >= row[0] or check_equivalance_of_data(column[0], row[0])) and (column[2] <= row[2] or check_equivalance_of_data(column[2], row[2])) ) :
                cell_coordinates = (column[0], row[1], column[2], row[3])
                cells_matrix[row_idx, col_idx] = cell_coordinates
                
    return cells_matrix

def determine_table_perimeter(results_table):
    
    test = results_table['boxes']
    # test_1 = (0.13 * test[0][0])
    # test_2 = (0.10 * test[0][1])
    # test_3 = (0.03 * test[0][2])
    # test_4 = (0.02 * test[0][3])
    
    test[0][0] = test[0][0] - (0.13 * test[0][0])
    test[0][1] = test[0][1] - (0.10 * test[0][1])
    test[0][2] = test[0][2] + (0.03 * test[0][2])
    test[0][3] = test[0][3] + (0.02 * test[0][3])
    
    # tensor_2 = torch.tensor([[test_1, test_2, test_3, test_4]])
    # results_table['boxes'] = results_table['boxes'] - tensor_2
                
    return True
                
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
                # columns_tensors.append(cells[index])
                pass
            case _:
                pass
            
    return columns_tensors, rows_tensors

def plot_results(model, config_number_to_show, pil_img, scores, labels, boxes):
    # To create a new figure object (width, height).
    plt.figure(figsize=(16,10))
    
    # To display an image represented as a PIL Image object.
    plt.imshow(pil_img)
    
    # Get the current Axes instance.
    ax = plt.gca()
    colors = COLORS * 100
    
    for score, label, (xmin, ymin, xmax, ymax),c  in zip(scores.tolist(), labels.tolist(), boxes.tolist(), colors):
      if label != config_number_to_show:
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
    



# image_raw = Image.open("raw_1.png").convert("RGB")
# # image.show()

# encoding_table = feature_extractor_table(image_raw, return_tensors="pt")
# # print(feature_extractor_table.data["pixel_values"])

# with torch.no_grad():
#   outputs_table = model_table(**encoding_table)
# # print(outputs_table.logits)
# # outputs_table.logits.shape 

# width_raw, height_raw = image_raw.size
# results_table = feature_extractor_table.post_process_object_detection(outputs_table, threshold=0.7, target_sizes=[(height_raw, width_raw)])[0]
# # plot_results(model_table, 0, image_raw, results_table['scores'], results_table['labels'], results_table['boxes'])
# determine_table_perimeter(results_table)
# # plot_results(model_table, 0, image_raw, results_table['scores'], results_table['labels'], results_table['boxes'])
# test = results_table['boxes'].tolist()
# adjusted_element = (test[0][0], test[0][1], test[0][2], test[0][3])
# # adjusted_element2 = adjusted_element.tolist()
# table_image = image_raw.crop(adjusted_element)
# # table_image_png_buffer = BytesIO()
# # table_image.save(table_image_png_buffer, format="PNG")
# # table_image_png_buffer_bytes = table_image_png_buffer.getvalue()

# table_image.save("table_1.png")
# print("The End for table perimeter detection !")


# // ---- Structure section ---- //

structure_image = Image.open("table3.png").convert("RGB")
structure_image = structure_image.resize((structure_image.width * 3, structure_image.height * 3))
structure_image.show()

encoding_structure = feature_extractor_structure(structure_image, return_tensors="pt")
# print(feature_extractor_structure.data["pixel_values"])

with torch.no_grad():
  outputs_structure = model_structure(**encoding_structure)

target_sizes = [structure_image.size[::-1]]
# TODO : The image NEED to have more PADDING on his left side ! 
results_structure = feature_extractor_structure.post_process_object_detection(outputs_structure, threshold=0.3, target_sizes=target_sizes)[0]

plot_results(model_structure, 2, structure_image, results_structure['scores'], results_structure['labels'], results_structure['boxes'])

cells_array = results_structure['boxes'].tolist()
labels_array = results_structure['labels'].tolist()
unsorted_columns_array, unsorted_rows_array  = isolate_table_rows_and_columns(cells_array, labels_array)

# Sort columns in function of x0 or xmin coordinate.
sorted_columns_array = sorted(unsorted_columns_array, key=lambda c: c[0])
# Sort rows in function of y0 or ymin coordinate.
sorted_rows_array = sorted(unsorted_rows_array, key=lambda c: c[1])

sorted_cells_matrix = isolate_table_cells(sorted_columns_array, sorted_rows_array)
sorted_values_matrix = extract_values_from_cells_table(structure_image, sorted_cells_matrix)

for row_idx in range(sorted_values_matrix.shape[0]):
    print()
    for col_idx in range(sorted_values_matrix.shape[1]):
        print(f" {sorted_values_matrix[row_idx, col_idx]} ", end="")

print("The End for table structure data detection !")