# dsplayer-plugin

DsPlayer 插件官方市场仓库：`market.json` 为市场索引（在线安装入口），`packages/` 存放插件包，`icons/` 存放插件图标。

## 当前收录（8 个插件）

| 插件 | id | 版本 | 类型 | 包 |
|---|---|---|---|---|
| 媒体代理服务 | `mediaProxy` | 1.1.0 | import（zip） | `packages/mediaProxy-1.1.0.zip` |
| Node.js 运行时 | `nodejs` | 1.0.0 | import（zip） | `packages/nodejs-1.0.0.zip` |
| PHP 运行时 | `php` | 1.0.0 | import（zip） | `packages/php-1.0.0.zip` |
| Python 爬虫引擎 | `py` | 1.0.7 | **apk**（系统安装） | `packages/DsPlayer-Python-plugin-1.0.7-arm64.apk` |
| MPV 播放内核 | `mpv` | 1.0.1 | import（apk 直装包可导入） | `packages/mpv-1.0.1.apk` |
| QJS 爬虫引擎 | `qjs` | 1.0.0 | import | `packages/qjs-1.0.0.apk` |
| fjs 引擎（drpy3 源） | `fjs` | 1.0.0 | import | `packages/fjs-1.0.0.apk` |
| AI 助手界面 | `agent` | 1.0.0 | import | `packages/agent-1.0.0.apk` |

图标在 `icons/`（与条目 `icon` 字段对应）；fjs 暂与 QJS 共用 JS 图标（`icons/fjs.png`），可随时替换。

## 使用

DsPlayer → 插件中心 → 市场 → 添加市场，填入本仓库索引直链：

```
https://raw.githubusercontent.com/hjdhnx/dsplayer-plugin/main/market.json
```

### 镜像与加速

GitHub 直连不畅时，任选其一（DsPlayer 内「管理市场 → GitHub 加速代理」已内置前两个，无需手动拼地址）：

- jsDelivr CDN：`https://cdn.jsdelivr.net/gh/hjdhnx/dsplayer-plugin@main/market.json`
  - ⚠️ jsDelivr 对分支引用有 CDN 缓存（索引推送后可能滞后数小时）。索引更新后可主动刷新缓存：
    `https://purge.jsdelivr.net/gh/hjdhnx/dsplayer-plugin@main/market.json`（浏览器访问一次即可）
- gh-proxy 类前缀代理（实测推荐序，2026-09-17）：
  1. `https://gh-proxy.com/` —— 最快最稳（zip 完整 ~960KB/s），DsPlayer 内置默认
  2. `https://gh-proxy.playdreamer.cn/` —— 稳定
  3. `https://github.catvod.com/` —— 偶发 502/截断，备选
- 用法：前缀 + 完整原始 URL，如 `https://gh-proxy.com/https://raw.githubusercontent.com/hjdhnx/dsplayer-plugin/main/market.json`

## 索引格式

见 `market.json` 与 DsPlayer 仓库 `docs/plugin/PLUGIN-MARKET-DESIGN.md` §二：

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | ✓ | 插件唯一身份：binary/runtime 插件 = 包内 plugin.json 的 `name`；内置引擎 = `mpv/py/qjs/fjs/agent`；与本地已装判定对齐 |
| `name` / `version` / `url` | ✓ | 展示名 / 语义化版本 / 包地址（绝对直链或相对本索引的路径） |
| `type` | ✓ | `import` = 应用内静默导入；`apk` = APK 直装（系统安装器） |
| `icon` | | 图标地址（绝对 URL 或相对本索引的路径），未声明回落首字母占位 |
| `size` / `author` / `desc` / `tags` / `changelog` | | 展示元数据 |
| `sha256` | | 可选；声明后下载强制校验，不符拒装 |
| `minApp` | | 可选；要求的最低 DsPlayer 版本，不满足时安装按钮置灰 |

## 自建市场

任意能放静态文件的地址（GitHub 仓库 / 对象存储 / 本地 sdcard）都可作市场：一份索引 JSON + 包文件即可。第三方条目的 `id` 同样须与包内 `plugin.json` 身份一致，否则已装判定不闭环。
