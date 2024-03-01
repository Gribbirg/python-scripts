import json

data = []

with open("input/data.txt", "r", encoding="UTF-8") as txt_file:
    content = [line.strip() for line in txt_file.readlines()]

for i in range(len(content)):
    if not ('0' <= content[i][0] <= '9') and content[i][0] != "!":
        j = i - 1
        while len(content[j]) == 0:
            j -= 1
        if content[j][-1] != " " and content[i][0] != " ":
            content[j] += " "
        content[j] += content[i]
        content[i] = ""

for line in content:
    if len(line) == 0:
        continue
    elif line[2] != " " and line[3] != " " and line[4] != " ":
        print("No space on line: " + line)
    elif line[0] == "!":
        data.append({"name": " ".join(line.split(" ")[1:]), "questions_count": 0, "questions": []})
    elif line.split(" ")[0].find(")") == -1:
        data[-1]["questions"].append(
            {"name": " ".join(line.split(" ")[1:]), "number": data[-1]["questions_count"] + 1, "answers_count": 0,
             "answers": []})
        data[-1]["questions_count"] += 1
    elif line.split(" ")[0].find(")") != -1:
        data[-1]["questions"][-1]["answers"].append(" ".join(line.split(" ")[1:]))
        data[-1]["questions"][-1]["answers_count"] += 1
    else:
        print("Error on line: " + line)

with open("output/data.json", "w", encoding="UTF-8") as js_file:
    js_file.write(json.dumps(data, indent=4, ensure_ascii=False))
