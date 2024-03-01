import json

with open("output/chemistry.json", "r", encoding="UTF-8") as js_file:
    data = json.load(js_file)

for subject in data:
    for question in subject["questions"]:
        number = question["num"]
        question.pop("num")
        question["number"] = number

with open("output/chemistry.json", "w", encoding="UTF-8") as js_file:
    js_file.write(json.dumps(data, indent=2, ensure_ascii=False))
