import re


# 获取文本中匹配的行
def get_line_by_pattern(file_path, pattern):
    with open(file_path, 'r') as f:
        for line in f.readlines():
            if re.search(pattern, line):
                yield line


# 获取文本中匹配 [rows: 的行
def get_line_by_rows(file_path):
    return get_line_by_pattern(file_path, r'\[rows:')


# 获取SQL执行耗时,'['和'ms]'之间的数字
def get_sql_time(line):
    return re.findall(r'\[(.+?)ms\]', line)[0]


# 统计SQL执行耗时不同区间的个数及SQL语句
# 返回0-1ms,1ms-5ms,5ms-10ms,10ms+的个数，5ms-10ms的SQL语句,10ms+的SQL语句
def count_sql_time(file_path):
    count_0_1 = 0
    count_1_5 = 0
    count_5_10 = 0
    count_10 = 0
    sql_5_10 = []
    sql_10 = []
    for line in get_line_by_rows(file_path):
        sql_time = float(get_sql_time(line))
        if sql_time <= 1:
            count_0_1 += 1
        elif sql_time <= 5:
            count_1_5 += 1
        elif sql_time <= 10:
            count_5_10 += 1
            sql_5_10.append(line)
        else:
            count_10 += 1
            sql_10.append(line)
    return count_0_1, count_1_5, count_5_10, count_10, sql_5_10, sql_10


# 打印统计结果，并将5ms以上耗时的SQL语句写入文件
# 写文件时进行去重
def print_sql_time(file_path):
    count_0_1, count_1_5, count_5_10, count_10, sql_5_10, sql_10 = count_sql_time(file_path)
    print('0-1ms: %s' % count_0_1)
    print('1-5ms: %s' % count_1_5)
    print('5-10ms: %s' % count_5_10)
    print('10ms+: %s' % count_10)
    print('all: %s' % (count_0_1 + count_1_5 + count_5_10 + count_10))
    with open('sql_5_10.txt', 'w') as f:
        f.write('\n'.join(list(set(sql_5_10))))
    with open('sql_10.txt', 'w') as f:
        f.write('\n'.join(list(set(sql_10))))


if __name__ == '__main__':
    file_path = 'test.txt'
    print_sql_time(file_path)
