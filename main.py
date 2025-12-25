import time
from setting import *
from task import Task
import pandas as pd
import os
import subprocess

def check(tasks, user):
    sul = os.path.exists(os.path.join(USERS_DIR, user, PROGRAM_DIR, SUL_NAME))
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
        with open(os.path.join(USERS_DIR, user, PROGRAM_DIR, "res.txt"), 'w') as f:
            f.write("Результат\n")

        notes = ""
        for task in tasks:
            score_temp = 0

            for i in task:
                error = ""
                with open(os.path.join(USERS_DIR, user, PROGRAM_DIR, "input.txt"), "w") as f:
                    f.write(i[0])

                try:
                    subprocess.run(f"cd {os.path.join(USERS_DIR, user, PROGRAM_DIR)}; ./{SUL_NAME}", shell=True, capture_output=True, text=True, timeout=TIME_OUT)
                except:
                    error = "TE"
                if error == "":
                    with open(os.path.join(USERS_DIR, user, PROGRAM_DIR, "output.txt"), "r+") as f:
                        user_answ = f.read()
                        if task.score_str == -1:
                            # print(user_answ.split("\n")[1])
                            if user_answ == i[1]:
                                score_temp += 1
                        else:
                            if user_answ.split("\n")[task.score_str] == i[1]:
                                score_temp += 1
                else:
                    notes = error

                os.remove(os.path.join(USERS_DIR, user, PROGRAM_DIR, "input.txt"))
                os.remove(os.path.join(USERS_DIR, user, PROGRAM_DIR, "output.txt"))

            score_final = 0
            if task.type == "FULL" and len(task) == score_temp:
                    score_final = task.score
            elif task.type == "PART":
                score_final = int(score_temp / len(task) * task.score)

            res.append(str(score_final) + notes)
            print(notes)
            with open(os.path.join(USERS_DIR, user, PROGRAM_DIR, "res.txt"), "a") as f:
                f.write(f"{str(task)}: {score_final} {notes}\n")

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
