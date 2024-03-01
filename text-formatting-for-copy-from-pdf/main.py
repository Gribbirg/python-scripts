enterFile = open("enter.txt", encoding='utf-8')
resultFile = open("result.txt", "w")

for line in enterFile:
    if line[:-1].isdecimal():
        continue
    elif 'а' <= line[0] <= 'я':
        resultFile.write(line[:-1] + " ")
    else:
        resultFile.write("\n" + line[:-1] + " ")

enterFile.close()
resultFile.close()
