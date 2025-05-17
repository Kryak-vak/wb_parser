from httpx import URL

from py_mini_racer import py_mini_racer


def calc_card_url(nm_id: int, js_funcs: tuple[str]) -> URL:
    js_funcs_f = ','.join(js_funcs)

    ctx = py_mini_racer.MiniRacer()
    ctx.eval("const wb = { settings: { secondHost: null } };")
    ctx.eval(f"const u = {{{js_funcs_f}}};")
    card_url = ctx.call("u.constructHostV2", nm_id)
    card_url: URL = URL(f'{card_url}/info/ru/card.json')

    return card_url