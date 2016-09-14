import  random

# Unit类


def clamp(number_1,number_2,number_3):
    '''
    :param number_1: 输入数
    :param number_2: 下界
    :param number_3: 上界
    :return: 输出数
    '''
    if number_1<=number_2:
        number_1=number_2
    if number_2>=number_3:
        number_1=number_3
    return number_1

class Unit:
    # 属性
    Hp=200
    Hp_store=200
    name='unit'
    physical_resistance=20
    magic_resistance=20
    ID=0
    ISDIED=False

# Enemy_Exp类
class Enemy_Exp:
    def __init__(self,ID,experience,unit):
        self.ID=ID
        self.experience=experience
        self.unit=unit

# 技能类
class Skill:
    name=''
    hurt_factor=1
    physicalHarm=20
    magicHarm=20
    AOE=1
    cd=10
    cd_store=10
    Consume=10
    master=None   # 技能宿主

# 英雄类
class Hero(Unit):
    def __init__(self):
        self.power=0
        self.speed=0
        self.intelligance=0
        self.Magic=200
        self.Magic_store=200

        self.LEVEL=1
        self.experience=0

        self.Hp_restore=10
        self.Magic_restore=10

        self.attack=10
        self.crit_probability=0.2
        self.crit_power=2
        self.attack_speed=1  # 将每一帧数学等效为一秒，单次平a伤害*attack_speed 为此次平a的伤害进行数学等效
        self.move_speed=300
        self.attackSpeed_lose=0
        self.moveSpeed_lose=0
        self.toughness_attack=0
        self.toughness_move=0

        self.physicalPower_add=1
        self.magicPower_add=1

        self.SkillA=None
        self.SkillB=None

        self.enemys_list=[]  #用于经验判定的数据结构

    def append_list(self,enemy):
        '''
        为enemy_list添加不重复的单位
        :param enemy: 敌人
        :return: Bool
        '''
        for x in self.enemys_list:
            if x.ID==Unit.ID:
                return False
        self.enemys_list.append(Enemy_Exp(enemy.ID,0,enemy))
        return True

    def add_Experience(self,enemy,harm):
        '''
        :param enemy: 敌人
        :param harm: 对敌人造成的伤害量
        :return: None
        '''
        for x in self.enemys_list:
            if x.ID==enemy.ID:
                x.experience+=(harm/enemy.Hp_store)*enemy.experience_Get

    # 死亡判定，列表剔除，经验结算
    def caculateExp_WhenDied(self,enemy):
        '''
        输出日志
        :param enemy: 死亡的敌人
        '''
        for x in self.enemys_list:
            if enemy.ID==x.ID:
                # 经验结算，然后剔除x
                self.experience += x.experience
                # log
                print(str(enemy.ID)+' '+enemy.name+' DIED!!')
                print(self.name + 'get experience:' + str(x.experience))
                self.enemys_list.remove(x)
                break


    def action_attack(self,enemy):
        '''
        :param Unit: 要攻击的单位
        '''
        #添加经验判定数据结构
        Bool=self.append_list(enemy)

        # 暴击判定
        harm=0
        random_number=random.randint(0,100)
        # 暴击
        if random_number<=self.crit_probability*100:
            harm=((self.power*10)*self.crit_power-(enemy.physical_resistance*10))*self.attack_speed
        # 不暴击
        if random_number>self.crit_probability*100:
            harm = ((self.power * 10) - (enemy.physical_resistance * 10)) * self.attack_speed
        # 伤害不能为负值
        if harm<=0:
            harm=0
        # 伤害结算
        enemy.Hp-=harm
        harm_caculate=0
        if enemy.Hp<=0:
            harm_caculate=harm+enemy.Hp
            enemy.Hp=0
            enemy.ISDIED=True

        #经验存储值添加
        self.add_Experience(enemy,harm_caculate)
        #死亡判定，列表剔除，经验结算
        if enemy.Hp<=0:
            self.caculateExp_WhenDied(enemy)

        # 输出战斗日志
        print(self.name+'----attack----'+enemy.name+' '+'the Harm ='+str(harm)+' '+enemy.name+'Hp='+str(enemy.Hp))

    def action_SkillA(self,enemys):
        '''
        :param enemys: 敌方单位的列表，时刻根据AOE值读取队列前端对象。更新并输出战斗日志
        列表操作算法：
        1，遍历列表，indexForAOE+=1，==AOE，break
            在此遍历过程中进行战斗判定，输出战斗日志
            -----------------------------------------
        2，遍历数组，当数组中出现死亡对象时，剔除之
            外部进行的判定，对enemys列表进行剔除
            输出死亡日志
            -----------------------------------------
        '''
        self.SkillA.cd-=1
        if self.SkillA.cd<=0:
            self.SkillA.cd=0
        if self.SkillA.cd==0 and self.Magic>=self.SkillA.Consume:
            indexForAOE=0
            self.Magic-=self.SkillA.Consume
            for x in enemys:
                #经验判定数据结构添加对象
                self.append_list(x)
                harm=((self.SkillA.physicalHarm*self.physicalPower_add-x.physical_resistance)+(self.SkillA.magicHarm*self.magicPower_add-x.magic_resistance))*self.SkillA.hurt_factor
                # 伤害不能为负值
                if harm<=0:
                    harm=0
                x.Hp-=harm
                harm_caculate=0
                if x.Hp<=0:
                    harm_caculate = harm + x.Hp
                    x.Hp=0
                    x.ISDIED=True
                # log
                print(self.name+' use Skill:'+self.SkillA.name+"  harm="+str(harm))
                #添加经验
                self.add_Experience(x,harm_caculate)
                # 死亡判定，列表剔除，经验结算
                if x.Hp==0:
                    self.caculateExp_WhenDied(x)
                indexForAOE+=1
                if indexForAOE==self.SkillA.AOE:
                    self.SkillA.cd=self.SkillA.cd_store
                    break

    def action_SikllB(self,enemys):

        self.SkillB.cd-=1
        if self.SkillB.cd<=0:
            self.SkillB.cd=0
        if self.SkillB.cd==0 and self.Magic>=self.SkillB.Consume:
            self.Magic-=self.SkillB.Consume
            indexForAOE=0
            for x in enemys:
                #经验判定数据结构添加对象
                self.append_list(x)
                harm=((self.SkillB.physicalHarm*self.physicalPower_add-x.physical_resistance)+(self.SkillB.magicHarm*self.magicPower_add-x.magic_resistance))*self.SkillB.hurt_factor
                # 伤害不能为负值
                if harm<=0:
                    harm=0
                x.Hp-=harm
                harm_caculate=0
                if x.Hp<=0:
                    harm_caculate=harm+x.Hp
                    x.Hp=0
                    x.ISDIED=True
                # log
                print(self.name + ' use Skill:' + self.SkillA.name + "  harm=" + str(harm))
                #添加经验
                self.add_Experience(x,harm_caculate)
                # 死亡判定，列表剔除，经验结算
                if x.Hp==0:
                    self.caculateExp_WhenDied(x)
                indexForAOE+=1
                if indexForAOE==self.SkillB.AOE:
                    self.SkillB.cd=self.SkillB.cd_store
                    break

    def action(self):
        '''
        action函数，更新实例的属性。
        经验--升级判定--更新等级
        自动加点--根据三大基本属性使用公式更新其它属性
        '''
        #经验-升级
        if self.experience>=(self.LEVEL-1)*(self.LEVEL-1)*(self.LEVEL-1)+1000 or self.LEVEL==1:
            self.LEVEL+=1
            caculate_once=True
            # log
            print(self.name+'LEVEL UP TO:'+str(self.LEVEL))
            self.experience=self.experience-((self.LEVEL-1)*(self.LEVEL-1)*(self.LEVEL-1)+1000)
            self.power+=2
            self.intelligance+=2
            self.speed+=2
            #update other parameters
            self.attack_speed=(self.speed*0.044+0.5)*clamp((1-self.attackSpeed_lose+self.toughness_attack),0,1)
            self.move_speed=(self.speed*10+300)*clamp((1-self.moveSpeed_lose+self.toughness_move),0,1)
            if self.LEVEL==1 and caculate_once:
                self.magicPower_add=self.intelligance/20+1
                self.physicalPower_add=self.power/20+1
                self.Hp_store=self.Hp_store+20
                caculate_once=False
            if self.LEVEL!=1:
                self.magicPower_add=self.intelligance/20+1
                self.physicalPower_add=self.power/20+1
                self.Hp_store=self.Hp_store+20


        #体力恢复，法力恢复
        self.Hp+=self.Hp_restore
        self.Magic+=self.Magic_restore
        if self.Hp>=self.Hp_store:
            self.Hp=self.Hp_store
        if self.Magic>=self.Magic_store:
            self.Magic=self.Magic_store


class Monster(Unit):
    def __init__(self):
        self.experience_Get=0
        self.attack=10
    def action_attack(self,hero):
        '''
        :param hero: 怪物要攻击的英雄
        '''
        harm=self.attack-hero.physical_resistance
        hero.Hp-=harm
        print(self.name+'-attack-'+hero.name+'--harm=:'+str(harm)+'  hero.HP剩余：'+str(hero.Hp))
        if hero.Hp<=0:
            print('Hero Die:'+hero.name)
            hero.ISDIED=True

