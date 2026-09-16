# dsplayer-plugin

DsPlayer 插件官方市场仓库：`market.json` 为市场索引（在线安装入口），`packages/` 存放插件包。

## 使用

DsPlayer → 插件中心 → 市场 → 添加市场，填入本仓库索引直链：

```
https://raw.githubusercontent.com/hjdhnx/dsplayer-plugin/main/market.json
```

（国内可达性不佳时可换 jsdelivr 镜像：`https://cdn.jsdelivr.net/gh/hjdhnx/dsplayer-plugin@main/market.json`）

## 索引格式

见 `market.json` 与 DsPlayer 仓库 `docs/plugin/PLUGIN-MARKET-DESIGN.md` §二：

- `plugins[].id`：插件唯一身份（binary/runtime 插件 = 包内 plugin.json 的 `name`；内置引擎 = `mpv/py/qjs/fjs/agent`），与本地已装判定对齐
- `plugins[].type`：`import` = 应用内静默导入；`apk` = APK 直装（系统安装器）
- `plugins[].url`：绝对直链或相对本索引文件的相对路径
- `plugins[].sha256`：可选，声明后下载强制校验

## 自建市场

任意能放静态文件的地址（GitHub 仓库 / 对象存储 / 本地 sdcard）都可作市场：一份索引 JSON + 包文件即可。
