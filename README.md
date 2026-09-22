# dsplayer-plugin

DsPlayer 插件官方市场仓库：`market.json` 为市场索引（在线安装入口），`packages/` 存放插件包，`icons/` 存放条目图标。

## 当前收录（12 个条目 = 环境 8 + 应用 4）

条目带 `category` 字段（2026-09-20 起）：`env`=环境（引擎/运行时，给壳子供能力，默认归类）；`app`=应用（面向完整使用场景：整合包、直播源包、服务包）。市场内按类别过滤，默认展示「环境」。

### 环境（env）

| 条目 | id | 版本 | type | 包 |
|---|---|---|---|---|
| 媒体代理服务 | `mediaProxy` | 1.1.1 | import（zip） | `packages/mediaProxy-1.1.1.zip` |
| Node.js 运行时 | `nodejs` | 1.0.0 | import（zip） | `packages/nodejs-1.0.0.zip` |
| PHP 运行时 | `php` | 1.3.1 | import（zip） | `packages/php-1.3.1.zip` |
| Python 爬虫引擎 | `py` | 1.0.8 | **apk**（系统安装） | `packages/DsPlayer-Python-plugin-1.0.8-arm64.apk` |
| MPV 播放内核 | `mpv` | 1.0.2 | import（apk 直装包可导入） | `packages/mpv-1.0.2.apk` |
| QJS 爬虫引擎 | `qjs` | 1.0.1 | import | `packages/qjs-1.0.1.apk` |
| fjs 引擎（dr3 源） | `fjs` | 1.0.0 | import | `packages/fjs-1.0.0.apk` |
| AI 助手界面 | `agent` | 1.0.0 | import | `packages/agent-1.0.0.apk` |

### 应用（app）

| 条目 | id | 版本 | type | 包 |
|---|---|---|---|---|
| 插件整合包 | `bundle` | 1.0.7 | **apk**（系统安装） | `packages/DsPlayer-Plugin-Bundle-1.0.7-arm64.apk` |
| IPTV 直播源（CCSH 采集） | `iptv-ccsh` | 1.0.0 | **live**（直播源包） | `packages/iptv-ccsh.json` |
| 洛雪同步 | `lx-sync` | 2.1.2 | **server**（服务包） | `packages/lx-sync-2.1.2.zip` |
| 弹幕 API 服务 | `danmu-api` | 1.0.0 | **server**（服务包） | `packages/danmu-1.0.0.zip` |

### 引擎类条目版本要点

| 条目 | 当前版本 | 要点 |
|---|---|---|
| `mpv` | 1.0.2 | libmpv 重编入 DASH（MPD）demuxer（上游构建缺 libxml2 致 `ff_dash_demuxer` 未编入，DASH 源此前须降级 Exo）；内核 1.2.5 → 1.2.6 |
| `qjs` | 1.0.1 | 根治跨 isolate SIGABRT 闪退——so 回调从进程级全局改 per-context 注册 |
| `bundle` | 1.0.7 | 整合包内置子插件刷新：mpv 1.0.2（DASH 原生）/ qjs 1.0.1（根治闪退）/ php 1.3.1 |

各包完整变更说明见 `market.json` 条目的 `changelog` 字段（DsPlayer 详情弹层直接展示）。

图标在 `icons/`（与条目 `icon` 字段对应；fjs 暂与 QJS 共用 JS 图标）。`iptv.png` 为已弃用的旧版图标（被 `iptv2.png` 取代，保留留档）。

弹幕 API 服务配套用法：服务启动后，DsPlayer 设置 → 播放器 → 弹幕接口 填 `http://127.0.0.1:9321`，播放无自带弹幕的影片即自动按标题匹配（兼容弹弹play 协议）。

## 条目形态（type）与安装语义

| type | 包体 | 安装动作 | 典型条目 |
|---|---|---|---|
| `import` | zip / apk | 应用内静默导入（组件落应用内目录） | 引擎/运行时类 |
| `apk` | apk | 跳系统安装器直装 | py、bundle |
| `live` | JSON（`{"lives":[{name,url,ua,epg}]}`） | 写入直播配置并启用，切直播页生效；**订阅制**（内容指向外部地址时随源自动更新） | iptv-ccsh |
| `server` | zip（根部须有 `server.json` manifest：`serviceName/workDir/entry/port/healthType/desc`） | 解压到 `sdcard/dsplayer/server/node/`（覆盖式，数据目录保留）+ **自动创建服务配置**（nodejs 运行时启动；服务 id 约定 `svc-mkt-<条目id>`，已存在跳过） | lx-sync、danmu-api |

`server` 包要求设备已装 `nodejs` 运行时插件；manifest 字段由 DsPlayer 市场安装器消费（见 DsPlayer 仓库 `MarketManager.installServerPackage`）。

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
  1. `https://gh-proxy.com/` —— 最快最稳，DsPlayer 内置默认
  2. `https://gh-proxy.playdreamer.cn/` —— 稳定
  3. `https://github.catvod.com/` —— 偶发 502/截断，备选
- 用法：前缀 + 完整原始 URL，如 `https://gh-proxy.com/https://raw.githubusercontent.com/hjdhnx/dsplayer-plugin/main/market.json`

## 索引格式

见 `market.json` 与 DsPlayer 仓库 `docs/plugin/PLUGIN-MARKET-DESIGN.md` §二：

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | ✓ | 条目唯一身份：binary/runtime 插件 = 包内 plugin.json 的 `name`；内置引擎 = `mpv/py/qjs/fjs/agent`；应用类自定（iptv-ccsh/lx-sync/danmu-api） |
| `name` / `version` / `url` | ✓ | 展示名 / 语义化版本 / 包地址（绝对直链或相对本索引的路径） |
| `type` | ✓ | `import` / `apk` / `live` / `server`（语义见上表） |
| `category` | | `env`（默认）/ `app`；未声明归 env |
| `icon` | | 图标地址（绝对 URL 或相对本索引的路径），未声明回落首字母占位 |
| `size` / `author` / `desc` / `tags` / `changelog` | | 展示元数据 |
| `md5` | | 包校验和（32 位 hex）；**声明即强制校验**，不符拒装防篡改。官方 12 包全量声明，可用 `md5sum packages/<包名>` 复核 |
| `minApp` | | 可选；要求的最低 DsPlayer 版本，不满足时安装按钮置灰 |

## 发布约定（2026-09-20 起执行）

1. **同名包绝不重传**：内容有任何变化一律升版本号并换新文件名（如 `lx-sync-2.1.2.zip`），代理/CDN 层对同名文件的缓存会导致客户端「md5 校验不符」假失败（lx-sync 实锤）。旧版本包删除（git 历史留档）。
2. `md5` / `size` / `version` / `changelog` 与包严格同步；顶层 `updatedAt` 每次发布刷新。
3. `server` 条目包内 `server.json` 为安装指令，DsPlayer 安装时跳过落盘；`live` 条目包体即数据。
4. 图标换图时**换文件名**（如 `iptv.png`→`iptv2.png`），客户端图片磁盘缓存按 URL 键控。

## 自建市场

任意能放静态文件的地址（GitHub 仓库 / 对象存储 / 本地 sdcard）都可作市场：一份索引 JSON + 包文件即可。第三方条目的 `id` 须与包内 `plugin.json` 身份一致（`live`/`server` 条目除外：`live` 无插件身份，`server` 以 manifest 建服务），否则已装判定不闭环。
