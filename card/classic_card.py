from card.basic_card import *


# 闪电箭
class LightingBolt(SpellPointOppo):
    spell_type = SPELL_POINT_OPPO
    bias = -4

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        spell_power = state.my_total_spell_power
        damage = 3 + spell_power + cls.plan_additional
        best_delta_h = state.oppo_hero.delta_h_after_damage(damage)
        best_oppo_index = -1

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_spell:
                continue
            delta_h = oppo_minion.delta_h_after_damage(damage)
            if best_delta_h < delta_h:
                best_delta_h = delta_h
                best_oppo_index = oppo_index

        return best_delta_h + cls.bias, best_oppo_index,

# 盾牌格挡
class AmorBlock(SpellNoPoint):
    keep_in_hand_bool = False

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        best_h = state.my_hero.delta_h_after_amor(5)
        if state.my_hero.health <= 9:
            best_h += 2
        #如果我方优势增加分数
        if state.my_heuristic_value -6 > state.oppo_heuristic_value :
            best_h = best_h + state.my_heuristic_value - state.oppo_heuristic_value -5

        #获取是否有盾猛和使用盾猛的费用
        hand_card = state.my_hand_cards[hand_card_index]
        if state.my_last_mana > hand_card.current_cost + 1:
            amorSlams_delta_h = 0
            for another_index, hand_card in enumerate(state.my_hand_cards):
                detail_card = hand_card.detail_card
                if another_index == hand_card_index:
                    continue
                if detail_card is None:
                    continue
                #如果有，计算加5攻击后的结果
                elif hand_card.card_id == "VAN_EX1_410":
                    
                    detail_card.plan_additional = 5
                    amorSlams_delta_h,*args = detail_card.best_h_and_arg(state, another_index)
                    detail_card.plan_additional = 0
                    amorSlams_delta_h -= 1
                    
                    if amorSlams_delta_h > best_h:
                        best_h = amorSlams_delta_h
                    break
        return best_h,

# 装甲师
class AromrMaeker(MinionNoPoint):
    
    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        delta_h = 2
        #taunt
        for my_minion in state.my_minions:
            if my_minion.taunt and not my_minion.stealth:
                delta_h += 0.6
            else:
                delta_h += 0.4
        #对面1血怪
        if state.my_total_mana <= 2:
            for oppo_minion in state.oppo_minions:
                if oppo_minion.health == 1:
                    delta_h += 4
        return delta_h,


# 盾猛
class AmorSlams(SpellPointOppo):
    keep_in_hand_bool = False
    spell_type = SPELL_POINT_OPPO
    bias = -5

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        best_delta_h = 0
        best_oppo_index = -1
        if cls.plan_additional != 0 :
            print("附加攻击引入成功")
        
        spell_power = state.my_total_spell_power
        damage = state.my_hero.armor + cls.plan_additional + spell_power

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_spell:
                continue
            delta_h = oppo_minion.delta_h_after_damage(damage)
            if best_delta_h < delta_h:
                best_delta_h = delta_h
                best_oppo_index = oppo_index

        return best_delta_h + cls.bias, best_oppo_index,


# 呱
class Hex(SpellPointOppo):
    bias = -6
    keep_in_hand_bool = False

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        best_delta_h = 0
        best_oppo_index = -1

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_spell:
                continue

            delta_h = oppo_minion.heuristic_val - 1

            if best_delta_h < delta_h:
                best_delta_h = delta_h
                best_oppo_index = oppo_index

        return best_delta_h + cls.bias, best_oppo_index,


# 闪电风暴
class LightningStorm(SpellNoPoint):
    bias = -10

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        h_sum = 0
        spell_power = state.my_total_spell_power +cls.plan_additional

        for oppo_minion in state.oppo_minions:
            h_sum += (oppo_minion.delta_h_after_damage(2 + spell_power) +
                      oppo_minion.delta_h_after_damage(3 + spell_power)) / 2

        return h_sum + cls.bias,
# 乱斗
class DesperateFighting(SpellNoPoint):
    bias = -5
    keep_in_hand_bool = False
    
    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):

        # 优势不能乱斗
        if state.my_heuristic_value >= state.oppo_heuristic_value:
            return cls.bias,
        #如果对方minion3个以上，并且比我们属性多
        if state.oppo_minion_num >= 3:
            dfValue = state.oppo_heuristic_value - state.my_heuristic_value + cls.bias
            # print("乱斗得分为")
            # print(dfValue)
            return dfValue,
        return cls.bias,
        
    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        state.my_all_minion_attack_hero()
        click.choose_and_use_spell(card_index, state.my_hand_card_num)
        click.cancel_click()
        time.sleep(cls.wait_time)

# 旋风斩
class fufufu(SpellNoPoint):
    bias = -3
    keep_in_hand_bool = False

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        spell_power = state.my_total_spell_power
        car_damage = spell_power + 1 + cls.plan_additional
        h_sum = 0
        for oppo_minion in state.oppo_minions:
            h_sum += oppo_minion.delta_h_after_damage(car_damage)
        for my_minion in state.my_minions:
            h_sum -= my_minion.delta_h_after_damage(car_damage)
        return h_sum+cls.bias,


# 加盾男爵
class buinYou(MinionNoPoint):
    value = 2
    keep_in_hand_bool = False

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        h_sum = 0
        for oppo_minion in state.oppo_minions:
            h_sum += oppo_minion.delta_h_after_damage(2)
        for my_minion in state.my_minions:
            h_sum -= my_minion.delta_h_after_damage(2)
        h_sum += state.oppo_hero.delta_h_after_damage(2)
        h_sum -= state.my_hero.delta_h_after_damage(2)
        return cls.value + h_sum,

# TC130
class MindControlTech(MinionNoPoint):
    value = 0
    keep_in_hand_bool = False

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        if state.oppo_minion_num < 4:
            return cls.value, state.my_minion_num
        else:
            h_sum = sum([minion.heuristic_val for minion in state.oppo_minions])
            h_sum /= state.oppo_minion_num
            return h_sum * 2,

# 女王
class Sylvanas(MinionNoPoint):
    keep_in_hand_bool = False

    @classmethod
    def bias_dead_delta_h(self,state,my_index,oppo_index):
        oppo_minion = state.oppo_minions[oppo_index]
        my_minion = state.my_minions[my_index]
        
        #女王亡语
        target_minion_dead = oppo_minion.get_damaged(my_minion.attack)
        tmp_delta_h = 0
        hear_dead_minion_heuristic_val = 0
        hear_dead_minion_count  = len(state.touchable_oppo_minions)

        # debug_print("女王亡语计分")
        # debug_print(target_minion_dead)
        if not target_minion_dead or hear_dead_minion_count != 1:
            for hear_dead_index,hear_dead_minion in \
                enumerate(state.touchable_oppo_minions):
                #如果被攻击的随从死了，不计算
                if hear_dead_index == oppo_index and target_minion_dead:
                    hear_dead_minion_count -= 1
                    continue
                hear_dead_minion_heuristic_val += hear_dead_minion.heuristic_val
            # debug_print(f"对方总分： {hear_dead_minion_heuristic_val}")
            tmp_delta_h += hear_dead_minion_heuristic_val/hear_dead_minion_count
        # debug_print(f"分：{tmp_delta_h}")
        return tmp_delta_h



# 野性狼魂
class FeralSpirit(SpellNoPoint):
    value = 2.4

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        if state.my_minion_num >= 6:
            return -1, 0
        else:
            return cls.value, 0


# 碧蓝幼龙
class AzureDrake(MinionNoPoint):
    value = 3.5
    keep_in_hand_bool = False


# 奥妮克希亚
class Onyxia(MinionNoPoint):
    value = 10
    keep_in_hand_bool = False


# 火元素
class FireElemental(MinionPointOppo):
    keep_in_hand_bool = False

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        best_h = 3 + state.oppo_hero.delta_h_after_damage(3)
        best_oppo_index = -1

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_minion:
                continue

            delta_h = 3 + oppo_minion.delta_h_after_damage(3)
            if delta_h > best_h:
                best_h = delta_h
                best_oppo_index = oppo_index

        return best_h, state.my_minion_num, best_oppo_index


# 泄法
class xieFa(MinionNoPoint):
    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        best_h = 1.1
        this_card = state.my_hand_cards[hand_card_index]
        if state.my_last_mana > this_card.current_cost:
            spellPower_delta_h = 0

            for another_index, hand_card in enumerate(state.my_hand_cards):
                detail_card = hand_card.detail_card
                if another_index == hand_card_index:
                    continue
                if detail_card is None:
                    continue
                #如果是法术，并且可以一起用
                elif hand_card.cardtype == "SPELL" and \
                    state.my_last_mana > this_card.current_cost + hand_card.current_cost:
                    
                    detail_card.plan_additional = 1
                    spellPower_delta_h,*args = detail_card.best_h_and_arg(state, another_index)
                    detail_card.plan_additional = 0
                    spellPower_delta_h -= 1

                    if spellPower_delta_h > best_h:
                        best_h = spellPower_delta_h

        return best_h,

# 精灵弓箭手
class ElvenArcher(MinionPointOppo):
    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        # 不能让她下去点脸, 除非对面快死了
        best_h = -0.8 + state.oppo_hero.delta_h_after_damage(1)
        best_oppo_index = -1

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_minion:
                continue

            delta_h = -0.5 + oppo_minion.delta_h_after_damage(1)
            if delta_h > best_h:
                best_h = delta_h
                best_oppo_index = oppo_index

        return best_h, state.my_minion_num, best_oppo_index


# 大地之环先知
class EarthenRingFarseer(MinionPointMine):
    
    #打分
    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        #判断恢复英雄
        #1加上恢复英雄3血的得分
        best_h = 1.3 + state.my_hero.delta_h_after_heal(3)
        
        #如果英雄血量低于9点，提高得分
        if state.my_hero.health + state.my_hero.armor <= 9:
            best_h += 2
        best_my_index = -1

        #判断恢复随从
        for my_index, my_minion in enumerate(state.my_minions):
            #0.5加上恢复随从3血的得分
            delta_h = -0.5 + my_minion.delta_h_after_heal(3)
            #得出最高分
            if delta_h > best_h:
                best_h = delta_h
                best_my_index = my_index

        return best_h, state.my_minion_num, best_my_index


# 憎恶
class Abomination(MinionNoPoint):
    keep_in_hand_bool = False

    @classmethod
    def attack_target_delta_h(cls, state,my_index,oppo_index):
        oppo_minion = state.oppo_minions[oppo_index]
        if oppo_minion.health <=2:#两血怪亡语就解了
            return -2
        else:
            return 2

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        h_sum = 0
        for oppo_minion in state.oppo_minions:
            h_sum += oppo_minion.delta_h_after_damage(2)
        for my_minion in state.my_minions:
            h_sum -= my_minion.delta_h_after_damage(2)
        h_sum += state.oppo_hero.delta_h_after_damage(2)
        h_sum -= state.my_hero.delta_h_after_damage(2)

        return h_sum,
        


# 狂奔科多兽
class StampedingKodo(MinionNoPoint):
    keep_in_hand_bool = False

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        h_sum = 2
        temp_sum = 0
        temp_count = 0

        for oppo_minion in state.oppo_minions:
            if oppo_minion.attack <= 2:
                temp_sum += oppo_minion.heuristic_val
                temp_count += 1
        if temp_count > 0:
            h_sum += temp_sum / temp_count

        return h_sum,


# 血骑士
class BloodKnight(MinionNoPoint):
    keep_in_hand_bool = False

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        h_sum = 1

        for oppo_minion in state.oppo_minions:
            if oppo_minion.divine_shield:
                h_sum += oppo_minion.attack + 6
        for my_minion in state.my_minions:
            if my_minion.divine_shield:
                h_sum += -my_minion.attack + 6

        return h_sum,


# 末日
class DoomSayer(MinionNoPoint):
    keep_in_hand_bool = True

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        # 一费别跳末日
        if state.my_total_mana == 1:
            return 0,

        # 二三费压末日就完事了
        if state.my_total_mana <= 3:
            return 1000,

        sceneSituation = state.scene_situation()
        # 优势不能上末日
        if sceneSituation >= 0:
            return 0,

        oppo_attack_sum = 0
        for oppo_minion in state.oppo_minions:
            oppo_attack_sum += oppo_minion.attack

        if oppo_attack_sum >= 7:
            # 当个嘲讽也好
            return 1,
        else:
            return sceneSituation * -1,

#雷铸战斧
class StormforgedAxe(WeaponCard):
    keep_in_hand_bool = True
    value = 1.5

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        # 不要已经有刀了再顶刀
        if state.my_weapon is not None:
            return 0,
        delta_h = 1
        if state.my_total_mana >= 2:
            for oppo_minion in state.touchable_oppo_minions:
                # 如果能提起刀解了, 那太好了
                if oppo_minion.health <= 2 and \
                        not oppo_minion.divine_shield:
                    one_delta_h = oppo_minion.delta_h_after_damage(3)
                    if delta_h < one_delta_h:
                        delta_h = one_delta_h

        return cls.value+delta_h-1,
        
#小斧子
class RedBurnAxe(WeaponCard):
    keep_in_hand_bool = True
    value = 1.2

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        # 不要已经有刀了再顶刀
        if state.my_weapon is not None:
            return 0,
        delta_h = 2
        for oppo_minion in state.touchable_oppo_minions:
            # 如果能提起刀解了, 那太好了
            if oppo_minion.health <= 3 and \
                    not oppo_minion.divine_shield:
                one_delta_h = oppo_minion.delta_h_after_damage(3)
                if delta_h < one_delta_h:
                    delta_h = one_delta_h

        if state.my_total_mana > 3:
            delta_h *= 0.5
        # print(f"小斧子：{delta_h}")
        return cls.value+delta_h-2,
