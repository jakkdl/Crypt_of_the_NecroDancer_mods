import sys




if len(sys.argv) < 3:
    sys.exit("usage: python program.py beats_to_preserve file1 [...files]")

length = int(sys.argv[1])

for arg in sys.argv[2:]:
    print(arg)
    with open(arg, 'r') as f:
        data = f.read()
    content = data.split(',')[:length]
    content_str = ','.join(content)

    with open(arg, 'w') as f:
        f.write(content_str)


    with open(arg, 'r') as f:
        data = f.read()
