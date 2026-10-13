import json, sys, urllib.request
sys.stdout.reconfigure(encoding="utf-8")

SRC = r"E:/ComfyUI_windows_portable/min_h3.api.json"
DST = r"E:/ComfyUI_windows_portable/verify_lv.api.json"
API = "http://127.0.0.1:8188"

d = json.load(open(SRC, encoding="utf-8"))
dirk = [k for k, v in d.items() if v["class_type"] == "MiniMaxH3Director"][0]
dv = d[dirk]["inputs"]

dv["width"] = 544
dv["height"] = 960
dv["steps"] = 1
dv["ref_max_size"] = 960
dv["clear_vram_between_segments"] = True

# 改用纯 Triton、不依赖 sageattention 的低显存注意力节点
upstream = dv["model"]
nid = "910"
while nid in d:
    nid = str(int(nid) + 1)
d[nid] = {
    "class_type": "MiniMaxLowVRAMAttention",
    "inputs": {"model": upstream, "head_chunks": 4},
}
dv["model"] = [nid, 0]
print("inserted MiniMaxLowVRAMAttention (head_chunks=4) node", nid, "after", upstream)

for k, v in d.items():
    if v["class_type"] in ("SaveVideo", "VHS_VideoCombine"):
        for ik in ("filename_prefix", "prefix"):
            if ik in v["inputs"]:
                v["inputs"][ik] = "video/LV验证_长眉真人传S2"

json.dump(d, open(DST, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

op = urllib.request.build_opener(urllib.request.ProxyHandler({}))
req = urllib.request.Request(API + "/prompt",
                             data=json.dumps({"prompt": d}).encode("utf-8"),
                             headers={"Content-Type": "application/json"})
try:
    r = json.loads(op.open(req, timeout=60).read().decode("utf-8"))
    if "error" in r:
        print("SUBMIT ERROR:", json.dumps(r, ensure_ascii=False)[:1200])
    else:
        print("SUBMITTED prompt_id =", r.get("prompt_id"))
        print("node_errors =", r.get("node_errors"))
except urllib.error.HTTPError as e:
    print("HTTP ERROR", e.code, e.read().decode("utf-8", "ignore")[:1200])
