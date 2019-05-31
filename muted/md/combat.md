
* 屬性
    1. strength: 力量

      + +damage

    1. constitution: 體質

      + +hp (hitpoints)

    1. dexterity:

      + +dodge

    1. intelligence:

      + +critical (-hit)

    1. perception: 感知

      + +parry
      + +aggro_radius (mob)

    1. wisdom:

    1. luck:

      + loot

    1. focus: 專注

     + -parry

    1. spirit: 精神

     + +wp (willpower)

* defence 防禦

* Resilience 抗性

    1. fire

    1. ice

    1. poison

* Speed 攻速

    1. Cool Down 以秒數表示，代表攻擊間隔

* 百面骰

  + Base:

    1. hit      90%

    1. miss     5%

    1. critical 5%

    1. dodge    5%

    1. parry    5%

  + normalized:

    1. hit       67.5%

    1. miss      10%

    1. critical  9%

    1. dodge     4.5%

    1. parry     9%

* de/buff:
    1. add base attribute -> stats system/add components

    1. add %              -> (+hit, -miss)
                             (+critical, -hit)
                             +dodge/+block

    1. add scalar         -> +power/+defence/+hp/+wp

* flow:

    1. AttackSystem 檢查 CD，產生 Attacked 物件 (紀錄攻擊強度)；

    1. AttackSystem 將 (AttackedEntity, Attacked) 置入 AttackedComponent

    1. AttackedComponent = {
         attackedEntity: Attack power
       }

    1. DefendSystem 遍歷 AttackedComponent

    1. DefendSystem 依據 Attacked 攻擊力，AttackedEntity 的防禦力，
       算出 Damaged 物件

    1. DefendSystem 將 (AtteckedEntity, Damaged) 物件置入 DamagedComponent

* 範圍技能

    1. 範圍技能 (aoe) 綁在區域上；而不是 avatar。

