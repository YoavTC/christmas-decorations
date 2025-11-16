advancement revoke @s only christmasdeco:events/on_place

execute positioned as @s rotated as @s anchored eyes positioned ^ ^ ^2 as @n[type=item_frame,nbt={Item:{components:{"minecraft:custom_data":{christmasdeco:1b}}}},distance=..2] positioned as @s run function christmasdeco:setup_christmasdeco with entity @s Item.components.minecraft:custom_data