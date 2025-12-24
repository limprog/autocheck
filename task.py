import os
from setting import *


class Task:
    def __init__(self, file_name):
        self.file_name = file_name
        self.tests = []

        in_file = open(os.path.join(INPUT_DIR, file_name), 'r')
        tests = in_file.read().split("-")
        in_file.close()
        info = tests[0].split(";")
        tests = tests[1:]
        self.score = int(info[1][:-1])
        self.type = info[0]
        tests = [tests[i][1:-1] if i != len(tests) - 1 else tests[i][1:] for i in range(len(tests))] # чтобы убрать не нужные \n
        out_file = open(os.path.join(OUTPUT_DIR, file_name), 'r')
        out = out_file.read().split("-")[1:]
        out = [out[i][1:-1] if i != len(out) - 1 else out[i][1:] for i in range(len(out))]
        print(out)
        if len(tests) != len(out):
            raise Exception("Tests do not match")

        for i in range(len(tests)):
            self.tests.append((tests[i], out[i]))

    def __iter__(self):
        return iter(self.tests)

    def __len__(self):
        return len(self.tests)

    def __str__(self):
        return str(self.file_name.split(".")[0])
