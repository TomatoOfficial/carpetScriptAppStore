import json
import os
import time

# ==================== 配置区域 ====================
# 请根据实际情况修改以下路径
UUID_MAP_FILE = "player_uuids.json"          # 上一步生成的 UUID 映射文件
STATS_FOLDER = "./stats"                      # 服务器世界文件夹下的 stats 目录
OUTPUT_FUNCTION = "sync_output.mcfunction" # 输出的 mcfunction 文件名
BLOCK_LIST_FILE = "block_list.json"           # 包含要统计的方块 ID 列表的 JSON 文件（可选）
# =================================================

# 如果未提供方块列表文件，则使用默认列表（示例，请替换为你需要的实际方块）
DEFAULT_BLOCK_LIST = ['acacia_button', 'acacia_door', 'acacia_fence', 'acacia_fence_gate', 'acacia_hanging_sign', 'acacia_leaves', 'acacia_log', 'acacia_planks', 'acacia_pressure_plate', 'acacia_sapling', 'acacia_sign', 'acacia_slab', 'acacia_stairs', 'acacia_trapdoor', 'acacia_wall_hanging_sign', 'acacia_wall_sign', 'acacia_wood', 'activator_rail', 'allium', 'amethyst_block', 'amethyst_cluster', 'ancient_debris', 'andesite', 'andesite_slab', 'andesite_stairs', 'andesite_wall', 'anvil', 'attached_melon_stem', 'attached_pumpkin_stem', 'azalea', 'azalea_leaves', 'azure_bluet', 'bamboo', 'bamboo_block', 'bamboo_button', 'bamboo_door', 'bamboo_fence', 'bamboo_fence_gate', 'bamboo_hanging_sign', 'bamboo_mosaic', 'bamboo_mosaic_slab', 'bamboo_mosaic_stairs', 'bamboo_planks', 'bamboo_pressure_plate', 'bamboo_sapling', 'bamboo_sign', 'bamboo_slab', 'bamboo_stairs', 'bamboo_trapdoor', 'bamboo_wall_hanging_sign', 'bamboo_wall_sign', 'barrel', 'basalt', 'beacon', 'beehive', 'beetroots', 'bee_nest', 'bell', 'big_dripleaf', 'big_dripleaf_stem', 'birch_button', 'birch_door', 'birch_fence', 'birch_fence_gate', 'birch_hanging_sign', 'birch_leaves', 'birch_log', 'birch_planks', 'birch_pressure_plate', 'birch_sapling', 'birch_sign', 'birch_slab', 'birch_stairs', 'birch_trapdoor', 'birch_wall_hanging_sign', 'birch_wall_sign', 'birch_wood', 'blackstone', 'blackstone_slab', 'blackstone_stairs', 'blackstone_wall', 'black_banner', 'black_bed', 'black_candle', 'black_candle_cake', 'black_carpet', 'black_concrete', 'black_concrete_powder', 'black_glazed_terracotta', 'black_shulker_box', 'black_stained_glass', 'black_stained_glass_pane', 'black_terracotta', 'black_wall_banner', 'black_wool', 'blast_furnace', 'blue_banner', 'blue_bed', 'blue_candle', 'blue_candle_cake', 'blue_carpet', 'blue_concrete', 'blue_concrete_powder', 'blue_glazed_terracotta', 'blue_ice', 'blue_orchid', 'blue_shulker_box', 'blue_stained_glass', 'blue_stained_glass_pane', 'blue_terracotta', 'blue_wall_banner', 'blue_wool', 'bone_block', 'bookshelf', 'brain_coral', 'brain_coral_block', 'brain_coral_fan', 'brain_coral_wall_fan', 'brewing_stand', 'bricks', 'brick_slab', 'brick_stairs', 'brick_wall', 'brown_banner', 'brown_bed', 'brown_candle', 'brown_candle_cake', 'brown_carpet', 'brown_concrete', 'brown_concrete_powder', 'brown_glazed_terracotta', 'brown_mushroom', 'brown_mushroom_block', 'brown_shulker_box', 'brown_stained_glass', 'brown_stained_glass_pane', 'brown_terracotta', 'brown_wall_banner', 'brown_wool', 'bubble_column', 'bubble_coral', 'bubble_coral_block', 'bubble_coral_fan', 'bubble_coral_wall_fan', 'budding_amethyst', 'bush', 'cactus', 'cactus_flower', 'cake', 'calcite', 'calibrated_sculk_sensor', 'campfire', 'candle', 'candle_cake', 'carrots', 'cartography_table', 'carved_pumpkin', 'cauldron', 'cave_vines', 'cave_vines_plant', 'chain', 'cherry_button', 'cherry_door', 'cherry_fence', 'cherry_fence_gate', 'cherry_hanging_sign', 'cherry_leaves', 'cherry_log', 'cherry_planks', 'cherry_pressure_plate', 'cherry_sapling', 'cherry_sign', 'cherry_slab', 'cherry_stairs', 'cherry_trapdoor', 'cherry_wall_hanging_sign', 'cherry_wall_sign', 'cherry_wood', 'chest', 'chipped_anvil', 'chiseled_bookshelf', 'chiseled_copper', 'chiseled_deepslate', 'chiseled_nether_bricks', 'chiseled_polished_blackstone', 'chiseled_quartz_block', 'chiseled_red_sandstone', 'chiseled_resin_bricks', 'chiseled_sandstone', 'chiseled_stone_bricks', 'chiseled_tuff', 'chiseled_tuff_bricks', 'chorus_flower', 'chorus_plant', 'clay', 'closed_eyeblossom', 'coal_block', 'coal_ore', 'coarse_dirt', 'cobbled_deepslate', 'cobbled_deepslate_slab', 'cobbled_deepslate_stairs', 'cobbled_deepslate_wall', 'cobblestone', 'cobblestone_slab', 'cobblestone_stairs', 'cobblestone_wall', 'cobweb', 'cocoa', 'comparator', 'composter', 'conduit', 'copper_block', 'copper_bulb', 'copper_door', 'copper_grate', 'copper_ore', 'copper_trapdoor', 'cornflower', 'cracked_deepslate_bricks', 'cracked_deepslate_tiles', 'cracked_nether_bricks', 'cracked_polished_blackstone_bricks', 'cracked_stone_bricks', 'crafter', 'crafting_table', 'creaking_heart', 'creeper_head', 'creeper_wall_head', 'crimson_button', 'crimson_door', 'crimson_fence', 'crimson_fence_gate', 'crimson_fungus', 'crimson_hanging_sign', 'crimson_hyphae', 'crimson_nylium', 'crimson_planks', 'crimson_pressure_plate', 'crimson_roots', 'crimson_sign', 'crimson_slab', 'crimson_stairs', 'crimson_stem', 'crimson_trapdoor', 'crimson_wall_hanging_sign', 'crimson_wall_sign', 'crying_obsidian', 'cut_copper', 'cut_copper_slab', 'cut_copper_stairs', 'cut_red_sandstone', 'cut_red_sandstone_slab', 'cut_sandstone', 'cut_sandstone_slab', 'cyan_banner', 'cyan_bed', 'cyan_candle', 'cyan_candle_cake', 'cyan_carpet', 'cyan_concrete', 'cyan_concrete_powder', 'cyan_glazed_terracotta', 'cyan_shulker_box', 'cyan_stained_glass', 'cyan_stained_glass_pane', 'cyan_terracotta', 'cyan_wall_banner', 'cyan_wool', 'damaged_anvil', 'dandelion', 'dark_oak_button', 'dark_oak_door', 'dark_oak_fence', 'dark_oak_fence_gate', 'dark_oak_hanging_sign', 'dark_oak_leaves', 'dark_oak_log', 'dark_oak_planks', 'dark_oak_pressure_plate', 'dark_oak_sapling', 'dark_oak_sign', 'dark_oak_slab', 'dark_oak_stairs', 'dark_oak_trapdoor', 'dark_oak_wall_hanging_sign', 'dark_oak_wall_sign', 'dark_oak_wood', 'dark_prismarine', 'dark_prismarine_slab', 'dark_prismarine_stairs', 'daylight_detector', 'dead_brain_coral', 'dead_brain_coral_block', 'dead_brain_coral_fan', 'dead_brain_coral_wall_fan', 'dead_bubble_coral', 'dead_bubble_coral_block', 'dead_bubble_coral_fan', 'dead_bubble_coral_wall_fan', 'dead_bush', 'dead_fire_coral', 'dead_fire_coral_block', 'dead_fire_coral_fan', 'dead_fire_coral_wall_fan', 'dead_horn_coral', 'dead_horn_coral_block', 'dead_horn_coral_fan', 'dead_horn_coral_wall_fan', 'dead_tube_coral', 'dead_tube_coral_block', 'dead_tube_coral_fan', 'dead_tube_coral_wall_fan', 'decorated_pot', 'deepslate', 'deepslate_bricks', 'deepslate_brick_slab', 'deepslate_brick_stairs', 'deepslate_brick_wall', 'deepslate_coal_ore', 'deepslate_copper_ore', 'deepslate_diamond_ore', 'deepslate_emerald_ore', 'deepslate_gold_ore', 'deepslate_iron_ore', 'deepslate_lapis_ore', 'deepslate_redstone_ore', 'deepslate_tiles', 'deepslate_tile_slab', 'deepslate_tile_stairs', 'deepslate_tile_wall', 'detector_rail', 'diamond_block', 'diamond_ore', 'diorite', 'diorite_slab', 'diorite_stairs', 'diorite_wall', 'dirt', 'dirt_path', 'dispenser', 'dragon_head', 'dragon_wall_head', 'dried_ghast', 'dried_kelp_block', 'dripstone_block', 'dropper', 'emerald_block', 'emerald_ore', 'enchanting_table', 'ender_chest', 'end_rod', 'end_stone', 'end_stone_bricks', 'end_stone_brick_slab', 'end_stone_brick_stairs', 'end_stone_brick_wall', 'exposed_chiseled_copper', 'exposed_copper', 'exposed_copper_bulb', 'exposed_copper_door', 'exposed_copper_grate', 'exposed_copper_trapdoor', 'exposed_cut_copper', 'exposed_cut_copper_slab', 'exposed_cut_copper_stairs', 'farmland', 'fern', 'firefly_bush', 'fire_coral', 'fire_coral_block', 'fire_coral_fan', 'fire_coral_wall_fan', 'fletching_table', 'flowering_azalea', 'flowering_azalea_leaves', 'flower_pot', 'frogspawn', 'frosted_ice', 'furnace', 'gilded_blackstone', 'glass', 'glass_pane', 'glowstone', 'glow_lichen', 'gold_block', 'gold_ore', 'granite', 'granite_slab', 'granite_stairs', 'granite_wall', 'grass_block', 'gravel', 'gray_banner', 'gray_bed', 'gray_candle', 'gray_candle_cake', 'gray_carpet', 'gray_concrete', 'gray_concrete_powder', 'gray_glazed_terracotta', 'gray_shulker_box', 'gray_stained_glass', 'gray_stained_glass_pane', 'gray_terracotta', 'gray_wall_banner', 'gray_wool', 'green_banner', 'green_bed', 'green_candle', 'green_candle_cake', 'green_carpet', 'green_concrete', 'green_concrete_powder', 'green_glazed_terracotta', 'green_shulker_box', 'green_stained_glass', 'green_stained_glass_pane', 'green_terracotta', 'green_wall_banner', 'green_wool', 'grindstone', 'hanging_roots', 'hay_block', 'heavy_core', 'heavy_weighted_pressure_plate', 'honeycomb_block', 'honey_block', 'hopper', 'horn_coral', 'horn_coral_block', 'horn_coral_fan', 'horn_coral_wall_fan', 'ice', 'infested_chiseled_stone_bricks', 'infested_cobblestone', 'infested_cracked_stone_bricks', 'infested_deepslate', 'infested_mossy_stone_bricks', 'infested_stone', 'infested_stone_bricks', 'iron_bars', 'iron_block', 'iron_door', 'iron_ore', 'iron_trapdoor', 'jack_o_lantern', 'jukebox', 'jungle_button', 'jungle_door', 'jungle_fence', 'jungle_fence_gate', 'jungle_hanging_sign', 'jungle_leaves', 'jungle_log', 'jungle_planks', 'jungle_pressure_plate', 'jungle_sapling', 'jungle_sign', 'jungle_slab', 'jungle_stairs', 'jungle_trapdoor', 'jungle_wall_hanging_sign', 'jungle_wall_sign', 'jungle_wood', 'kelp', 'kelp_plant', 'ladder', 'lantern', 'lapis_block', 'lapis_ore', 'large_amethyst_bud', 'large_fern', 'lava', 'lava_cauldron', 'leaf_litter', 'lectern', 'lever', 'lightning_rod', 'light_blue_banner', 'light_blue_bed', 'light_blue_candle', 'light_blue_candle_cake', 'light_blue_carpet', 'light_blue_concrete', 'light_blue_concrete_powder', 'light_blue_glazed_terracotta', 'light_blue_shulker_box', 'light_blue_stained_glass', 'light_blue_stained_glass_pane', 'light_blue_terracotta', 'light_blue_wall_banner', 'light_blue_wool', 'light_gray_banner', 'light_gray_bed', 'light_gray_candle', 'light_gray_candle_cake', 'light_gray_carpet', 'light_gray_concrete', 'light_gray_concrete_powder', 'light_gray_glazed_terracotta', 'light_gray_shulker_box', 'light_gray_stained_glass', 'light_gray_stained_glass_pane', 'light_gray_terracotta', 'light_gray_wall_banner', 'light_gray_wool', 'light_weighted_pressure_plate', 'lilac', 'lily_of_the_valley', 'lily_pad', 'lime_banner', 'lime_bed', 'lime_candle', 'lime_candle_cake', 'lime_carpet', 'lime_concrete', 'lime_concrete_powder', 'lime_glazed_terracotta', 'lime_shulker_box', 'lime_stained_glass', 'lime_stained_glass_pane', 'lime_terracotta', 'lime_wall_banner', 'lime_wool', 'lodestone', 'loom', 'magenta_banner', 'magenta_bed', 'magenta_candle', 'magenta_candle_cake', 'magenta_carpet', 'magenta_concrete', 'magenta_concrete_powder', 'magenta_glazed_terracotta', 'magenta_shulker_box', 'magenta_stained_glass', 'magenta_stained_glass_pane', 'magenta_terracotta', 'magenta_wall_banner', 'magenta_wool', 'magma_block', 'mangrove_button', 'mangrove_door', 'mangrove_fence', 'mangrove_fence_gate', 'mangrove_hanging_sign', 'mangrove_leaves', 'mangrove_log', 'mangrove_planks', 'mangrove_pressure_plate', 'mangrove_propagule', 'mangrove_roots', 'mangrove_sign', 'mangrove_slab', 'mangrove_stairs', 'mangrove_trapdoor', 'mangrove_wall_hanging_sign', 'mangrove_wall_sign', 'mangrove_wood', 'medium_amethyst_bud', 'melon', 'melon_stem', 'mossy_cobblestone', 'mossy_cobblestone_slab', 'mossy_cobblestone_stairs', 'mossy_cobblestone_wall', 'mossy_stone_bricks', 'mossy_stone_brick_slab', 'mossy_stone_brick_stairs', 'mossy_stone_brick_wall', 'moss_block', 'moss_carpet', 'moving_piston', 'mud', 'muddy_mangrove_roots', 'mud_bricks', 'mud_brick_slab', 'mud_brick_stairs', 'mud_brick_wall', 'mushroom_stem', 'mycelium', 'netherite_block', 'netherrack', 'nether_bricks', 'nether_brick_fence', 'nether_brick_slab', 'nether_brick_stairs', 'nether_brick_wall', 'nether_gold_ore', 'nether_portal', 'nether_quartz_ore', 'nether_sprouts', 'nether_wart', 'nether_wart_block', 'note_block', 'oak_button', 'oak_door', 'oak_fence', 'oak_fence_gate', 'oak_hanging_sign', 'oak_leaves', 'oak_log', 'oak_planks', 'oak_pressure_plate', 'oak_sapling', 'oak_sign', 'oak_slab', 'oak_stairs', 'oak_trapdoor', 'oak_wall_hanging_sign', 'oak_wall_sign', 'oak_wood', 'observer', 'obsidian', 'ochre_froglight', 'open_eyeblossom', 'orange_banner', 'orange_bed', 'orange_candle', 'orange_candle_cake', 'orange_carpet', 'orange_concrete', 'orange_concrete_powder', 'orange_glazed_terracotta', 'orange_shulker_box', 'orange_stained_glass', 'orange_stained_glass_pane', 'orange_terracotta', 'orange_tulip', 'orange_wall_banner', 'orange_wool', 'oxeye_daisy', 'oxidized_chiseled_copper', 'oxidized_copper', 'oxidized_copper_bulb', 'oxidized_copper_door', 'oxidized_copper_grate', 'oxidized_copper_trapdoor', 'oxidized_cut_copper', 'oxidized_cut_copper_slab', 'oxidized_cut_copper_stairs', 'packed_ice', 'packed_mud', 'pale_hanging_moss', 'pale_moss_block', 'pale_moss_carpet', 'pale_oak_button', 'pale_oak_door', 'pale_oak_fence', 'pale_oak_fence_gate', 'pale_oak_hanging_sign', 'pale_oak_leaves', 'pale_oak_log', 'pale_oak_planks', 'pale_oak_pressure_plate', 'pale_oak_sapling', 'pale_oak_sign', 'pale_oak_slab', 'pale_oak_stairs', 'pale_oak_trapdoor', 'pale_oak_wall_hanging_sign', 'pale_oak_wall_sign', 'pale_oak_wood', 'pearlescent_froglight', 'peony', 'petrified_oak_slab', 'piglin_head', 'piglin_wall_head', 'pink_banner', 'pink_bed', 'pink_candle', 'pink_candle_cake', 'pink_carpet', 'pink_concrete', 'pink_concrete_powder', 'pink_glazed_terracotta', 'pink_petals', 'pink_shulker_box', 'pink_stained_glass', 'pink_stained_glass_pane', 'pink_terracotta', 'pink_tulip', 'pink_wall_banner', 'pink_wool', 'piston', 'piston_head', 'pitcher_crop', 'pitcher_plant', 'player_head', 'player_wall_head', 'podzol', 'pointed_dripstone', 'polished_andesite', 'polished_andesite_slab', 'polished_andesite_stairs', 'polished_basalt', 'polished_blackstone', 'polished_blackstone_bricks', 'polished_blackstone_brick_slab', 'polished_blackstone_brick_stairs', 'polished_blackstone_brick_wall', 'polished_blackstone_button', 'polished_blackstone_pressure_plate', 'polished_blackstone_slab', 'polished_blackstone_stairs', 'polished_blackstone_wall', 'polished_deepslate', 'polished_deepslate_slab', 'polished_deepslate_stairs', 'polished_deepslate_wall', 'polished_diorite', 'polished_diorite_slab', 'polished_diorite_stairs', 'polished_granite', 'polished_granite_slab', 'polished_granite_stairs', 'polished_tuff', 'polished_tuff_slab', 'polished_tuff_stairs', 'polished_tuff_wall', 'poppy', 'potatoes', 'potted_acacia_sapling', 'potted_allium', 'potted_azalea_bush', 'potted_azure_bluet', 'potted_bamboo', 'potted_birch_sapling', 'potted_blue_orchid', 'potted_brown_mushroom', 'potted_cactus', 'potted_cherry_sapling', 'potted_closed_eyeblossom', 'potted_cornflower', 'potted_crimson_fungus', 'potted_crimson_roots', 'potted_dandelion', 'potted_dark_oak_sapling', 'potted_dead_bush', 'potted_fern', 'potted_flowering_azalea_bush', 'potted_jungle_sapling', 'potted_lily_of_the_valley', 'potted_mangrove_propagule', 'potted_oak_sapling', 'potted_open_eyeblossom', 'potted_orange_tulip', 'potted_oxeye_daisy', 'potted_pale_oak_sapling', 'potted_pink_tulip', 'potted_poppy', 'potted_red_mushroom', 'potted_red_tulip', 'potted_spruce_sapling', 'potted_torchflower', 'potted_warped_fungus', 'potted_warped_roots', 'potted_white_tulip', 'potted_wither_rose', 'powder_snow', 'powder_snow_cauldron', 'powered_rail', 'prismarine', 'prismarine_bricks', 'prismarine_brick_slab', 'prismarine_brick_stairs', 'prismarine_slab', 'prismarine_stairs', 'prismarine_wall', 'pumpkin', 'pumpkin_stem', 'purple_banner', 'purple_bed', 'purple_candle', 'purple_candle_cake', 'purple_carpet', 'purple_concrete', 'purple_concrete_powder', 'purple_glazed_terracotta', 'purple_shulker_box', 'purple_stained_glass', 'purple_stained_glass_pane', 'purple_terracotta', 'purple_wall_banner', 'purple_wool', 'purpur_block', 'purpur_pillar', 'purpur_slab', 'purpur_stairs', 'quartz_block', 'quartz_bricks', 'quartz_pillar', 'quartz_slab', 'quartz_stairs', 'rail', 'raw_copper_block', 'raw_gold_block', 'raw_iron_block', 'redstone_block', 'redstone_lamp', 'redstone_ore', 'redstone_torch', 'redstone_wall_torch', 'redstone_wire', 'red_banner', 'red_bed', 'red_candle', 'red_candle_cake', 'red_carpet', 'red_concrete', 'red_concrete_powder', 'red_glazed_terracotta', 'red_mushroom', 'red_mushroom_block', 'red_nether_bricks', 'red_nether_brick_slab', 'red_nether_brick_stairs', 'red_nether_brick_wall', 'red_sand', 'red_sandstone', 'red_sandstone_slab', 'red_sandstone_stairs', 'red_sandstone_wall', 'red_shulker_box', 'red_stained_glass', 'red_stained_glass_pane', 'red_terracotta', 'red_tulip', 'red_wall_banner', 'red_wool', 'reinforced_deepslate', 'repeater', 'resin_block', 'resin_bricks', 'resin_brick_slab', 'resin_brick_stairs', 'resin_brick_wall', 'resin_clump', 'respawn_anchor', 'rooted_dirt', 'rose_bush', 'sand', 'sandstone', 'sandstone_slab', 'sandstone_stairs', 'sandstone_wall', 'scaffolding', 'sculk', 'sculk_catalyst', 'sculk_sensor', 'sculk_shrieker', 'sculk_vein', 'seagrass', 'sea_lantern', 'sea_pickle', 'short_dry_grass', 'short_grass', 'shroomlight', 'shulker_box', 'skeleton_skull', 'skeleton_wall_skull', 'slime_block', 'small_amethyst_bud', 'small_dripleaf', 'smithing_table', 'smoker', 'smooth_basalt', 'smooth_quartz', 'smooth_quartz_slab', 'smooth_quartz_stairs', 'smooth_red_sandstone', 'smooth_red_sandstone_slab', 'smooth_red_sandstone_stairs', 'smooth_sandstone', 'smooth_sandstone_slab', 'smooth_sandstone_stairs', 'smooth_stone', 'smooth_stone_slab', 'sniffer_egg', 'snow', 'snow_block', 'soul_campfire', 'soul_lantern', 'soul_sand', 'soul_soil', 'soul_torch', 'soul_wall_torch', 'spawner', 'sponge', 'spore_blossom', 'spruce_button', 'spruce_door', 'spruce_fence', 'spruce_fence_gate', 'spruce_hanging_sign', 'spruce_leaves', 'spruce_log', 'spruce_planks', 'spruce_pressure_plate', 'spruce_sapling', 'spruce_sign', 'spruce_slab', 'spruce_stairs', 'spruce_trapdoor', 'spruce_wall_hanging_sign', 'spruce_wall_sign', 'spruce_wood', 'sticky_piston', 'stone', 'stonecutter', 'stone_bricks', 'stone_brick_slab', 'stone_brick_stairs', 'stone_brick_wall', 'stone_button', 'stone_pressure_plate', 'stone_slab', 'stone_stairs', 'stripped_acacia_log', 'stripped_acacia_wood', 'stripped_bamboo_block', 'stripped_birch_log', 'stripped_birch_wood', 'stripped_cherry_log', 'stripped_cherry_wood', 'stripped_crimson_hyphae', 'stripped_crimson_stem', 'stripped_dark_oak_log', 'stripped_dark_oak_wood', 'stripped_jungle_log', 'stripped_jungle_wood', 'stripped_mangrove_log', 'stripped_mangrove_wood', 'stripped_oak_log', 'stripped_oak_wood', 'stripped_pale_oak_log', 'stripped_pale_oak_wood', 'stripped_spruce_log', 'stripped_spruce_wood', 'stripped_warped_hyphae', 'stripped_warped_stem', 'sugar_cane', 'sunflower', 'suspicious_gravel', 'suspicious_sand', 'sweet_berry_bush', 'tall_dry_grass', 'tall_grass', 'tall_seagrass', 'target', 'terracotta', 'tinted_glass', 'tnt', 'torch', 'torchflower', 'torchflower_crop', 'trapped_chest', 'trial_spawner', 'tripwire', 'tripwire_hook', 'tube_coral', 'tube_coral_block', 'tube_coral_fan', 'tube_coral_wall_fan', 'tuff', 'tuff_bricks', 'tuff_brick_slab', 'tuff_brick_stairs', 'tuff_brick_wall', 'tuff_slab', 'tuff_stairs', 'tuff_wall', 'turtle_egg', 'twisting_vines', 'twisting_vines_plant', 'vault', 'verdant_froglight', 'vine', 'wall_torch', 'warped_button', 'warped_door', 'warped_fence', 'warped_fence_gate', 'warped_fungus', 'warped_hanging_sign', 'warped_hyphae', 'warped_nylium', 'warped_planks', 'warped_pressure_plate', 'warped_roots', 'warped_sign', 'warped_slab', 'warped_stairs', 'warped_stem', 'warped_trapdoor', 'warped_wall_hanging_sign', 'warped_wall_sign', 'warped_wart_block', 'water', 'water_cauldron', 'waxed_chiseled_copper', 'waxed_copper_block', 'waxed_copper_bulb', 'waxed_copper_door', 'waxed_copper_grate', 'waxed_copper_trapdoor', 'waxed_cut_copper', 'waxed_cut_copper_slab', 'waxed_cut_copper_stairs', 'waxed_exposed_chiseled_copper', 'waxed_exposed_copper', 'waxed_exposed_copper_bulb', 'waxed_exposed_copper_door', 'waxed_exposed_copper_grate', 'waxed_exposed_copper_trapdoor', 'waxed_exposed_cut_copper', 'waxed_exposed_cut_copper_slab', 'waxed_exposed_cut_copper_stairs', 'waxed_oxidized_chiseled_copper', 'waxed_oxidized_copper', 'waxed_oxidized_copper_bulb', 'waxed_oxidized_copper_door', 'waxed_oxidized_copper_grate', 'waxed_oxidized_copper_trapdoor', 'waxed_oxidized_cut_copper', 'waxed_oxidized_cut_copper_slab', 'waxed_oxidized_cut_copper_stairs', 'waxed_weathered_chiseled_copper', 'waxed_weathered_copper', 'waxed_weathered_copper_bulb', 'waxed_weathered_copper_door', 'waxed_weathered_copper_grate', 'waxed_weathered_copper_trapdoor', 'waxed_weathered_cut_copper', 'waxed_weathered_cut_copper_slab', 'waxed_weathered_cut_copper_stairs', 'weathered_chiseled_copper', 'weathered_copper', 'weathered_copper_bulb', 'weathered_copper_door', 'weathered_copper_grate', 'weathered_copper_trapdoor', 'weathered_cut_copper', 'weathered_cut_copper_slab', 'weathered_cut_copper_stairs', 'weeping_vines', 'weeping_vines_plant', 'wet_sponge', 'wheat', 'white_banner', 'white_bed', 'white_candle', 'white_candle_cake', 'white_carpet', 'white_concrete', 'white_concrete_powder', 'white_glazed_terracotta', 'white_shulker_box', 'white_stained_glass', 'white_stained_glass_pane', 'white_terracotta', 'white_tulip', 'white_wall_banner', 'white_wool', 'wildflowers', 'wither_rose', 'wither_skeleton_skull', 'wither_skeleton_wall_skull', 'yellow_banner', 'yellow_bed', 'yellow_candle', 'yellow_candle_cake', 'yellow_carpet', 'yellow_concrete', 'yellow_concrete_powder', 'yellow_glazed_terracotta', 'yellow_shulker_box', 'yellow_stained_glass', 'yellow_stained_glass_pane', 'yellow_terracotta', 'yellow_wall_banner', 'yellow_wool', 'zombie_head', 'zombie_wall_head']

def load_block_list():
    """从文件加载方块列表，若文件不存在则返回默认列表"""

    if os.path.exists(BLOCK_LIST_FILE):
        with open(BLOCK_LIST_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # print(f"警告：未找到 {BLOCK_LIST_FILE}，使用默认方块列表（请确认是否完整）")
        return DEFAULT_BLOCK_LIST

def format_uuid(uuid_str):
    """确保 UUID 为带连字符的标准格式（若传入无连字符则转换）"""

    uuid_str = uuid_str.replace("-", "")
    if len(uuid_str) != 32:
        raise ValueError(f"无效的 UUID 长度: {len(uuid_str)}")
    return f"{uuid_str[:8]}-{uuid_str[8:12]}-{uuid_str[12:16]}-{uuid_str[16:20]}-{uuid_str[20:]}"

def calculate_mining(data, block_list):
    """计算指定方块的挖掘总次数"""
    if "minecraft:mined" not in data.get("stats", {}):
        return 0
    mined = data["stats"]["minecraft:mined"]
    total = 0
    for block in block_list:
        # 确保 block 是完整的资源位置，例如 "minecraft:stone"
        if not block.startswith("minecraft:"):
            block = f"minecraft:{block}"
        total += mined.get(block, 0)
    return total

def calculate_placing(data, block_list):
    """计算指定方块的放置总次数"""
    if "minecraft:used" not in data.get("stats", {}):
        return 0
    used = data["stats"]["minecraft:used"]
    total = 0
    for block in block_list:
        # 确保 block 是完整的资源位置，例如 "minecraft:stone"
        if not block.startswith("minecraft:"):
            block = f"minecraft:{block}"
        total += used.get(block, 0)
    return total

def calculate_play_time(data):
    """计算世界打开时间"""
    if "minecraft:custom" not in data.get("stats", {}):
        return 0

    custom_data = data["stats"]["minecraft:custom"]    
    play_time = round(custom_data.get("minecraft:play_time", 0) / 20 / 3600)
    return play_time

def main():
    # 加载 UUID 映射
    with open(UUID_MAP_FILE, 'r', encoding='utf-8') as f:
        uuid_map = json.load(f)  # 格式：{"玩家名": "带连字符UUID"}

    # 加载方块列表
    block_list = load_block_list()

    commands = []  # 存储最终要写入文件的计分板命令
    skipped = []   # 记录跳过的玩家

    for player_name, uuid in uuid_map.items():
        # 确保 UUID 为标准格式（带连字符）
        uuid_std = format_uuid(uuid)
        stat_file = os.path.join(STATS_FOLDER, f"{uuid_std}.json")

        if not os.path.exists(stat_file):
            print(f"跳过 {player_name}：统计文件不存在 {stat_file}")
            skipped.append((player_name, "文件不存在"))
            time.sleep(0.1)
            continue

        try:
            with open(stat_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"跳过 {player_name}：读取文件失败 {e}")
            skipped.append((player_name, f"读取错误: {e}"))
            time.sleep(0.1)
            continue

        # BOT 检测（可选，若不需要可注释掉）

        mining_total = calculate_mining(data, block_list)
        placing_total = calculate_placing(data, block_list)
        play_time_total = calculate_play_time(data)
        time.sleep(0.2)
        commands.append(f"scoreboard players set {player_name} leaderboard.mined_block {mining_total}")
        commands.append(f"scoreboard players set {player_name} leaderboard.used_block {placing_total}")
        commands.append(f"scoreboard players set {player_name} leaderboard.online_time {play_time_total}")
        print('')
        print(f"{player_name} 挖掘总数: {mining_total}")
        print(f"{player_name} 放置总数: {placing_total}")
        print(f"{player_name} 在线时间: {play_time_total}")
        print('')


    # 写入 mcfunction 文件
    with open(OUTPUT_FUNCTION, 'w', encoding='utf-8') as f:
        f.write("# 自动生成的 leaderboard 同步命令\n")
        f.write(f"# 生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# 处理的玩家数: {len(commands)/3}\n")
        f.write("# =================================\n\n")
        f.write("\n".join(commands))

    time.sleep(0.4)
    print(f"\n完成！共生成 {len(commands)} 条命令，保存至 {OUTPUT_FUNCTION}")
    if skipped:
        time.sleep(0.1)
        print("跳过的玩家：")
        for name, reason in skipped:
            print(f"  {name}: {reason}")
            time.sleep(0.04)

if __name__ == "__main__":
    time.sleep(1)
    main()
    os.system( 'pause ')