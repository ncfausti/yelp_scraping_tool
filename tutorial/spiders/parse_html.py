import os


def parse():
    count = 0

    for fname in os.listdir('./pull2'):
        count += 1

    print(count)
