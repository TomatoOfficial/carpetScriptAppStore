import requests
import json
import time

def format_uuid(uuid_no_hyphen):
    return f"{uuid_no_hyphen[:8]}-{uuid_no_hyphen[8:12]}-{uuid_no_hyphen[12:16]}-{uuid_no_hyphen[16:20]}-{uuid_no_hyphen[20:]}"

def fetch_uuids(player_names, output_file='player_uuids.json', delay=0.3):
    uuid_mapping = {}

    for name in player_names:
        url = f"https://api.mojang.com/users/profiles/minecraft/{name}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                raw_uuid = data['id']                 # 32 位无连字符
                formatted_uuid = format_uuid(raw_uuid)
                uuid_mapping[name] = formatted_uuid
                print(f"成功获取 {name} -> {formatted_uuid}")
            else:
                print(f"玩家 {name} 不存在或请求失败，状态码: {response.status_code}")
                uuid_mapping[name] = None
        except Exception as e:
            print(f"请求 {name} 时发生异常: {e}")
            uuid_mapping[name] = None

        time.sleep(delay)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(uuid_mapping, f, ensure_ascii=False, indent=4)

    print(f"完成！结果已保存至 {output_file}")

# 单独使用的转换示例
if __name__ == "__main__":

    # 实际获取玩家 UUID（请替换为你的玩家列表）
    player_list = ['LoserWen', 'Haloshrimpx', 'kertimesim', 'galiwanzi', 'its__crimson', 'lllast', 'lin_gsh', 'CoKeLaoda', 'ReToForest', 'TomatoOfficial', 'sagiri1235', 'syltus_233', 'yetingxue258', 'izhi999', 'SweetLuo258', 'CrystalCube_xwx', 'MC_XiaoQing', 'loserwen1', 'YYZ_fanliuo', 'NNRSP', 'LZeniths_', 'kong_ji', 'Quadrant_united', 'V_Cr_Og', 'bqm870870', 'guhaol', 'VegeBear', 'the_wolves', 'INGLyYyyy', '_o_v_0_']
    fetch_uuids(player_list)