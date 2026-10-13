import json, sys, os, urllib.request
sys.stdout.reconfigure(encoding="utf-8")

SRC = r"E:/ComfyUI_windows_portable/min_h3.api.json"
DST = r"E:/ComfyUI_windows_portable/verify_sa.api.json"
API = "http://127.0.0.1:8188"

d = json.load(open(SRC, encoding="utf-8"))

# --- 1. 定位 Director ---
dirk = [k for k, v in d.items() if v["class_type"] == "MiniMaxH3Director"][0]
dv = d[dirk]["inputs"]
print("Director node:", dirk)

# --- 2. 最小化参数 ---
dv["width"] = 544
dv["height"] = 960
dv["steps"] = 1
dv["ref_max_size"] = 960
dv["clear_vram_between_segments"] = True
print("params -> %sx%s  steps=%s  ref=%s" % (dv["width"], dv["height"], dv["steps"], dv["ref_max_size"]))

# --- 3. 插入 SageAttention 补丁节点 ---
upstream = dv["model"]          # ['62', 0]
new_id = "900"
while new_id in d:
    new_id = str(int(new_id) + 1)
d[new_id] = {
    "class_type": "MiniMaxH3MemoryEfficientSageAttentionPatch",
    "inputs": {"model": upstream},
}
dv["model"] = [new_id, 0]
print("inserted SageAttention patch node", new_id, "after", upstream)

# --- 4. 输出文件名区分 ---
for k, v in d.items():
    if v["class_type"] in ("SaveVideo", "VHS_VideoCombine"):
        for ik in ("filename_prefix", "prefix"):
            if ik in v["inputs"]:
                v["inputs"][ik] = "video/SA验证_" + str(v["inputs"][ik]).replace("video/", "")
                print("SaveVideo prefix ->", v["inputs"][ik])

json.dump(d, open(DST, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("written:", DST)

# --- 5. 校验图 ---
op = urllib.request.build_opener(urllib.request.ProxyHandler({}))
payload = json.dumps({"prompt": d}).encode("utf-8")
req = urllib.request.Request(API + "/prompt", data=payload,
                             headers={"Content-Type": "application/json"})
try:
    r = json.loads(op.open(req, timeout=60).read().decode("utf-8"))
    if "error" in r:
        print("SUBMIT ERROR:")
        print(json.dumps(r, ensure_ascii=False)[:1500])
    else:
        print("SUBMITTED prompt_id =", r.get("prompt_id"))
        print("node_errors =", r.get("node_errors"))
except urllib.error.HTTPError as e:
    print("HTTP ERROR", e.code)
    print(e.read().decode("utf-8", "ignore")[:1500])
