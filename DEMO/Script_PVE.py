import Tool_InstantiateFromExcel
import DEMO
import sys

'''
# 重定向输出流
import sys
f=open('result_PVP.txt','w')
old=sys.stdout #将当前系统输出储存到一个临时变量中
sys.stdout=f  #输出重定向到文件
'''
#中间代码
'''
sys.stdout=old #还原原系统输出
f.close()
'''

class PVE:
    def __init__(self):
        '''
        创建英雄列表
        创建技能列表
        为英雄添加技能
        生成怪物列表
        工厂模式的怪物生成器，当有怪物死亡时便在敌人列表中添加怪物，直至英雄死亡

        每创建一个新的实例，更新一次ID
        '''
        self.ID=0

        self.heros=Tool_InstantiateFromExcel.instantiateHero()
        for x in self.heros:
            x.ID=self.ID
            self.ID+=1

        self.skills=Tool_InstantiateFromExcel.instantiateSkill()
        for x in self.skills:
            x.ID=self.ID
            self.ID+=1

        self.monsters=Tool_InstantiateFromExcel.instantiateMonster()

        for hero in self.heros:
            for skill in self.skills:
                if skill.master==hero.name:
                    if hero.SkillA==None:
                        hero.SkillA=skill
                    if hero.SkillB==None:
                        hero.SkillB=skill

        self.enemys=[]    # 敌人列表，通过方法进行动态填充

    def getMonster(self,monster_name):
        '''
        :param monster_name: 要创建的怪物的名称
        :return: 返回一个相关的实例
        '''
        monster=DEMO.Monster()
        monster.name=monster_name
        for x in self.monsters:
            if monster.name==x.name:
                # 属性复制
                monster.Hp=x.Hp
                monster.Hp_store=x.Hp_store
                monster.attack=x.attack
                monster.physical_resistance=x.physical_resistance
                monster.magic_resistance=x.magic_resistance
                monster.experience_Get=x.experience_Get
                monster.ID=self.ID
                self.ID+=1
        return monster

    def removeIFDIED(self):
        while True:
            canEXIT=True
            for x in self.enemys:
                if x.ISDIED:
                    self.enemys.remove(x)
            for x in self.enemys:
                if x.ISDIED:
                    canEXIT=False
            if canEXIT:
                return

    def caculate(self,monster_name):
        '''
        开始试算：
        试算策略：
            1，英雄逐个攻击小怪、中怪，大型怪物，boss
            2，死亡后换下一个英雄
        '''
        for hero in self.heros:
            while True:
                if hero.ISDIED:
                    break
                # 列表中小于10个怪物则添加到10个
                if len(self.enemys)<=10:
                    self.enemys.append(self.getMonster(monster_name))
                hero.action()
                hero.action_attack(self.enemys[0])
                # 添加反击： 被攻击的怪物同时攻击玩家
                for monster in hero.enemys_list:
                    monster.unit.action_attack(hero)
                #死亡剔除
                self.removeIFDIED()
                hero.action_SkillA(self.enemys)
                self.removeIFDIED()
                hero.action_SikllB(self.enemys)
                self.removeIFDIED()



f=open('result_PVE_小型怪物.txt','w')
old=sys.stdout #将当前系统输出储存到一个临时变量中
sys.stdout=f  #输出重定向到文件
pve=PVE()
pve.caculate('小型怪物')
sys.stdout=old #还原原系统输出
f.close()