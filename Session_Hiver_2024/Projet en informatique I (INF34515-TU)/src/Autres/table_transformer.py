from transformers import AutoModelForObjectDetection
import torch
from PIL import Image, ImageDraw
from huggingface_hub import hf_hub_download
from torchvision import transforms
import torch
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Patch
from transformers import TableTransformerForObjectDetection
import numpy as np
import csv
import easyocr
from tqdm.auto import tqdm
import csv
import pandas as pd

import fitz as PyMuPDF 

CASE_SAVE_CSV = False
CASE_SAVE_JPG = False
OPTIONAL = True
CASE_PRINT_TABLE_CELLS = True
TEST_CASE = True



def find_table_of_microsoft_table_transformer(page):
    # - 1 - Load model for table detection.
    model = AutoModelForObjectDetection.from_pretrained("microsoft/table-transformer-detection", revision="no_timm")
    model.config.id2label

    # - 8 - Load structure recognition model.
    structure_model = TableTransformerForObjectDetection.from_pretrained("microsoft/table-structure-recognition-v1.1-all")


    # - 3 - Prepare image for the model
    class MaxResize(object):
        def __init__(self, max_size=800):
            self.max_size = max_size

        def __call__(self, image):
            width, height = image.size
            current_max_size = max(width, height)
            scale = self.max_size / current_max_size
            resized_image = image.resize((int(round(scale*width)), int(round(scale*height))))

            return resized_image


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

        if OPTIONAL:
            print("Max number of columns:", max_num_columns)

        # pad rows which don't have max_num_columns elements
        # to make sure all rows have the same number of columns
        for row, row_data in data.copy().items():
            if len(row_data) != max_num_columns:
                row_data = row_data + ["" for _ in range(max_num_columns - len(row_data))]
            data[row] = row_data

        return data


    # - 5 - Postprocessing
    # for output bounding box post-processing
    def box_cxcywh_to_xyxy(x):
        x_c, y_c, w, h = x.unbind(-1)
        b = [(x_c - 0.5 * w), (y_c - 0.5 * h), (x_c + 0.5 * w), (y_c + 0.5 * h)]
        return torch.stack(b, dim=1)


    # -6- Visualize
    def fig2img(fig):
        """Convert a Matplotlib figure to a PIL Image and return it"""
        import io
        buf = io.BytesIO()
        fig.savefig(buf)
        buf.seek(0)
        img = Image.open(buf)
        return img


    # - 11 - Apply OCR row by row
    def get_cell_coordinates_by_row(table_data):
        # Extract rows and columns
        rows = [entry for entry in table_data if entry['label'] == 'table row']
        columns = [entry for entry in table_data if entry['label'] == 'table column']

        # Sort rows and columns by their Y and X coordinates, respectively
        rows.sort(key=lambda x: x['bbox'][1])
        columns.sort(key=lambda x: x['bbox'][0])

        # Function to find cell coordinates
        def find_cell_coordinates(row, column):
            cell_bbox = [column['bbox'][0], row['bbox'][1], column['bbox'][2], row['bbox'][3]]
            return cell_bbox

        # Generate cell coordinates and count cells in each row
        cell_coordinates = []

        for row in rows:
            row_cells = []
            for column in columns:
                cell_bbox = find_cell_coordinates(row, column)
                row_cells.append({'column': column['bbox'], 'cell': cell_bbox})

            # Sort cells in the row by X coordinate
            row_cells.sort(key=lambda x: x['column'][0])

            # Append row information to cell_coordinates
            cell_coordinates.append({'row': row['bbox'], 'cells': row_cells, 'cell_count': len(row_cells)})

        # Sort rows from top to bottom
        cell_coordinates.sort(key=lambda x: x['row'][1])

        return cell_coordinates


    # -7- Crop table
    # We crop the table out of the image, which include some padding to make sure the borders of the table are included.#
    def objects_to_crops(img, tokens, objects, class_thresholds, padding=10):
        """
        Process the bounding boxes produced by the table detection model into
        cropped table images and cropped tokens.
        """

        table_crops = []
        for obj in objects:
            if obj['score'] < class_thresholds[obj['label']]:
                continue

            cropped_table = {}

            bbox = obj['bbox']
            bbox = [bbox[0]-padding, bbox[1]-padding, bbox[2]+padding, bbox[3]+padding]

            cropped_img = img.crop(bbox)

            table_tokens = [token for token in tokens if iob(token['bbox'], bbox) >= 0.5]
            for token in table_tokens:
                token['bbox'] = [token['bbox'][0]-bbox[0],
                                token['bbox'][1]-bbox[1],
                                token['bbox'][2]-bbox[0],
                                token['bbox'][3]-bbox[1]]

            # If table is predicted to be rotated, rotate cropped image and tokens/words:
            if obj['label'] == 'table rotated':
                cropped_img = cropped_img.rotate(270, expand=True)
                for token in table_tokens:
                    bbox = token['bbox']
                    bbox = [cropped_img.size[0]-bbox[3]-1,
                            bbox[0],
                            cropped_img.size[0]-bbox[1]-1,
                            bbox[2]]
                    token['bbox'] = bbox

            cropped_table['image'] = cropped_img
            cropped_table['tokens'] = table_tokens

            table_crops.append(cropped_table)

        return table_crops


    # - 5 - Postprocessing
    #  This function takes the model outputs, image size, and id2label dictionary as input. 
    # It extracts the predicted labels, scores, and bounding boxes from the model outputs and 
    # creates a list of dictionaries, each representing an object detected in the image. 
    def outputs_to_objects(outputs, img_size, id2label):
        m = outputs.logits.softmax(-1).max(-1)
        pred_labels = list(m.indices.detach().cpu().numpy())[0]
        pred_scores = list(m.values.detach().cpu().numpy())[0]
        pred_bboxes = outputs['pred_boxes'].detach().cpu()[0]
        pred_bboxes = [elem.tolist() for elem in rescale_bboxes(pred_bboxes, img_size)]

        objects = []
        for label, score, bbox in zip(pred_labels, pred_scores, pred_bboxes):
            class_label = id2label[int(label)]
            if not class_label == 'no object':
                objects.append({'label': class_label, 'score': float(score),
                                'bbox': [float(elem) for elem in bbox]})

        return objects


    # - 10 - Visualize cells
    def plot_results(cells, class_to_visualize):
        if class_to_visualize not in structure_model.config.id2label.values():
            raise ValueError("Class should be one of the available classes")

        plt.figure(figsize=(16,10))
        plt.imshow(cropped_table)
        ax = plt.gca()

        for cell in cells:
            score = cell["score"]
            bbox = cell["bbox"]
            label = cell["label"]

            if label == class_to_visualize:
                xmin, ymin, xmax, ymax = tuple(bbox)

                ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, fill=False, color="red", linewidth=3))
                text = f'{cell["label"]}: {score:0.2f}'
                ax.text(xmin, ymin, text, fontsize=15,
                        bbox=dict(facecolor='yellow', alpha=0.5))
                plt.axis('off')


    # - 5 - Postprocessing
    def rescale_bboxes(out_bbox, size):
        img_w, img_h = size
        b = box_cxcywh_to_xyxy(out_bbox)
        b = b * torch.tensor([img_w, img_h, img_w, img_h], dtype=torch.float32)
        return b


    # -6- Visualize
    def visualize_detected_tables(img, det_tables, out_path=None):
        plt.imshow(img, interpolation="lanczos")
        fig = plt.gcf()
        fig.set_size_inches(20, 20)
        ax = plt.gca()

        for det_table in det_tables:
            bbox = det_table['bbox']

            if det_table['label'] == 'table':
                facecolor = (1, 0, 0.45)
                edgecolor = (1, 0, 0.45)
                alpha = 0.3
                linewidth = 2
                hatch='//////'
            elif det_table['label'] == 'table rotated':
                facecolor = (0.95, 0.6, 0.1)
                edgecolor = (0.95, 0.6, 0.1)
                alpha = 0.3
                linewidth = 2
                hatch='//////'
            else:
                continue

            rect = patches.Rectangle(bbox[:2], bbox[2]-bbox[0], bbox[3]-bbox[1], linewidth=linewidth,
                                        edgecolor='none',facecolor=facecolor, alpha=0.1)
            ax.add_patch(rect)
            rect = patches.Rectangle(bbox[:2], bbox[2]-bbox[0], bbox[3]-bbox[1], linewidth=linewidth,
                                        edgecolor=edgecolor,facecolor='none',linestyle='-', alpha=alpha)
            ax.add_patch(rect)
            rect = patches.Rectangle(bbox[:2], bbox[2]-bbox[0], bbox[3]-bbox[1], linewidth=0,
                                        edgecolor=edgecolor,facecolor='none',linestyle='-', hatch=hatch, alpha=0.2)
            ax.add_patch(rect)

        plt.xticks([], [])
        plt.yticks([], [])

        legend_elements = [Patch(facecolor=(1, 0, 0.45), edgecolor=(1, 0, 0.45),
                                    label='Table', hatch='//////', alpha=0.3),
                            Patch(facecolor=(0.95, 0.6, 0.1), edgecolor=(0.95, 0.6, 0.1),
                                    label='Table (rotated)', hatch='//////', alpha=0.3)]
        plt.legend(handles=legend_elements, bbox_to_anchor=(0.5, -0.02), loc='upper center', borderaxespad=0,
                        fontsize=10, ncol=2)
        plt.gcf().set_size_inches(10, 10)
        plt.axis('off')

        if out_path is not None:
            plt.savefig(out_path, bbox_inches='tight', dpi=150)

        return fig




    # - 1 - The torch package contains data structures, mathematical operations for multi-dimensional tensors.
    # CUDA is for doing operation using GPU.
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    print("microsoft/table-transformer-detection")


    if TEST_CASE:
        # - 2 - Load the PDF image.
        file_path = hf_hub_download(repo_id="nielsr/example-pdf", repo_type="dataset", filename="image.png")
        image = Image.open(file_path).convert("RGB")
        # let's display it a bit smaller
        # display(image.resize((int(0.6*width), (int(0.6*height)))))
    else :
        # - 2 - Load the PDF image.
        pixmap = page.get_pixmap(colorspace=PyMuPDF.csRGB)
        image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
        
    width, height = image.size
    image.resize((int(0.6*width), (int(0.6*height))))


    # - 3 - Prepare image for the model.
    detection_transform = transforms.Compose([
        MaxResize(800),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    pixel_values = detection_transform(image).unsqueeze(0)
    pixel_values = pixel_values.to(device)
    if OPTIONAL:
        print(pixel_values.shape)
    torch.Size([1, 3, 674, 800])    # Print the shape of the transformed image tensor.


    # - 4 - Forward pass to the model.
    with torch.no_grad():
        outputs = model(pixel_values)    # This performs a forward pass through the model using the transformed image tensor.
    outputs.logits.shape    # Check the shape of the logits (raw predictions)


    # - 5 - Postprocessing
    # We take the prediction that has an actual class (i.e. not "no object").
    # update id2label to include "no object"
    id2label = model.config.id2label
    id2label[len(model.config.id2label)] = "no object"

    objects = outputs_to_objects(outputs, image.size, id2label)
    if OPTIONAL:
        print(objects)


    # -6- Visualize (OPTIONAL)
    if OPTIONAL:
        fig = visualize_detected_tables(image, objects)
        visualized_image = fig2img(fig)


    # -7- Crop table
    tokens = []
    detection_class_thresholds = {
        "table": 0.5,
        "table rotated": 0.5,
        "no object": 10
    }
    crop_padding = 10
    tables_crops = objects_to_crops(image, tokens, objects, detection_class_thresholds, padding=0)
    cropped_table = tables_crops[0]['image'].convert("RGB")

    # -7- TODO : Try to eliminate the need to save physicly the image.
    if CASE_SAVE_JPG:
        cropped_table.save("table.jpg")


# // ----- //


    # - 8 - Load structure recognition model.
    structure_model.to(device)
    print("table-structure-recognition-v1.1-all")


    # - 9 - We prepare the cropped table image for the model, and perform a forward pass.
    structure_transform = transforms.Compose([
        MaxResize(1000),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    pixel_values = structure_transform(cropped_table).unsqueeze(0)
    pixel_values = pixel_values.to(device)
    if OPTIONAL:
        print(pixel_values.shape)
        torch.Size([1, 3, 258, 1000])

    # forward pass
    with torch.no_grad():
        outputs = structure_model(pixel_values)

    # update id2label to include "no object"
    structure_id2label = structure_model.config.id2label
    structure_id2label[len(structure_id2label)] = "no object"

    cells = outputs_to_objects(outputs, cropped_table.size, structure_id2label)
    if OPTIONAL: 
        print(cells)


    # - 10 - Visualize cells
    cropped_table_visualized = cropped_table.copy()
    draw = ImageDraw.Draw(cropped_table_visualized)

    for cell in cells:
        draw.rectangle(cell["bbox"], outline="red")

    cropped_table_visualized

    if OPTIONAL:   
        plot_results(cells, class_to_visualize="table row")


    # - 11 - Apply OCR row by row
    cell_coordinates = get_cell_coordinates_by_row(cells)
    len(cell_coordinates)
    len(cell_coordinates[0]["cells"])

    if OPTIONAL:
        for row in cell_coordinates:
            print(row["cells"])

    reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory
    data = apply_ocr(cell_coordinates)

    if CASE_PRINT_TABLE_CELLS:
        for row, row_data in data.items():
            print(row_data)

    
    # - 12 - Save as CSV (OPTIONAL)
    if CASE_SAVE_CSV :
        with open('output.csv','w') as result_file:
            wr = csv.writer(result_file, dialect='excel')

            for row, row_text in data.items():
                wr.writerow(row_text)
            
        df = pd.read_csv("output.csv")
        df.head()


find_table_of_microsoft_table_transformer(1)


