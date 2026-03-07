run('say NoMoreSkull Carpet Script Loaded')
max_count = 100
run('scoreboard objectives add wither_skull_count dummy wither_skull_count');
run('scoreboard players set wither_skull_max wither_skull_count ' + max_count);


__on_tick() -> (

    run('execute as @e[type=wither_skull] run scoreboard players add wither_skull_count wither_skull_count 1');
    run('execute if score wither_skull_count wither_skull_count >= wither_skull_max wither_skull_count run say 警告: 凋灵之首数量超过阈值');
    run('execute if score wither_skull_count wither_skull_count >= wither_skull_max wither_skull_count run say 已自动清理');
    run('execute if score wither_skull_count wither_skull_count >= wither_skull_max wither_skull_count run kill @e[type=wither_skull]');
    run('scoreboard players reset wither_skull_count wither_skull_count');
);

