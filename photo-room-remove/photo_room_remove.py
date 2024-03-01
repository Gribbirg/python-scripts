import os

DIRECTORY_PATH = ""

before = []
after = []

for path in os.listdir(DIRECTORY_PATH):
    if os.path.isfile(os.path.join(DIRECTORY_PATH, path)):
        before.append(os.path.join(DIRECTORY_PATH, path))

print(before)

for image in before:
    after.append(image.replace("-PhotoRoom.png-PhotoRoom", ""))

print(after)

for i in range(len(before)):
    os.rename(before[i], after[i])
