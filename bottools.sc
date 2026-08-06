//  ██████╗  ██████╗ ████████╗████████╗ ██████╗  ██████╗ ██╗     ███████╗
//  ██╔══██╗██╔═══██╗╚══██╔══╝╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
//  ██████╔╝██║   ██║   ██║      ██║   ██║   ██║██║   ██║██║     ███████╗
//  ██╔══██╗██║   ██║   ██║      ██║   ██║   ██║██║   ██║██║     ╚════██║
//  ██████╔╝╚██████╔╝   ██║      ██║   ╚██████╔╝╚██████╔╝███████╗███████║
//  ╚═════╝  ╚═════╝    ╚═╝      ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
//  v1.0.0
//
// - By TomatoOfficial with ❤.
//
// - A script dedicated to the MAE server.
// - Yes, we hate Carpet /player command.

__config() -> {
    'commands' -> {
        '' -> 'view_databank'
    },
    'command_permission' -> 4
};

global_pending = [];
global_processed = [];
global_datafile = 'databank';

__on_start() -> (
    load_databank();
    team_add('Bot');
    team_property('Bot','color','gray');
    team_property('Bot','prefix',format('g BOT | '));
);

print_hint(commander, text) -> (
    hint = '[提示]';
    command = 'tellraw @s [{"text":"'+ hint + '",color:yellow},{"text":" ' + text + ', ",color:gray}]';
    run(command);
);

load_databank() -> (
    data = read_file(global_datafile, 'json');
    if(data != null && type(data) == 'list',
        global_processed = data,
    // else
        global_processed = []
    );
);

sava_databank() -> (
    write_file(global_datafile, 'json', global_processed);
);

__on_player_connects(player) -> (
    welcome_real_player(player);
);

welcome_real_player(player) -> (
    world_name = system_info('world_name');
    command = 'tellraw @a [{"text":"欢迎加入' + world_name + ', "},{"selector":"' + player + '"},{"text":"!"}]';
    run(command);
    // 欢迎加入 {world_name}, {player_name}!
);

__on_player_command(player, command) -> (
    parts = split(' ', command);
    if(length(parts) >= 3 && parts:0 == 'player' && parts:2 == 'spawn',
        fake_name = str(parts:1);
        if(fake_name != '',
            add_pending(fake_name, player),
        // else
            return()
        )
    );
);

pending_detection(list, name) ->  (
    length(filter(list, lower(_) == lower(name))) > 0;
);

add_pending(name, commander) -> (
    if(pending_detection(global_pending, name),
        print_hint(commander, str('假人 %s 已在等待队列中', name));
        return()
    );
    if(pending_detection(global_processed, name),
        print_hint(commander, str('假人 %s 已处理过(实际名可能不是这个反正你知道就行)', name));
        return()
    );
    global_pending += name;
    // print_hint(commander, str('已添加 %s 至等待队列', name));
);

__on_tick() -> (
    if(length(global_pending) > 0,
        check_pending()
    );
);

check_pending() -> (
    i = 0;
    while(i < length(global_pending),
        fake_name = global_pending:i;
        real_player = player(fake_name);
        
        if(real_player != null,
            real_name = real_player ~ 'name';
            
            team_fake_player(real_name);

            global_processed += real_name;
            
            delete(global_pending, i);
            sava_databank(),
        // else
            i += 1
        )
    );
);

team_fake_player(name) -> (
    run(str('say 假人 %s 已加入!', name));
    team_add('Bot', name)
);

view_databank() -> (
    player = player();
    if(length(global_processed) == 0,
        print_hint(player, '当前无已处理假人'),
    // else if
        print_hint(player, '此脚本已处理以下假人:');
        for(global_processed,
            print_hint(player, str('  - %s', _))
        )
    );
);