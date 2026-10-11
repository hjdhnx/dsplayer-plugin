# dsplayer-plugin

DsPlayer 插件官方市场仓库：`market.json` 为市场索引（在线安装入口），`packages/` 存放插件包，`icons/` 存放条目图标。

## 当前收录（23 个条目 = 环境 16 + 应用 7）

条目带 `category` 字段（2026-09-20 起）：`env`=环境（引擎/运行时，给壳子供能力，默认归类）；`app`=应用（面向完整使用场景：整合包、直播源包、服务包）。市场内按类别过滤，默认展示「环境」。

**platforms 规范（2026-10-10 起，官方仓铁律，check_market.py 闸门强制）**：全量条目显式声明 `platforms`，零缺省（缺省=不限平台的语义仅为三方市场兼容保留）。词表 `android`/`win32`（预留 `linux`）。二进制形态条目（import/apk）**恰好一个平台词**——一个条目一个平台、包内只含该平台二进制（禁多合一合包，跨平台插件拆 `-win` 独立条目、版本独立线）；数据类条目（live/server/source）无二进制，标全平台组合 `["android","win32"]`，新平台加入时按此账本补标。win32 条目必须设 `minApp`（承载 PC 插件支持的最低本体版本）。包内适配以 plugin.json 的 binaries 平台键终判。发版前先跑 `python check_market.py`，六项全 PASS 才允许 commit（README 条目表↔market.json↔packages/ 一致性由它保证，不靠人肉）。

### 环境（env）

| 条目 | id | 版本 | type | 包 |
|---|---|---|---|---|
| 媒体代理服务 | `mediaProxy` | 1.2.2 | import（zip；platforms=android） | `packages/mediaProxy-1.2.2.zip` |
| 媒体代理服务（Windows） | `mediaProxy-win` | 1.0.0 | import（zip；platforms=win32，minApp 0.9.4） | `packages/mediaProxy-win-1.0.0.zip` |
| Node.js 运行时 | `nodejs` | 1.0.0 | import（zip；platforms=android） | `packages/nodejs-1.0.0.zip` |
| Node.js 运行时（Windows） | `nodejs-win` | 1.0.0 | import（zip；platforms=win32，minApp 0.9.4） | `packages/nodejs-win-1.0.0.zip` |
| PHP 运行时 | `php` | 1.3.2 | import（zip；platforms=android） | `packages/php-1.3.2.zip` |
| PHP 运行时（Windows） | `php-win` | 1.0.1 | import（zip；platforms=win32，minApp 0.9.4） | `packages/php-win-1.0.1.zip` |
| Python 运行时 | `python` | 1.0.2 | import（zip；platforms=android） | `packages/python-1.0.2.zip` |
| Python 运行时（Windows） | `python-win` | 1.1.2 | import（zip；platforms=win32，minApp 0.9.4） | `packages/python-win-1.1.2.zip` |
| Python 爬虫引擎 | `py` | 1.1.6 | **apk**（系统安装；platforms=android） | `packages/DsPlayer-Python-plugin-1.1.6-arm64.apk` |
| MPV 播放内核 | `mpv` | 1.0.2 | import（apk 直装包可导入；platforms=android） | `packages/mpv-1.0.2.apk` |
| MPV 播放内核（Windows） | `mpv-win` | 1.0.0 | import（zip；platforms=win32，minApp 0.9.5） | `packages/mpv-win-1.0.0.zip` |
| IJK 播放内核 | `ijk` | 1.0.2 | **apk**（桥接式必须系统安装；platforms=android） | `packages/ijk-1.0.2.apk` |
| FFmpeg 软解 | `ffmpeg` | 1.0.2 | **apk**（系统安装；需本体 v0.6.2+；platforms=android） | `packages/ffmpeg-1.0.2.apk` |
| QJS 爬虫引擎（dr2 + dr3 源） | `qjs` | 1.0.5 | import（platforms=android） | `packages/qjs-1.0.5.apk` |
| QJS 爬虫引擎（Windows） | `qjs-win` | 1.0.6 | import（zip；platforms=win32，minApp 0.9.5） | `packages/qjs-win-1.0.6.zip` |
| AI 助手界面 | `agent` | 1.1.0 | import（platforms=android） | `packages/agent-1.1.0.apk` |

### 应用（app）

| 条目 | id | 版本 | type | 包 |
|---|---|---|---|---|
| 插件整合包 | `bundle` | 1.1.0 | **apk**（系统安装；platforms=android） | `packages/bundle-1.1.0.apk` |
| IPTV 直播源（CCSH 采集） | `iptv-ccsh` | 1.1.0 | **live**（直播源包；platforms=android+win32） | `packages/iptv-ccsh-1.1.0.json` |
| 洛雪同步 | `lx-sync` | 2.1.2 | **server**（服务包；platforms=android+win32） | `packages/lx-sync-2.1.2.zip` |
| 弹幕 API 服务 | `danmu-api` | 1.0.0 | **server**（服务包；platforms=android+win32） | `packages/danmu-1.0.0.zip` |
| 演示源包 | `demo-sources` | 1.2.5 | **source**（源码包；platforms=android+win32；html/ 含 bilibili 完整源 + Web 源演示 + 歪比巴卜 booster——需本体 ≥0.9.7） | `packages/demo-sources-1.2.5.zip` |
| catLib 引擎库包 | `catlib` | 1.0.0 | **source**（源码包；引擎库；platforms=android+win32） | `packages/catlib-1.0.0.zip` |
| IDM+ 下载器（1DM+） | `idmplus` | 18.2 | **apk**（系统安装；Release 分发；platforms=android） | `idmplus-18.2-CN.apk` |
| MT管理器 | `mtmanager` | 2.14.5 | **apk**（系统安装；platforms=android） | `packages/mtmanager-2.14.5.apk` |

### 引擎类条目版本要点

| 条目 | 当前版本 | 要点 |
|---|---|---|
| `mediaProxy` | 1.2.2 | **1.2.2 单平台拆包（MARKET-PLATFORM-ADAPT）**：双平台合包按平台拆为两个独立条目——`mediaProxy` 只面向 Android（1.2.2，包内仅 ELF，与 1.2.1 二进制同源同 md5，瘦身约 2.4MB）+ 新条目 `mediaProxy-win`（1.0.0 起独立版本线，包内仅 PE）。已装 1.2.1 合包的 Windows 用户不做自动迁移（已装豁免显示，装新卸旧自定）。此前 1.2.1 纠正 1.2.0 win 二进制误用旧源构建（win/android 同源同引擎 leader-follower 流式分段） |
| `php` | 1.3.2 | 1.3.2 t4_demo BaseSpider 代理统一：`getProxyUrl()` 拿本源代理基址（php -S 通道 run() 自感知自身脚本 `?do=proxy&` 端点；drpyS 桥通道接服务层 env 注入）+ `localProxy($params)` 钩子与 `do=proxy` 分发（五元组契约直出，空图透明 GIF 兜底）——php 源代理写法与其他引擎统一，配套壳内《源本地代理指南》。已装旧版：服务页「示例」重释放 t4_demo 壳文件后重启 T4-PHP 服务生效（自带 lib/spider.php 改过的不覆盖）。drpyS 侧配套改动在 drpy-node 仓（_bridge.php env 注入 + php.js methodMapping） |
| `python` | 1.0.2 | CPython 3.12.15（musl）独立进程运行时，对齐 nodejs/php 服务形态。插件卡专属「依赖管理」（pip 装卸/刷新/搜索/二次确认）+「爬虫一键装」九件套。**1.0.2 鸿蒙 4.2 兼容两连修**：TMPDIR/HOME 注入插件内可写目录（部分 ROM 无 HOME 无 /tmp，pip 报 No usable temporary directory）；musl 平台探测 spawn 失败防御（部分 ROM fork/exec 受限报 /lib/ld-musl ENOENT 整包失败，现回落伪造标签照常装 musllinux wheel）。1.0.1 pip 平台标签修复（musllinux wheel 识别，lxml/pycryptodome 等 C 扩展免编译直装）。内置 DNS shim + CA + py.sh wrapper。需 DsPlayer 0.8.5+。fastapi 不可用（pydantic-core 无 musl wheel），Flask/标准库可用 |
| `mpv` | 1.0.2 | libmpv 重编入 DASH（MPD）demuxer（上游构建缺 libxml2 致 `ff_dash_demuxer` 未编入，DASH 源此前须降级 Exo）；内核 1.2.5 → 1.2.6 |
| `mpv-win` | 1.0.0 | 首发（PC 拆包 P2）：Windows MPV 内核市场化——0.9.5 起 release 本体不含 libmpv-2.dll（空壳 override 剔分发 + /DELAYLOAD 延迟加载），装本插件后可在内核面板选 MPV；dll 与历史内置同源（fork mpv-winbuild-cmake 20260607） |
| `py` | 1.1.6 | 1.1.6 T3 桩代理地址跨源污染根修——_PYUTIL_PROXY 模块级全局此前仅在源创建时写一次，任何一次空 proxyUrl 的源创建（网关未就绪窗口）清空全局、污染此后所有源的 getProxyUrl()；改为实例携带 proxy_url + 每次调用前刷新（实例锁串行）。1.1.5 localProxy 大载荷槽文件直传（PERF A1）根修——_invoke 引用未定义 env_str（NameError 被 except 静默吞）致 slotDir 恒空，槽通道从未生效（≥64KB proxy 体恒走 base64，IPC ×1.33 膨胀）；修复后写槽文件回 file:// + toBytes=4，图床源大图提速。1.1.4 新增编程调试 execCode 通道（AIDL 末尾追加，engine>=1.1.4）：执行任意 Python 片段，stdout/stderr 走 fd 二通道无 Binder 上限，work_dir 进 sys.path[0] 并临时 chdir，base.spider/pip 预装同源环境；`_result` 赋值 → 控制台 ⇒ 行。配套本体「编程调试」页；旧本体不受影响。1.1.3 恢复插件存储读权限（Manifest 此前仅 INTERNET）：文件浏览器式本地源（资源管理.py 等）在**插件进程**内列目录/读文件必需——无权限时对他人属主文件 stat 全 EACCES、目录恒 0 项；补 READ + MANAGE_EXTERNAL_STORAGE + requestLegacyExternalStorage（**仅读**，写删约束仍由 fs_guard + 无 WRITE 承载），装机后需授予「文件/存储」权限（应用详情→权限）。1.1.2 并发与自愈：同源长任务占锁 10s 快速报忙；源实例创建移出全局锁；修复 unloadSource 逐出通道静默空转；配套本体超时自动换实例 + 分发池 8 线程。1.1.1 修 BaseSpider 构造期崩溃（`__init__` 不再调用可被子类重写的 `self.log`，改模块级 `_log` 直调——hipy 源「资源管理」AttributeError 实锤，T3 官方基类对齐，上游 drpy-node 已同步修）。1.1.0 大响应 callBigFile 通道 + 抗杀保活开关（插件页 py 卡片，BIND_IMPORTANT，默认关） |同源长任务占锁时后续调用 10s 快速报忙（不再 30s 长队堆积）；源实例创建移出全局锁（新源首次加载不堵其他源）；修复 unloadSource 逐出通道自设计起静默空转；配套本体 v0.7.2+ debug（超时自动换实例 + 分发池 8 线程）后一个源失控不拖累其他源、失控源超时后秒级自愈。1.1.1 修 BaseSpider 构造期崩溃——`__init__` 不再调用可被子类重写的 `self.log`（改模块级 `_log` 直调）：源重写 log 且在 `super().__init__()` 之后才赋值其引用的属性时（hipy 源「资源管理」实锤 AttributeError），构造中断实例残废；T3 官方基类构造期不调 log，兼容性对齐，上游 drpy-node 已同步修。1.1.0 大响应 callBigFile 通道（AIDL 追加新方法，engine 1.1.0）+ 抗杀保活开关（插件页 py 卡片，BIND_IMPORTANT，默认关） |
| `python-win` | 1.1.2 | 1.1.2 引擎同步 1.1.6——T3 桩代理地址跨源污染根修（网关未就绪窗口的空 proxyUrl 源创建会清空全局代理地址；改为实例携带+调用前刷新）。1.1.1 引擎同步 1.1.5（localProxy 槽文件直传根修）+ worker /ping 新增 engine_md5 引擎指纹（DsPlayer 收养扫描版本检查：插件升级后残留旧 worker 不再被收养复用）。1.1.0 新增 PC 端 py 源本地执行 worker（`bin/py_worker_server.py` 常驻 127.0.0.1，端口 57591~57610 探测递补）：复用移动端 Chaquopy 插件同款引擎 manager.py（构建期从 plugin_python 拷入，md5 对账），init 后带缓存（实例 LRU 30/实例锁 10s 快返），DsPlayer 0.9.6+ PC 端 py-online/py-local 源直连可用，不再需要 drpys 服务中转；协议与移动端 AIDL envelope 完全一致（unknown-key 自愈链等语义保留）；POST body 支持 chunked 解码（DsPlayer 引擎的 HttpClient 恒走 chunked，实测修复空 body）。v1.0.0 首发：embeddable 3.12.10 + 爬虫九件套 + SSL 证书桥 |
| `qjs` | 1.0.5 | so 升级（qjs_ultra build-20261001-975e55b）：**qjs_update_stack_top 根治 isolate 线程迁移假 stack overflow**——Dart isolate 迁移 OS 线程后栈基线失配，512MB 许可仍随机假爆（dr3 引擎 worker 化真机实锤，md5 级浅调用即触发；dr2 的 64MB 时代偶发假爆栈为同根因弱形态）。宿主每入口刷新基线（QuickjsEngine 执行链汇聚点），新增 1 导出（ABI 兼容旧宿主，exports.txt 已登记）。需 DsPlayer 0.7.6+（drpy3 引擎 worker 化版本）配合。此前 1.0.4 so 升级（qjs_ultra build-20260930-b221bd5）：**根修源码模式模块装载的随机假语法错误**——quickjs 契约要求 JS_Eval 输入以 NUL 结尾，此前缺终结符导致 lexer 读穿缓冲区把相邻堆字节当源码解析（dr3 源装载高频报 SyntaxError 的根因，DSPlayer 侧对照实验 15/30→0/30）。ABI 与 1.0.3 一致（66 导出闸门校验），旧本体兼容。此前 1.0.3 so 升级（cheerio 补齐 :gt/:lt 切片，选择器伪类 + 链式方法，外部贡献合入），drpy2/drpy3 源 HTML 解析选择器更全。ABI 与 1.0.2 一致（66 导出闸门校验），旧本体兼容。此前 1.0.2 drpy3 源运行时并入本插件（fjs 退役下架）+ 原生 WebAssembly（wasm3）+ 墙钟超时中断/结构化错误/值转换护栏；1.0.1 根治跨 isolate SIGABRT（回调 per-context 注册） |
| `qjs-win` | 1.0.6 | 1.0.6 Windows dll WebAssembly 根修（qjs_ultra build-20261010-e2cfa2d，dll md5 5122b545）：MinGW PE 无 ELF mergeable .rodata，gcc LTO 常量传播把 wasm3 错误码物化成新字符串副本（与 m3_core.c 初始化字面量地址不同），指针同一性比较恒 false → LinkLibC 的 lookup-failure 抑制失效，WebAssembly.Instance 构造即抛 function lookup failed（最小 wasm 模块也炸；PC 央视频等 emscripten wasm 解密源全灭，Android ELF 同源码正常）。修复 = MinGW 构建下 wasm3 退出 LTO（Android 路径零影响），qjs_ultra CI 补 wasm 用例防假阳性。另累计三轮从未发过 Windows 包的 so 修复：1.0.3 cheerio 补齐（:gt/:lt 等）、1.0.4 模块装载 NUL 终结符（源码模式随机假语法错误）、1.0.5 qjs_update_stack_top（isolate 线程迁移假爆栈）。ABI 零变化，已装 1.0.0 直接覆盖升级即得全部修复。此前 1.0.0 首发（PC 拆包 P1）：Windows 引擎 dll 市场化——0.9.5 起 release 本体不再内置 quickjs_bridge.dll（CMake 改 Debug-only），dr2/dr3/cat 源与编程调试 js 通道按需安装本插件（native-lib 消费模式，落 plugins/qjs-win/bin/）。dll 与本体 vendored 逐字节一致（qjs_ultra 同源） |
| `bundle` | 1.1.0 | 移除 fjs 子插件（drpy3 并入 qjs 1.0.2），全家桶现为 MPV/Python/QJS/Agent 四插件；此前 1.0.9 agent 1.0.0→1.1.0（NextChat v2.15.8 + injectCompat） |
| `ijk` | 1.0.1 | 1.0.0 首版（DexClassLoader 桥接，CarGuo 修正版 ijkplayer，HTTPS/16K page size）真机播放/切集/连播/三内核切换全通；1.0.1 修 UA 透传——IJK n4.3 的 headers 字典不生效到 HTTP 请求头（部分 CDN/防盗链源拒默认 UA 报 400），UA 改走 user_agent 协议级 option 直达；1.0.2 桥 options 透传 FORMAT 类 setOption + protocol_whitelist 注入放行 rtmp/rtmps/rtsp/srt（ffmpeg 编译白名单默认不含，rtmp 直播频道此前 Protocol not on whitelist 黑屏；注入须在 Java 层 setDataSource 强写默认之后覆盖）。**必须 APK 直装**（files zip 导入会丢 dex 致本体探测失效） |
| `ffmpeg` | 1.0.2 | 1.0.2 修复软解画面纯色闪烁（Flutter SurfaceProducer 尺寸协商，需搭配最新本体）；1.0.1 补载 NDK C++ 运行时 libc++_shared.so（真机实锤：FongMi 编的 libavcodec 等动态依赖它，缺失时 dlopen 直接失败）；1.0.0 首版——FongMi/media fork（release-1.11.0-fongmi）编出的 decoder_ffmpeg so 载体：音频软解（AC3/EAC3/DTS 全家/TrueHD/Atmos 等）+ 视频软解（H.264/H.265/AV1/VP9/MPEG-4/AVS2/AVS3，Dolby Vision 基础层映射），为 Exo 内核补第三层解码兜底（硬解不支持自动回落，硬解可用时零开销）。**需本体 v0.6.2+**（media3 切 fork 版 + FfmpegDecoderLoader 加载链），**必须 APK 直装** |

各包完整变更说明见 `market.json` 条目的 `changelog` 字段（DsPlayer 详情弹层直接展示）。

图标在 `icons/`（与条目 `icon` 字段对应；fjs.png 已随条目下架弃用，保留留档）。`iptv.png` 为已弃用的旧版图标（被 `iptv2.png` 取代，保留留档）。

弹幕 API 服务配套用法：服务启动后，DsPlayer 设置 → 播放器 → 弹幕接口 填 `http://127.0.0.1:9321`，播放无自带弹幕的影片即自动按标题匹配（兼容弹弹play 协议）。

## 条目形态（type）与安装语义

| type | 包体 | 安装动作 | 典型条目 |
|---|---|---|---|
| `import` | zip / apk | 应用内静默导入（组件落应用内目录） | 引擎/运行时类 |
| `apk` | apk | 跳系统安装器直装 | py、bundle、ijk、ffmpeg、idmplus、mtmanager |
| `live` | JSON（`{"lives":[{name,url,ua,epg}]}`） | 写入直播配置并启用，切直播页生效；**订阅制**（内容指向外部地址时随源自动更新） | iptv-ccsh |
| `server` | zip（根部须有 `server.json` manifest：`serviceName/workDir/entry/port/healthType/desc`） | 解压到 `sdcard/dsplayer/server/node/`（覆盖式，数据目录保留）+ **自动创建服务配置**（nodejs 运行时启动；服务 id 约定 `svc-mkt-<条目id>`，已存在跳过） | lx-sync、danmu-api |
| `source` | zip（根部可选 `source.json` manifest：`{"dirs":["dr3","js"]}` 目录白名单缺省全解压；`{"target":"dsplayer"}` = 包内路径即 dsplayer 目录树整体解压，`spider/`、`server/` 等可共存） | 缺省解压到 `sdcard/dsplayer/spider/`（顶层目录与本地源扫描目录 `dr2`/`dr3`/`hipy`/`js` 同名直落位）；target=dsplayer 按包内路径落 `sdcard/dsplayer/` 树。覆盖式不影响包外文件；进对应本地源页自动扫描入库；已装态存 App 安装记录（更新 = 市场版本对比后重装）。**zip 文件名必须 UTF-8 编码**（7-Zip 默认按本地代码页打包中文名会乱码，用 Python zipfile/UTF-8 工具打包） | demo-sources |

`server` 包要求设备已装 `nodejs` 运行时插件；manifest 字段由 DsPlayer 市场安装器消费（见 DsPlayer 仓库 `MarketManager.installServerPackage`）。

大体积 APK（50MB 量级及以上）可不进 `packages/`，改发 GitHub Release 分发：tag 约定 `<id>-<version>`（升版本发新 tag，同名资产不覆盖——代理 CDN 缓存纪律同 packages/），asset 文件名避开 `+`/中文等需 URL 编码字符，条目 `url` 写**绝对直链**——客户端 `resolveMarketUrl` 对 `https://` 原样直通、`applyGithubProxy` 对 github.com 域自动套加速代理。首个样例 `idmplus`。

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
| `id` | ✓ | 条目唯一身份：binary/runtime 插件 = 包内 plugin.json 的 `name`；内置引擎 = `mpv/py/qjs/agent`；应用类自定（iptv-ccsh/lx-sync/danmu-api/demo-sources） |
| `name` / `version` / `url` | ✓ | 展示名 / 语义化版本 / 包地址（绝对直链或相对本索引的路径） |
| `type` | ✓ | `import` / `apk` / `live` / `server`（语义见上表） |
| `category` | | `env`（默认）/ `app`；未声明归 env |
| `icon` | | 图标地址（绝对 URL 或相对本索引的路径），未声明回落首字母占位 |
| `size` / `author` / `desc` / `tags` / `changelog` | | 展示元数据 |
| `md5` | | 包校验和（32 位 hex）；**声明即强制校验**，不符拒装防篡改。官方仓全量声明，本地包可用 `md5sum packages/<包名>` 复核 |
| `minApp` | | 可选；要求的最低 DsPlayer 版本，不满足时安装按钮置灰 |
| `pkg` | | 可选；**type=apk 专属**——应用包名。声明后客户端走通用包探测判定已安装（第三方插件零壳子改动接入的关键：不在 DsPlayer 内置插件注册表的 apk 条目必须声明，否则市场 UI 恒判「未安装」） |

## 发布约定（2026-09-20 起执行）

0. **发版闸门**：commit 前先跑 `python check_market.py`，六项全 PASS 才允许发布（退出码非零=拒绝）；红项即待修清单。
1. **同名包绝不重传**：内容有任何变化一律升版本号并换新文件名（如 `lx-sync-2.1.2.zip`），代理/CDN 层对同名文件的缓存会导致客户端「md5 校验不符」假失败（lx-sync 实锤）。旧版本包删除（git 历史留档）。
2. `md5` / `size` / `version` / `changelog` 与包严格同步；顶层 `updatedAt` 每次发布刷新。
3. `server` 条目包内 `server.json` 为安装指令，DsPlayer 安装时跳过落盘；`live` 条目包体即数据。
4. 图标换图时**换文件名**（如 `iptv.png`→`iptv2.png`），客户端图片磁盘缓存按 URL 键控。

## 自建市场

任意能放静态文件的地址（GitHub 仓库 / 对象存储 / 本地 sdcard）都可作市场：一份索引 JSON + 包文件即可。第三方条目的 `id` 须与包内 `plugin.json` 身份一致（`live`/`server` 条目除外：`live` 无插件身份，`server` 以 manifest 建服务），否则已装判定不闭环。
