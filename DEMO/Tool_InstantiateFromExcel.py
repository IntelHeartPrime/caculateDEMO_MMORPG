import DEMO
'''
python读取excel文件代码：
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 读取excel数据
# 小罗的需求，取第二行以下的数据，然后取每行前13列的数据
import xlrd
data = xlrd.open_workbook('test.xls') # 打开xls文件
table = data.sheets()[0] # 打开第一张表
nrows = table.nrows # 获取表的行数
for i in range(nrows): # 循环逐行打印
if i == 0: # 跳过第一行
continue
print table.row_values(i)[:13] # 取前十三列
'''
import xlrd

def instantiateHero():
    data=xlrd.open_workbook('HERO.xls')
    table=data.sheets()[0]
    list_length=0
    caculated=True
    nrows=table.nrows
    for x in range(nrows):
        print (table.row_values(x))# list
        if caculated:
            for y in table.row_values(x):
                list_length+=1
            print(list_length)
            caculated=False

    # 根据列数创建实例列表
    heros=[]
    for x in range(list_length-1):
        hero=DEMO.Hero()
        heros.append(hero)
    #赋值
    for x in range(0,nrows):
        index=0
        for y in table.row_values(x)[1:]:
            if x==0:
                heros[index].name=y
                index+=1
            if x==1:
                heros[index].Hp=float(y)
                index+=1
            if x==2:
                heros[index].Magic=float(y)
                index+=1
            if x==3:
                heros[index].power=float(y)
                index+=1
            if x==4:
                heros[index].speed=float(y)
                index+=1
            if x==5:
                heros[index].intelligance=float(y)
                index+=1
            if x==6:
                heros[index].physical_resistance=float(y)
                index+=1
            if x==7:
                heros[index].magic_resistance=float(y)
                index+=1
    return heros

def instantiateMonster():
    data = xlrd.open_workbook('MONS.xls')
    table = data.sheets()[0]
    list_length = 0
    caculated = True
    nrows = table.nrows
    for x in range(nrows):
        print(table.row_values(x))  # list
        if caculated:
            for y in table.row_values(x):
                list_length += 1
            print(list_length)
            caculated = False

    # 根据列数创建实例列表
    monsters = []
    for x in range(list_length - 1):
        monster = DEMO.Monster()
        monsters.append(monster)
    # 赋值
    for x in range(0, nrows):
        index = 0
        for y in table.row_values(x)[1:]:
            if x==0:
                monsters[index].name=y
                index+=1
            if x == 1:
                monsters[index].Hp = float(y)
                index += 1
            if x == 2:
                monsters[index].attack =float(y)
                index += 1
            if x == 3:
                monsters[index].physical_resistance = float(y)
                index += 1
            if x == 4:
                monsters[index].magic_resistance = float(y)
                index += 1
            if x == 5:
                monsters[index].experience_Get = float(y)
                index += 1
    return monsters

def instantiateSkill():
    data = xlrd.open_workbook('SKILL.xls')
    table = data.sheets()[0]
    list_length = 0
    caculated = True
    nrows = table.nrows
    for x in range(nrows):
        print(table.row_values(x))  # list
        if caculated:
            for y in table.row_values(x):
                list_length += 1
            print(list_length)
            caculated = False

    # 根据列数创建实例列表
    skills = []
    for x in range(list_length - 1):
        skill = DEMO.Skill()
        skills.append(skill)
    # 赋值
    for x in range(0, nrows):
        index = 0
        for y in table.row_values(x)[1:]:
            if x == 0:
                skills[index].name = y
                index += 1
            if x == 1:
                skills[index].hurt_factor= float(y)
                index += 1
            if x == 2:
                skills[index].physicalHarm = float(y)
                index += 1
            if x == 3:
                skills[index].magicHarm = float(y)
                index += 1
            if x == 4:
                skills[index].AOE = float(y)
                index += 1
            if x == 6:
                skills[index].cd = float(y)
                index += 1
            if x==7:
                skills[index].Consume = float(y)
                index+=1
            if x==8:
                skills[index].master=y
                index+=1
    return skills

heros=instantiateHero()
monsters=instantiateMonster()
skills=instantiateSkill()