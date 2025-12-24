import time
from setting import *
from task import Task
import pandas as pd
import os

def check(tasks, user):
    sul = os.path.exists(os.path.join(USERS_DIR, user, SUL_NAME))
    data = pd.read_csv(os.path.join("res.csv"))
    res = []

    if not sul:
        res = [-1 for i in range(len(tasks))]
        res = [user] + res
        data.loc[len(data)] = res
        data.to_csv(os.path.join("res.csv"), index=False)
        with open(os.path.join(USERS_DIR, user, "res.txt"), 'w') as f:
            f.write("исполняймый фаил не найден")

    else:
        res.append(user)
        with open(os.path.join(USERS_DIR, user, "res.txt"), 'w') as f:
            f.write("Результат\n")
        for task in tasks:
            score_temp = 0

            for i in task:
                with open(os.path.join(USERS_DIR, user, "input.txt"), "w") as f:
                    f.write(i[0])

                os.system(f"cd {os.path.join(USERS_DIR, user)}; ./{SUL_NAME}")
                with open(os.path.join(USERS_DIR, user, "output.txt"), "r") as f:
                    if f.read() == i[1]:
                        score_temp += 1

                os.remove(os.path.join(USERS_DIR, user, "input.txt"))
                os.remove(os.path.join(USERS_DIR, user, "output.txt"))

            score_final = 0
            if task.type == "FULL" and len(task) == score_temp:
                    score_final = task.score
            elif task.type == "PART":
                score_final = int(score_temp / len(task) * task.score)

            res.append(score_final)
            with open(os.path.join(USERS_DIR, user, "res.txt"), "a") as f:
                f.write(f"{str(task)}: {score_final}\n")


        data.loc[len(data)] = res
        data.to_csv(os.path.join("res.csv"), index=False)



def main():
    input_files = os.listdir(INPUT_DIR)
    tasks = list()

    for file in input_files:
        tasks.append(Task(file))

    users = os.listdir(USERS_DIR)
    while True:
        with open(RESULT_FILE, "w") as f:
            f.write("name")
            for i in input_files:
                f.write(","+i.split(".")[0])
            f.write("\n")
            f.write("ideal")
            for t in tasks:
                f.write(","+str(t.score))
        for user in users:
            check(tasks, user)
        time.sleep(SLEEP_TIME)


if __name__ == '__main__':
    main()
