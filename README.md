# ComfyUI Portable 仓库

ComfyUI Windows Portable 发行版的**外围脚本仓库**。
内层 `ComfyUI/` 是官方仓库克隆（含 700GB+ 模型），已在 `.gitignore` 中排除，
本仓库只跟踪**启动脚本、更新脚本、自定义工具、配置等轻量内容**。

---

## 📦 仓库结构

```
comefyUI/                         ← GitHub 仓库（本仓库）
├── .gitignore                    ← 屏蔽大体积内容的规则
├── README.md                     ← 本文件
├── run_nvidia_gpu.bat            ← 启动脚本（NVIDIA GPU）
├── run_cpu.bat                   ← 启动脚本（CPU）
├── update/                       ← ComfyUI 更新脚本
├── advanced/                     ← 高级启动选项
└── *.py / *.json / *.txt         ← 自定义工具脚本、配置
```

**不纳入版本控制的内容**：
| 路径 | 原因 |
|------|------|
| `ComfyUI/` | 官方仓库克隆 + 717GB 模型，独立 git 仓库 |
| `python_embeded/` | Python 嵌入式运行时（6.8GB），每次 portable 更新会变 |
| `sa_dl/` | 下载缓存（zip / wheel / 源码包） |

---

## 🔑 关键：Git 代理配置（必做）

本仓库的远程是 `https://github.com/ndnc002/comefyUI.git`，
**直连 github.com:443 会超时**，必须走 Clash for Windows 代理。
**Git + Windows schannel 存在 TLS 握手 bug**，必须切换到 OpenSSL。

### 一次性配置（全局生效，所有仓库复用）

```bash
# 1. 设置 HTTP(S) 代理（Clash for Windows 默认端口 7890）
git config --global http.proxy  http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890

# 2. 把 TLS 后端从 schannel 切换到 OpenSSL（不修这步 fetch/push 会报 SSL/TLS 握手失败）
git config --global http.sslBackend openssl
```

### 临时关闭代理（如果直连突然恢复）

```bash
git config --global --unset http.proxy
git config --global --unset https.proxy
```

### 验证代理是否生效

```bash
git ls-remote origin
# 成功 = 无输出（空仓库）或打印 refs
# 失败 = 报 Connection was reset / schannel: failed to receive handshake
```

---

## 📥 新电脑 clone 本仓库

```bash
# 1. 先配好代理（上面那三条 git config）

# 2. 克隆
git clone https://github.com/ndnc002/comefyUI.git comefyUI_custom

# 3. 进入仓库
cd comefyUI_custom

# 4. 如果是 ComfyUI portable 新电脑，把克隆下来的内容覆盖到 E:\ComfyUI_windows_portable\ 即可
#    (ComfyUI/、python_embeded/、sa_dl/ 都在 .gitignore 里，不会被覆盖)
```

---

## 📤 日常提交推送

```bash
cd E:\ComfyUI_windows_portable

# 查看哪些文件变了
git status

# 添加所有变更
git add .

# 提交
git commit -m "你的提交说明"

# 首次 push 后以后可以直接 git push，不用再带 -u origin main
git push -u origin main
```

---

## 🔄 拉取最新

```bash
cd E:\ComfyUI_windows_portable
git pull origin main
```

---

## 🧑‍💻 仓库身份（仓库级，不污染全局）

当前仓库的提交身份写在 `E:\ComfyUI_windows_portable\.git\config` 里：

```
user.name  = ndnc002
user.email = 46179593@qq.com
```

要改的话：

```bash
cd E:\ComfyUI_windows_portable
git config user.name "新名字"
git config user.email "新邮箱"
```

注意是 **仓库级**（不带 `--global`），这样改只影响本仓库，不会动其他项目。

---

## ⚠️ 注意事项

1. **Clash for Windows 必须保持运行**，否则 Git 连不上 GitHub。
2. 不要手动删 `.gitignore`，删了下次 `git add .` 会把 700GB+ 模型一起提交，必炸。
3. 内层 `ComfyUI/` 有自己的 `.git`，那是官方仓库，和本仓库无关，不要混着操作。
4. 如果 push 报身份验证失败，需要在 GitHub 里加一个 **Personal Access Token (PAT)** 或改用 SSH。
