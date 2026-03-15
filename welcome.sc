__config() -> {
   'scope' -> 'player',
   'commands' -> {
		'' -> 'welcome_scoreboard'
	},
    'command_permission' -> 1
};

// 初始化
__on_start() -> (
    scoreboard_init('welcome.tick', 'dummy', 'welcome.tick');
); 

__on_player_connects(player) -> (
    connecthaha(player);
);

// 计分板初始化函数
scoreboard_init(objective, criterion, display_name) -> (
	if(scoreboard(objective) == null,
        scoreboard_add(objective, criterion);
    );
	scoreboard_property(objective, 'display_name', display_name);
);

// score += value
scoreboard_incr(objective, entity, value) -> (
	scoreboard(objective, entity, scoreboard(objective, entity) + value);
);

connecthaha(player) -> (
    world_name = system_info('world_name');
    command = 'tellraw @a [{"text":"欢迎加入' + world_name + ', "},{"selector":"' + player + '"},{"text":"!"}]';
    run(command);
    
); // 真人加入服务器

global_players = [];

// a = [1, 2, 3]; 
// put(a, null, [4, 5, 6], 'extend');
// a  => [1, 2, 3, 4, 5, 6]

__on_player_command(player, command) -> (

    split_command = split(' ', command);
    
    if(split_command:0 == 'player' && split_command:2 == 'spawn',
        (   // player {name} spawn
            
            // fake_player_name = player(split_command:1);
            // fake_player_name = entity_selector(str(split_command:1));

            // run('tp '+fake_player_name+' tomatoofficial');
            // //print(fake_player_name);

            // team_add('admin', str(split_command:1));
            // team_add('admin', 'bot_'+str(split_command:1));
            // logger('team join bot '+str(split_command:1));
            fake_name = str(split_command:1);
            print(fake_name);
            fake_player_welcome(fake_name);

        );
    );
);

fake_player_welcome(fake_name) -> (
    // 追加单个元素（不使用 extend）
    global_players += fake_name;
    // print(global_players);
    
    // 查找索引并删除（假设元素唯一）
    // index = global_players ~ fake_name;  // 查找元素位置，返回索引或 null
    // if (index != null, delete(global_players, index));
    // print(global_players);

    // welcome_scoreboard();
);

welcome_scoreboard() -> (

    // for(global_players,
    //     run('say '+_)
    // );

    if(global_players != [],

        for(global_players,
            fake_name = _;
            // print(fake_name);
            if(fake_name != [] && fake_name != '',
                (
                    real_name = player(fake_name);
                    print('Bot real name from player() : '+real_name);
                    if(real_name != null,
                        print('good morning, fake player '+str(real_name)+'!');
                        remove_fake_player(fake_name);
                        break();
                    );
                );
            );
            

            // scoreboard_incr('welcome.tick', _, 1);

            // tick = scoreboard('welcome.tick', _);

            // if(tick >= 20,
            //     scoreboard('welcome.tick', _, 0);
            //     welcome(_);
            // );
        );
    );
);

remove_fake_player(fake_name) -> (
    print('removed fake name: '+fake_name);
    global_players = global_players - fake_name;
);

welcome(fake_name) -> (
    // print(player);
    real_name = entity_selector(fake_name);
    print(real_name);
);


__on_tick() -> (
    if(global_players != [] && global_players != '',
        welcome_scoreboard();
    )
)