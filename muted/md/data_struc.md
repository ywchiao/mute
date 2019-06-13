

* structure

   | entity | type |  component  |
   | ------ | ---- | ----------- |
   | entity | room | brief       |
   | entity | room | description |
   | entity | room | hit_point   |
   | entity | room | exp_point   |
   | entity | room | exp_point   |

   * at_room
     - user_id -> room_id

   + binding:
     - socket -> user_id
     - not stored

   * entity:
     - room_type -> room_type_id
     - npc_type -> npc_type_id

   * exit:
     - room_id -> { "cmd": room_id }

   * guest:
     - room_id -> [ (socket, user_id) ]
     - not stored

   * npc:
     - npc_id -> npc_type => entity

   * passer:
     - room_id -> [ npc_id ]

   * role:
     - login_id -> user_id
 
   * room:
     - room_id -> room_type => entity

