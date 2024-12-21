import sys
file1 = sys.argv[1]
file2 = sys.argv[2]

EXCLUDE = {"pytz", "python-apt", "pyxdg", "pygobject", "idna"}

def load_file(file_name):
    with open(file_name) as f:
        deps1 = {x[0]:x[1] for x in map(lambda i:i.strip().split("=="),f)}
    return deps1

deps1 = load_file(file1)
deps2 = load_file(file2)

keys = sorted(deps1.keys(), key=lambda x: x.lower())

for k in keys:
    if k in EXCLUDE:
        continue
    if not k in deps2:
        pass
        #print(f"#{k}=={deps1[k]}")
    else:
        print(f"{k}=={deps2[k]}")



