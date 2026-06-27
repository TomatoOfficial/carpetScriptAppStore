// Show Me What You Got - 稳定版（仅显示物品ID和数量）
__on_player_message(player, message) -> (
    if(message ~ '[i]',

        message = replace(message, '\\"', '\\\\"');
        message = replace(message, '\\\\', '\\\\\\\\');

        item_data = query(player(), 'holds', 'mainhand');
        if(!item_data, return());
        //print(item_data);

        [id, count, nbt] = item_data;
        
        name_str = str(item_display_name(id));
        // in translated name
        //print(item_json_str);
        //print(name_str);
        
        parts = split('\\[i\\]', message);
        if(!parts, parts=['']);

        json_text = [str('\"<%s> \"', player())];
        json_text += str('\"%s\"', _);

        components_map = nbt:'components';
        if(components_map != null,
            components_json_string = encode_json(components_map);   // 转为 JSON 字符串
            //print(str(components_map));
            //print(components_json_string);  // {"minecraft:enchantments":{"minecraft:protection":1}}
        );

        chat_text = '/tellraw @a [{"text":"<"},{"selector": ' + player + '},{"text":">"},{"text":" [",color:gray},{"text":"'+name_str+'",color:"aqua",hover_event:{action:"show_item","id": "'+id+'",components:'+components_map+'}},{"text":"]",color:gray}]';

        //print(chat_text);
        run(chat_text);

        // /tellraw @a {text:"name",color:"aqua",hover_event:{action:"show_text",value:[{text:"item_desc",color:"aqua"}]}}

        return('cancel');
    )
);
