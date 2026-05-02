__config() -> {
   'commands' -> {
		'subscribe' -> 'subscribe_action',
        'info' -> 'info_action'
	},
    'command_permission' -> 1
};

subscribe_action() -> (
    if(query(player(), 'has_scoreboard_tag','sys.actionbar'),
        (
            modify(player(), 'clear_tag', 'sys.actionbar');
            print(player(), '[Server] 你已取消订阅服务器信息更新');
        ),
        (
            modify(player(), 'tag', 'sys.actionbar');
            print(player(), '[Server] 你已订阅服务器信息更新');
        );
    );
);

info_action() -> (
    name = (format('g | ','w 世界: ', 'l ' + s('world_name'), '&' + s('world_name'), '^w 点击以复制'));
    seed = (format('g | ','w 种子: [', 'l ' + s('world_seed'), '&' + s('world_seed'), '^w 点击以复制', 'w ]'));
    jvm  = (format('g | ','w JVM 版本: ', 'y ' + s('java_version') + ' x' + s('java_bits')));
    core = (format('g | ','w 可用 CPU 数量: ', 'y ' + s('java_cpu_count')));
    ltt = s('server_last_tick_times');
    tick = (format('g | ','w TPS: ', 'y ' + ltt:0, 'w , ', 'y ' + ltt:1, 'w , ', 'y ' + ltt:2));
    
    print(player(), name);
    print(player(), seed);
    print(player(), jvm+'   '+core);
    print(player(), tick);
);

s(id) -> system_info(id);

actionbar(s) -> (
    cpu  = (format('w CPU 占用：', 'c ' + round(s('java_process_cpu_load')*10000)/100.00 + '%', 'w /', 'c ' + round(s('java_system_cpu_load')*10000)/100.00 + '%'));
    mem  = (format('w JVM 内存分配：', 'c ' + round(s('java_used_memory')/1048576), 'w /', 'c ' + round(s('java_allocated_memory')/1048576), 'w /', 'c ' + round(s('java_max_memory')/1048576)));
    msg = cpu + '  |  ' + mem;
    display_title(s, 'actionbar', msg);
);

__on_tick() -> (
    for(player('all'),
        if(query(_, 'has_scoreboard_tag','sys.actionbar'),
            actionbar(_);
        );
    );
);