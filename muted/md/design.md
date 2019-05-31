<!---
  @file       design.md
  @brief      The design notes about the RAID project.
  @author     Yiwei Chiao (ywchiao@gmail.com)
  @date       10/12/2018 created.
  @date       10/12/2018 last modified.
  @version    0.1.0
  @since      0.1.0
  @copyright  CC-BY, © 2018 Yiwei Chiao
-->

## 隨機地圖演算法

1. 由地圖大小設定覆蓋率

1. rooms <- []

1. 隨機地點，建立一個隨機大小的房間 (lobby)

1. rooms.push(lobby)

1. 重複以下直到目前覆蓋率達標

1. 由 rooms 裡，隨機選一個房間 room

1. 在 room 隨機選一面牆

1. 在牆上，隨機找一個位置開洞 (門)

1. 選定的位置不能開門，回到選房間

1. 在開門的方向，建一個隨機大小的房間 (built)

1. 新建房間和既存房間重疊，回到選房間

1. 設定 room, exit 和新建房間 (built) 的關係

1. rooms.push(built)

1. 回去檢查覆蓋率


## 座標系統

  座標系統分為：

  1. 世界座標 - 以 px 為單位，所有 mob (可移動物體) 使用這個座標

  1. 地圖座標 - 以 tile 為單位，所有不可移動物體，使用這個座標

  1. 螢幕座標 - 以 px 為單位，顯示用；玩家角色使用這個座標

