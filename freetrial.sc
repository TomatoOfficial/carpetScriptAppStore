__config() -> {
   'scope' -> 'global',
   'commands' -> {
        'prepare' -> 'prepare',
        'begin' -> 'begin',
        'set info' -> 'info',
        'set global_location <x> <Y> <z> <pitch> <yaw>' -> 'set_global_location',
        'set players_count <count>' -> 'set_players_count'
	},
    'arguments' -> {
        'x' -> { 'type' -> 'float' },
        'y' -> { 'type' -> 'float' },
        'z' -> { 'type' -> 'float' },
        'pitch' -> { 'type' -> 'float', 'min' -> -90, 'max' -> 90 },
        'yaw' -> { 'type' -> 'float', 'min' -> -180, 'max' -> 180 },
        'count' -> { 'type' -> 'int', 'min' -> 1, 'max' -> 129}
    },
    'command_permission' -> 4
};

say(msg) -> run('say '+msg);

scoreboard_init(objective, criterion, display_name) -> (
    
	if(scoreboard(objective) == null,
        scoreboard_add(objective, criterion);
    );
	scoreboard_property(objective, 'display_name', display_name);
);

scoreboard_incr(objective, entity, value) -> (
	scoreboard(objective, entity, scoreboard(objective, entity) + value);
);

global_location = [0.0, 0.0, 0.0, 0.0, 0.0];
global_players = 129;

prepare() -> (
    if(player('1') && scoreboard('trial.time', 'is_prepared') == 0,
        //say('Player 1 已存在于世界中\n请在确保 1 ~ 128 假人都不存在于世界中后输入此指令');
        print(player('all'), format('by [FreeTrial] ', 'g Player 1 已存在于世界中\n请在确保 1 ~ 128 假人都不存在于世界中后输入此指令'));
        return(0);
    );

    // Spawn Player 1
    pos = global_location:0 + ' ' + global_location:1 + ' '+ global_location:2;
    facing = global_location:3+' '+global_location:4;

    scoreboard('trial.time', 'is_command', 1);


    if(scoreboard('trial.time', 'is_command') == 1 && !player('1'),
        (
            run('player 1 spawn at '+pos+' facing '+facing);
            // say('spawned player 1');
        ),
        (
            //say('重新准备中..');
            print(player('all'), format('by [FreeTrial] ', 'g 重新准备中...'));
            scoreboard('trial.time', 't', -5);
        );
    );
);

begin() -> (
    if(!scoreboard('trial.time', 'is_prepared') == 0,
        scoreboard('trial.time', 'is_begin', 1);
        scoreboard('trial.time', 't', 95),
        //else
        //say('你需要先准备此进程再开始!!');
        print(player('all'), format('by [FreeTrial] ', 'g 你需要先准备此进程再开始!!'));
    );
);

info() -> (
    pos = global_location:0 + ' / ' + global_location:1 + ' / '+ global_location:2;
    facing = global_location:3+' / '+global_location:4;

    msg = 'Current XYZ: ' + pos + '  ||  Current Facing: ' + facing + '  ||  Max Player: ' + global_players;

    display_title(player(), 'actionbar', msg);
);

set_global_location(x, y, z, pitch, yaw) -> (
    temp = [x, y, z, pitch, yaw];

    msg = format('by [FreeTrial] ', 'w 玩家 <', 'c '+player(),'w >', 'w  修改了假人生成位置');

    print(player('all'), msg);
    msg = format('by [FreeTrial] ', 'g '+global_location, '&'+global_location, '^w 点击以复制','w  -> ','g '+temp, '&'+temp, '^w 点击以复制');
    print(player('all'), msg);

    global_location:0 = x;
    global_location:1 = y;
    global_location:2 = z;
    global_location:3 = pitch;
    global_location:4 = yaw;
);

set_players_count(count) -> (
    msg = format('by [FreeTrial] ', 'w 玩家 <', 'c '+player(),'w > ', 'w 已设置玩家数量为 ','y '+count, 'w , 并重置循环');
    print(player('all'), msg);
    global_players = count;
    // reset + kill players
    for(range(1, global_players + 1),
        run('player ' + _ + ' kill')
    );
    // reset
    scoreboard('trial.time', 'cycle_now', 1);
    scoreboard('trial.time', 'cycle_total', 0);
    
);

prepare_begin() -> (
    tick = scoreboard('trial.time', 't') - 80;

    if(tick % 20 == 0 && tick <= 80,
        print(player('all'), format('by [FreeTrial] ', 'g 将于 ','w '+(5-(tick/20)),'g  秒后开始进程...'));
    );

    if(tick == 100,
        scoreboard('trial.time', 'is_cycle', 1);
        scoreboard('trial.time', 'cycle_now', 1);
    );
);

cycle() -> (
    cycle_now = scoreboard('trial.time', 'cycle_now');
    if(cycle_now == null, cycle_now = 1);
    cycle_total = scoreboard('trial.time', 'cycle_total'); // 0
    if(cycle_total == null, cycle_total = 0);

    pos = global_location:0 + ' ' + global_location:1 + ' '+ global_location:2;
    facing = global_location:3+' '+global_location:4;

    tick = scoreboard('trial.time', 't') - 200;

    // 计算当前阶段开始的时间点（用 cycle_total 和 cycle_now 推算）
    // 每个阶段固定长度 110 tick（100 use + 10 respawn）
    // 第几阶段（全局顺序）：stage_index = (cycle_total * 3 + (cycle_now - 1))
    stage_index = cycle_total * global_players + (cycle_now - 1);
    stage_start = stage_index * 200;
    use_time = stage_start + 10;
    respawn_time = stage_start + 100;

    // 生成玩家（在当前阶段开始的那一 tick）
    if(tick == (stage_start-80),
        run('player ' + cycle_now + ' spawn at ' + pos + ' facing ' + facing);
        // say('| 开始循环 ' + (cycle_total+1) + ' (阶段 ' + cycle_now +')');
        print(player('all'), format('by [FreeTrial] ', 'g | 开始循环 ','w '+(cycle_total+1),'g  (阶段 ','w '+cycle_now,'g )'));
    );

    if(use_time == tick,
        slot = 0;
        slot += inventory_find(player(cycle_now), 'ominous_trial_key')+1;
        // say('ominous key slot:'+slot+', moved hotbar to '+slot);
        run('player '+ cycle_now + ' hotbar ' + slot);
        run('gamemode survival '+ cycle_now);

        run('player '+ cycle_now + ' use once');
        // say('player '+ cycle_now +' used key.');
    );

    if(respawn_time == tick,
        run('player '+ cycle_now + ' kill');
        // say('player '+ cycle_now +' killed.');
        // run('player 1 spawn at '+pos+' facing '+facing);
        
        // 切换到下一个玩家
        if(cycle_now == global_players,
            cycle_now = 1;
            cycle_total = cycle_total + 1;
            scoreboard('trial.time', 'cycle_total', cycle_total);
        ,
            cycle_now = cycle_now + 1;
        );
        scoreboard('trial.time', 'cycle_now', cycle_now);
        
    );
    


    //display_title(s, 'actionbar', msg);
);

__on_start() -> (
    scoreboard_init('trial.time', 'dummy', 'time');
    scoreboard('trial.time', 't', -20);
    scoreboard('trial.time', 'is_begin', 0);
    scoreboard('trial.time', 'is_prepared', 0);
    scoreboard('trial.time', 'is_command', 0);
    scoreboard('trial.time', 'is_cycle', 0);
    scoreboard('trial.time', 'cycle_now', 0);
    scoreboard('trial.time', 'cycle_total', 0);
);

__on_tick() -> (
    if(scoreboard('trial.time', 'is_begin') == 1 && scoreboard('trial.time', 'is_command') == 1,
        (
            scoreboard_incr('trial.time', 't', 1);
        ),
        (
            if(player('1') && scoreboard('trial.time', 'is_command') == 1,
                if(scoreboard('trial.time', 't') <= -1,
                    scoreboard_incr('trial.time', 't', 1);
                );
            );
        );
    );

    if(scoreboard('trial.time', 't') == -1,
        (
            scoreboard_incr('trial.time', 't', 1);
            slot = 0;
            slot += inventory_find(player('1'), 'ominous_trial_key')+1;
            // say('ominous key slot:'+slot+', moved hotbar to '+slot);
            run('player 1 hotbar ' + slot);

            if(query(player('1'), 'holds'):0 == 'ominous_trial_key',
                msg = format('by [FreeTrial] ', 'w 预准备已完成，输入','g /freetrial begin','w 以开始进程');
                print(player('all'), msg);
                scoreboard('trial.time', 'is_prepared', 1);,
                // else
                msg = format('by [FreeTrial] ', 'r 预准备失败，原因为: ','rb 假人物品栏已满或未捡起钥匙\n','w 请在清空背包后并在物品栏内放置一把不详钥匙后\n输入','g /freetrial prepare','w 以重新准备');
                print(player('all'), msg);
            );
            
        );
    );

    if(scoreboard('trial.time', 'is_begin') == 1 && scoreboard('trial.time', 'is_cycle') != 1,
        prepare_begin();
    );

    if(scoreboard('trial.time', 'is_cycle') == 1,
        cycle();
        
    )

);