# Spawn origin container & triggerbox
$summon interaction ~ ~-0.03 ~ {data:{christmasdeco_id:"$(christmasdeco_id)"},Tags:[christmasdeco_origin,christmasdeco_origin_unset],width:0,height:0}
$summon interaction ~ ~-0.03 ~ {Tags:[christmasdeco_triggerbox],width:$(christmasdeco_width),height:$(christmasdeco_height)}

# Macro spawn function
$function christmasdeco:spawn/$(christmasdeco_id)

# Tagging
execute as @n[tag=christmasdeco_parent,distance=..2] on passengers run tag @s add christmasdeco_unset
tag @p add christmasdeco_placer

# Rotate towards the player
execute as @p[tag=christmasdeco_placer] store result score @s christmasdeco.dir run data get entity @s Rotation[0]
execute as @e[tag=christmasdeco_unset,distance=..2] run function christmasdeco:rotate

# Mount children to parent container
execute as @e[tag=christmasdeco_unset,distance=..2] run ride @s dismount
execute as @e[tag=christmasdeco_unset,distance=..2] run ride @s mount @n[tag=christmasdeco_origin_unset]
ride @n[tag=christmasdeco_parent,distance=..2] mount @n[tag=christmasdeco_origin_unset]

# Remove tagging
execute as @n[tag=christmasdeco_origin_unset] on passengers run tag @s remove christmasdeco_unset
tag @n[tag=christmasdeco_origin_unset] remove christmasdeco_origin_unset
tag @n[tag=christmasdeco_placer] remove christmasdeco_placer

kill @s