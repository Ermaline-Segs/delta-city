def rp(s,x,y,n=1):
    assert s.count(x)==n,(x[:70],s.count(x)); return s.replace(x,y)
def apply(head):
    head=rp(head,'<div class="toast" id="toast" hidden></div>','''<div class="toast" id="toast" hidden></div>
    <div id="guide" class="guide" hidden></div>\n<div id="choose" class="choose" hidden></div>
    <button id="act" class="act" hidden>Talk to Violet</button>
    <div id="talk" class="talk" hidden></div>
    <script id="person" type="application/json">'''+open('person_light.json').read()+'''</script>''')
    head=rp(head,"[hidden]{display:none !important}",'''[hidden]{display:none !important}
    .choose{position:fixed;inset:0;z-index:5;display:grid;place-items:center;padding:16px;background:rgba(10,18,32,.72);overflow:auto;touch-action:auto}
.choose .card{width:min(620px,100%);background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:20px}
.choose h1{margin:0 0 4px;font-size:26px}.choose p{margin:0 0 12px;opacity:.8}.choose .lab{font-weight:700;font-size:14px;margin:12px 0 6px}
.choose .seg{display:flex;gap:8px}.choose .seg button{flex:1;border-radius:12px;padding:11px}
.choose .looks{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.choose .look{border-radius:14px;padding:6px 6px 10px;display:grid;gap:6px;justify-items:center;font-weight:700}
.choose .look img{width:100%;border-radius:10px;display:block}.choose button.on{background:#167C80;border-color:#167C80;color:#fff}.choose .go{width:100%;margin-top:14px;padding:13px;border-radius:12px;background:#14263D;color:#fff;border-color:#14263D;font-size:16px}.choose .go:disabled{opacity:.45}
.certimg{display:block;width:100%;max-width:420px;margin:8px auto;border-radius:6px;box-shadow:0 4px 18px rgba(0,0,0,.25)}
.guide{position:fixed;left:50%;top:calc(62px + env(safe-area-inset-top,0px));transform:translateX(-50%);background:#167C80;color:#fff;font-weight:700;font-size:15px;padding:10px 16px;border-radius:12px;max-width:min(92vw,620px);text-align:center;box-shadow:0 6px 18px rgba(0,0,0,.25)}
    @media (max-width:760px){.guide{top:calc(128px + env(safe-area-inset-top,0px));font-size:14px}}
    .act{position:fixed;left:50%;bottom:calc(92px + env(safe-area-inset-bottom,0px));transform:translateX(-50%);background:#167C80;color:#fff;border:0;font-size:16px;padding:12px 22px;box-shadow:0 6px 18px rgba(0,0,0,.25)}
    .talk{position:fixed;left:50%;bottom:calc(14px + env(safe-area-inset-bottom,0px));transform:translateX(-50%);width:min(560px,calc(100vw - 20px));max-height:min(78vh,640px);overflow:auto;background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:16px;-webkit-user-select:text;user-select:text;touch-action:auto;box-shadow:0 12px 40px rgba(0,0,0,.3)}
    .talk .who{font-weight:800;font-size:18px;margin-bottom:6px}.talk .who span{font-weight:500;font-size:13px;opacity:.7;margin-left:6px}
    .talk p{margin:6px 0 10px;line-height:1.45}.talk label,.talk .lab{display:block;font-size:13.5px;font-weight:600;margin:8px 0 4px}
    .talk input{display:block;width:100%;margin-top:4px;padding:10px 12px;border-radius:10px;border:1.5px solid var(--line);background:transparent;color:inherit;font:inherit}
    .talk .row{display:flex;flex-wrap:wrap;gap:8px;margin-top:6px}.talk button{border-radius:10px;background:#14263D;color:#fff;border-color:#14263D}.talk button.ghost{background:transparent;color:var(--ink);border-color:var(--line)}.talk button.on{background:#167C80;border-color:#167C80;color:#fff}
    .talk .err{color:#c0392b;font-weight:600;min-height:1.2em}.talk .bar{height:12px;border-radius:999px;background:rgba(127,127,127,.25);overflow:hidden}.talk .bar i{display:block;height:100%;background:#167C80;transition:width .5s ease}
    .cert{border:3px double #14263D;border-radius:12px;background:#fbfaf3;color:#14263D;overflow:hidden;margin:8px 0}.cert .ctop{background:#14263D;color:#fff;text-align:center;padding:10px;font-size:12.5px;letter-spacing:1px}.cert .ctop b{display:block;font-size:20px;letter-spacing:2px;margin-top:2px}
    .cert .cno{text-align:center;font-size:24px;font-weight:800;padding:10px 0 2px;color:#167C80}.cert dl{display:grid;grid-template-columns:auto 1fr;gap:6px 16px;margin:0;padding:10px 16px 14px;font-size:15px}.cert dt{opacity:.65}.cert dd{margin:0;font-weight:700}''')

    return head
