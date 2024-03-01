import openpyxl
from openpyxl_image_loader import SheetImageLoader
import imagehash
import json

wb = openpyxl.load_workbook('table2.xlsx')

data = []

answers = False
count = 0

for sheet in wb.worksheets:
    image_loader = SheetImageLoader(sheet)
    for i in range(1, sheet.max_row + 1):
        row = sheet[i]
        if row[0].value is not None:
            if row[0].value.__str__().split(" ")[0].replace(":", "") == "Модуль":
                data.append({"name": row[0].value, "questions_count": 0, "questions": []})
            elif answers:
                if image_loader.image_in(f"B{i}"):
                    if row[1].value is not None:
                        print(row)
                    try:
                        image = image_loader.get(f'B{i}')
                        image.save(f"images/{count}.png")
                        data[-1]["questions"][-1]["answers"].append(f"{count}.png")
                        image.close()
                        count += 1
                    except ValueError:
                        print(row, row[1].value)
                        data[-1]["questions"][-1]["answers"].append(row[1].value)
                else:
                    data[-1]["questions"][-1]["answers"].append(row[1].value)
                answers = not row[0].value == 4
            else:
                data[-1]["questions"].append({"num": row[0].value, "name": row[1].value, "answers": []})
                data[-1]["questions_count"] += 1
                answers = True
                if image_loader.image_in(f"B{i}"):
                    try:
                        image = image_loader.get(f'B{i}')
                        image.save(f"images/{count}.png")
                        data[-1]["questions"][-1]["image"] = f"{count}.png"
                        image.close()
                        count += 1
                    except ValueError:
                        print(row, row[1].value)

        elif row[1].value is not None:
            data[-1]["questions"][-1]["name"] += " " + row[1].value.__str__()
        elif image_loader.image_in(f"B{i}"):
            try:
                image = image_loader.get(f'B{i}')
                image.save(f"images/{count}.png")
                data[-1]["questions"][-1]["image"] = f"{count}.png"
                image.close()
                count += 1
            except ValueError:
                print(row, row[1].value)
        elif len(data) != 0 and len(data[-1]["questions"]) != 0 and len(data[-1]["questions"][-1]["answers"]) == 0:
            continue
        else:
            answers = False

print([len(line["questions"]) for line in data])
#
# for j in range(len(data)):
#     fix = 0
#     for i in range(len(data[j]["questions"])):
#         num = data[j]["questions"][i]["num"]
#         if num != i + 1 + fix:
#             print(data[j]["questions"][i])
#             if num == data[j]["questions"][i - 1]["num"]:
#                 fix -= 1
#             else:
#                 fix += 1
print(count)
with open("output/data.json", "w", encoding="UTF-8") as js_file:
    js_file.write(json.dumps(data, indent=4, ensure_ascii=False))
