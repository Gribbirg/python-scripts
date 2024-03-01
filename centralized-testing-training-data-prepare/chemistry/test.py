import openpyxl
from openpyxl_image_loader import SheetImageLoader
import imagehash

wb = openpyxl.load_workbook('table.xlsx')
sheet = wb.active
image_loader = SheetImageLoader(sheet)

print(sheet[1][0].value)

if image_loader.image_in("B3"):
    image = image_loader.get('B3')
    print(imagehash.average_hash(image))
    image = image_loader.get('B55')
    print(imagehash.average_hash(image))
#     image.save(f"chemistry/images/{image.}.png")
#
# image = image_loader.get('B16')
# image.save(f"chemistry/images/{image.__hash__()}.png")

