# Summon item back & restore item frame
$loot spawn ~ ~ ~ loot christmasdeco:$(christmasdeco_id)
summon minecraft:item_frame ~ ~ ~ {Facing:1b}

# Kill triggerbox, christmasdeco origin and all of its children (all related christmasdeco model entities)
execute positioned as @s run kill @n[type=interaction,tag=christmasdeco_triggerbox,distance=..2,nbt={attack:{}}]
execute on passengers run kill @s
kill @s