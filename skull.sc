// 配置项 凋零之首清除阈值 (默认值 100)
global_max_count = 100;
global_warning_message1 = '警告: 凋灵之首数量超过阈值 (' + global_max_count + ')';
global_warning_message2 = '已自动清理';
global_manual_message1 = '手动清理完成';
global_manual_message2 = '本次一共清理了: ';

__config() -> {
   'scope' -> 'global',
   'commands' -> {
		'' -> 'wither_skull_manual_kill'
	},
    'command_permission' -> 1
};

// 初始化信息输出
__on_start() -> (
    unix_time = convert_date(unix_time()); // [YYYY, MM, DD, HH, MM, SS, ...]
    date = str(
        '%d/%d/%d',
        unix_time:0, unix_time:1, unix_time:2
    );
    time = str(
        '%02d:%02d:%02d',
        unix_time:3, unix_time:4, unix_time:5
    );

    print('[' + time + '] [INFO] ' + 'App \'' + system_info('app_name') + '.sc\' initialized');
    logger('info', 'App \'' + system_info('app_name') + '.sc\' initialized');
);  // [HH:MM:SS] [INFO] App XXXXX.sc initialized

// 计分板函数
scoreboard_init(objective, criterion, display_name) -> (
	if(scoreboard(objective) == null,
        scoreboard_add(objective, criterion);
    );
	scoreboard_property(objective, 'display_name', display_name);
);

wither_skull_overkill(now_count, global_max_count) -> (
    if(now_count >= global_max_count,
        (
            run('say '+global_warning_message1);
            run('say '+global_warning_message2);
            run('kill @e[type=wither_skull]');
            //format('w 世界名称：', 'l ' + s('world_name'), 'w    种子：[', 'l ' + s('world_seed'), '&' + s('world_seed'), '^w 点击以复制', 'w ]'));
        );
        
    );
);

wither_skull_manual_kill() -> (
    run('execute as @e[type=wither_skull] run scoreboard players add wither_skull_manual wither_skull_count 1');
    manual_heads = scoreboard('wither_skull_count', 'wither_skull_manual');
    if(manual_heads == null,
        manual_heads == 0
    );
    run('say '+global_manual_message1);
    run('say '+global_manual_message2+manual_heads+' 个凋零之首');
    run('kill @e[type=wither_skull]');
    scoreboard('wither_skull_count', 'wither_skull_manual', 0);
);

// 初始化计分表
scoreboard_init('wither_skull_count', 'dummy', 'wither_skull_count');
scoreboard('wither_skull_count', 'wither_skull_max', max_count);

__on_tick() -> (

    run('execute as @e[type=wither_skull] run scoreboard players add wither_skull_count wither_skull_count 1');
    now_count = scoreboard('wither_skull_count', 'wither_skull_count');
    
    wither_skull_overkill(now_count, global_max_count);

    // 重置计分板
    scoreboard('wither_skull_count', 'wither_skull_count', 0);
);