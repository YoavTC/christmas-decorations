# Spawn origin container & triggerbox
$summon interaction ~ ~-0.03 ~ {data:{christmasdeco_id:"$(christmasdeco_id)"},Tags:[christmasdeco_origin,christmasdeco_origin_unset],width:0,height:0}
$summon interaction ~ ~-0.03 ~ {Tags:[christmasdeco_triggerbox],width:$(christmasdeco_width),height:$(christmasdeco_height)}

$execute unless predicate christmasdeco:in_item_frame/is_floor as @n[tag=christmasdeco_triggerbox] positioned as @s run tp @s ~ ~$(christmasdeco_y_offset) ~

# Store item frame facing direction
data modify entity @n[type=interaction,tag=christmasdeco_origin] data.Facing set from entity @s Facing

# Macro spawn function
$execute if predicate christmasdeco:in_item_frame/is_floor run function christmasdeco:spawn/floor/$(christmasdeco_id)
$execute if predicate christmasdeco:in_item_frame/is_wall run function christmasdeco:spawn/wall/$(christmasdeco_id)
$execute if predicate christmasdeco:in_item_frame/is_ceiling run function christmasdeco:spawn/ceiling/$(christmasdeco_id)

# Tagging
execute as @n[tag=christmasdeco_parent,distance=..2] on passengers run tag @s add christmasdeco_unset
tag @p add christmasdeco_placer
tag @s add christmasdeco_item_frame

# Rotate towards the player
execute as @p[tag=christmasdeco_placer] store result score @s christmasdeco.dir run data get entity @s Rotation[0]
execute as @s store result score @s christmasdeco.dir run data get entity @s Rotation[0]

execute if predicate christmasdeco:in_item_frame/is_wall as @e[tag=christmasdeco_unset,distance=..2] run function christmasdeco:rotate_wall
execute unless predicate christmasdeco:in_item_frame/is_wall as @e[tag=christmasdeco_unset,distance=..2] run function christmasdeco:rotate

# Mount children to parent container
execute as @e[tag=christmasdeco_unset,distance=..2] run ride @s dismount
execute as @e[tag=christmasdeco_unset,distance=..2] run ride @s mount @n[tag=christmasdeco_origin_unset]
ride @n[tag=christmasdeco_parent,distance=..2] mount @n[tag=christmasdeco_origin_unset]

# Remove tagging
execute as @n[tag=christmasdeco_origin_unset] on passengers run tag @s remove christmasdeco_unset
tag @n[tag=christmasdeco_origin_unset] remove christmasdeco_origin_unset
tag @n[tag=christmasdeco_placer] remove christmasdeco_placer

kill @s