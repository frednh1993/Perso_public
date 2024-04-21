import fitz as PyMuPDF 
from PIL import Image
import matplotlib.pyplot as plt
from io import BytesIO
from pdf2image import convert_from_bytes


# colors for visualization
COLORS = [[0.000, 0.447, 0.741], [0.850, 0.325, 0.098], [0.929, 0.694, 0.125],
          [0.494, 0.184, 0.556], [0.466, 0.674, 0.188], [0.301, 0.745, 0.933]]

def plot_results(pil_img, labels, boxes):
    # To create a new figure object (width, height).
    plt.figure(figsize=(16,10))
    
    # To display an image represented as a PIL Image object.
    plt.imshow(pil_img)
    
    # Get the current Axes instance.
    ax = plt.gca()
    colors = COLORS * 100
    legend = ["Titre", "Tableau", "Métadonnées"]
    hor_adjustment_factor = pil_img.width/612.0
    ver_adjustment_factor = pil_img.height/792.0
    
    for label, (xmin, ymin, xmax, ymax),c  in zip(labels, boxes, colors):
      
      xmin = xmin * hor_adjustment_factor
      ymin = ymin * ver_adjustment_factor
      xmax = xmax * hor_adjustment_factor
      ymax = ymax * ver_adjustment_factor
      
      # if label != config_number_to_show:
      #   continue
      
      ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                  fill=False, color=c, linewidth=3))
      text = f'{legend[label]}'
      ax.text(xmin, ymin, text, fontsize=15,
              bbox=dict(facecolor='yellow', alpha=0.5))
    plt.axis('off')
    plt.show()
    print()


LABELS = [ 0, 1, 2, 0, 1 ]
# Data on a 612 points reference in X axis and a 792 reference in Y axis.
BOXES = [ [135.7875, 306.3825, 475.4475, 323.2125], [83.0025, 326.2725, 546.5925, 424.1925], [77.64750000000001, 426.4875, 535.1175000000001, 469.3275], [100.5975, 577.1925, 528.9975000000001, 620.7975], [88.3575, 623.8575, 558.8325, 731.7225] ]

# Page 2
page_index = 40
pdf_path = "C:\\Users\\rmfbo\\source\\repos\\UQAR\\Perso\\Session_Hiver_2024\\Projet en informatique I (INF34515-TU)\\2021-HONI-List_of_Transmission_Lines_by_Functional_Category.pdf"

# pdf_document = PyMuPDF.open(pdf_path)
# number_of_pages = pdf_document.page_count
# page_pdf = pdf_document.load_page(page_index)
# width, height = page_pdf.rect.width, page_pdf.rect.height
# image_pixmap = page_pdf.get_pixmap()
# image_bytes = image_pixmap.pil_tobytes()

with open(pdf_path, 'rb') as file:
    pdf_bytes = file.read()
    
images = convert_from_bytes(pdf_bytes)
    
# pdf_doc = BytesIO(pdf_bytes)
# pdf_doc_image = Image.open(pdf_doc)

# pil_image = Image.open(pdf_doc_image)
# pil_image = pil_image.convert("RGB")
# pil_image = Image.open(image_bytes).convert("RGB")

plot_results(images[page_index], LABELS, BOXES)

# test = table_image_png_buffer.getvalue()
# pil_image.save("test.png", "PNG")