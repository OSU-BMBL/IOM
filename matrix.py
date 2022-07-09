import argparse
import os
import re


# Parse arguments
parser = argparse.ArgumentParser(description='filtered reads')
parser.add_argument('-input', default=None,help='import filter reads file')

args = parser.parse_args()

# extract path
path = os.path.dirname(args.input)
# path = os.path.dirname(path)
# path1=path.split('/')
file = path+'/'+ "read_count_label.tsv"


# ss_ = re.search(r'p[0-9]{2}', path, flags=0)
# sss_ = ss_.group()
# ss = re.search(r'[0-9]{2}', sss_, flags=0)
# sss = int(ss.group())
print(args.input)


f = open(args.input)
col = []
row = []
# arr=[[] for i in range(3)]
dic = {}
x = f.readline()
while x:
    srow = x.split('|')[-1].strip()
    scol = x.split("_")[1]
    # w.write(str(scol) + '\n')
    if scol not in col :
        col.append(scol)
    if srow not in row:
        row.append(srow)
    s = srow+scol
    if s not in dic.keys():
        dic[s] = 1
    else:
        dic[s] += 1    
    f.readline()
    f.readline()
    f.readline()
    x = f.readline()
f.close()

print('col    ' + str(len(col)) + '\trow\t' + str(len(row)) + '\n')
fp = open(file,'w')
fp.write('\t')

for l in col:
    fp.write(l + '\t')
fp.write('\n')
for i in range(len(row)):
    fp.write(row[i] + '\t')
    for j in range(len(col)):
        a = row[i]+col[j]
        if a in dic.keys():
            fp.write(str(dic[a]) + "\t")
            del(dic[a])
        else:
            fp.write('0\t')
    fp.write('\n')
fp.close()

