# -*- coding: utf-8 -*-

import csv

def  获取板块分类(板块文件名):
    # with open(".\板块分类\\" + 板块文件名 + ".csv", "r") as csvfile:
    #     read = csv.reader(csvfile)
    #     stock_block = [];
    #     next(read)
    #     for i in read:
    #         stock_block.append(i[3])
    #     return list(set(stock_block))

    with open(".\板块分类\\" + 板块文件名 + ".csv", "r") as csvfile:
        文件索引 = csv.reader(csvfile)
        板块名 = [];
        next(文件索引)
        for i in 文件索引:
            板块名.append(i[3])
        return list(set(板块名))


if __name__ == "__main__":
    板块名 = 获取板块分类("概念分类")
    print(板块名)
