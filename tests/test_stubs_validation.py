from dragon import PROJECT_ROOT

stubs_path = PROJECT_ROOT / 'stubs'

import toml


def has_right_key(kv: dict, k: str) -> bool:
    return kv.get(k, "WRONG") != "WRONG"


def test_lookup_paths_validation():
    target_paths = stubs_path.glob('*.toml')
    for path in target_paths:
        r = toml.load(path)
        name = r['name']
        config = r['config']
        lookup_paths = config['lookup_paths']
        order_cnt = 1
        default_hit_unique_cnt = 0
        for p in lookup_paths:
            assert has_right_key(p, 'order')
            assert p['order'] == order_cnt, f"{ path.name } error"
            order_cnt += 1
            assert has_right_key(p, 'path')
            assert has_right_key(p, 'need_auth')
            assert has_right_key(p, 'default_hit')
            if p['default_hit']: default_hit_unique_cnt += 1
        assert default_hit_unique_cnt == 1, f"{path.name} error"

