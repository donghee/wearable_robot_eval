HEADER = """{
"Loop": "none", 
"VelFilterCutoff": -1.00000, 

"RightJoints": [3,  4,  5,  6,  7,  8], 
"LeftJoints": [9,  10,  11,  12,  13,  14], 
"Frames":
[
"""

FOOTER = "]}"

def csv2json(csv_file, json_file):
    i = 0
    lines = []
    with open(csv_file, 'r') as f:
        for line in f.readlines():
            #if i % 3 == 0: # skip every 2nd, 3rd lines, little slow
            if i % 9 == 0:
                lines.append(line.strip())
            i += 1

    with open(json_file, 'w') as f:
        f.write(HEADER)

        last_line = lines[-1]
        for line in lines[:-1]:
            f.write('[' + line + '],\n')
        f.write('[' + last_line + ']\n')
        f.write(FOOTER)


csv2json('human_controller1_normal.txt', '../human_controller1_normal.txt')
csv2json('human_controller2_torqueLimit.txt', '../human_controller2_torqueLimit.txt')
csv2json('human_controller3_romLimit.txt', '../human_controller3_romLimit.txt')
