# DeepSeek 联网搜索

YueLiBot 的外部工具插件。对方让她查资料，或者回答依赖近期、尚不确定的公开事实时，她可以调用
`deepseek_search`，通过 [DeepSeek Search API](https://api-docs.deepseek.com/guides/search)
取得网页的标题、来源、发布日期和摘要。结果只作为外部观察交给决策与回复生成，不直接发送消息，
也不打开结果里的链接。闲聊、群友私事与已知常识不需要搜索。

查询词会发给 DeepSeek，请勿把私人信息写入查询词；工具说明已要求她只写话题关键词。

## 安装

- **插件商店**：在 [月璃插件商店](https://plugins.yuelibot.org/plugins/akari.deepseek-search/)
  点「一键安装」，在管理面板确认后重启。
- **手动安装**：下载商店页上的 ZIP，解压到月璃目录下的 `plugins/`，得到
  `plugins/akari.deepseek-search/plugin.py`，然后重启。

本版声明支持主程序 0.2.0～0.2.5。更新的主程序会按兼容模式加载，并在启动日志中提示一次。

## 配置

第一次启动后，主程序会在插件目录生成 `config.toml`，也可以在管理面板「工具与 MCP」页修改。

| 字段 | 含义 | 默认值 |
| :--- | :--- | :--- |
| `api_key` | DeepSeek API 密钥；留空时工具不会出现在可选项里 | 空 |
| `base_url` | 接口根地址，不含 `/v1/tools/search`；经中转服务访问时改成中转地址 | `https://api.deepseek.com` |
| `daily_limit` | 服务器本地日期内最多发出的搜索请求数，1～1000，失败也计数 | `50` |

```toml
[plugin]
enabled = true
api_key = "填你的 DeepSeek 密钥"
daily_limit = 50
```

密钥字段在管理面板中隐藏，留空保存会保留原值。密钥不会出现在日志、错误信息和观察文本里。

同一个查询词 10 分钟内重复搜索时直接使用缓存，不计入日上限，也不产生费用。日计数在重启后清零。

## 费用

Search API 按成功请求计费：返回空结果、请求失败和超时都不计费，每次固定取 5 条结果，条数不影响价格。
具体单价以 [DeepSeek 官方文档](https://api-docs.deepseek.com/guides/search) 为准。
DeepSeek 对部分客户端的限时免费不适用于本插件，本插件直接调用接口，按正常价格计费。

## 搜索写法

工具说明会引导她在查询词里使用 DeepSeek 支持的限定写法：

| 写法 | 作用 |
| :--- | :--- |
| `after:2026-10-01` | 只要这个日期之后发布的网页 |
| `site:github.com` | 只搜某个网站 |
| `"完整短语"` | 精确匹配短语 |

查询词去首尾空白后最长 100 字。

## 出错时

失败原因会原样交给她，不会变成「没搜到」：

| 现象 | 原因 |
| :--- | :--- |
| HTTP 401 | 密钥无效 |
| HTTP 402 | DeepSeek 账户余额不足 |
| HTTP 429 | 请求太频繁 |
| 超过 8 秒没有响应 | 网络或 DeepSeek 服务较慢；主程序配置了代理时会经代理访问 |

## 许可证

AGPL-3.0-only，见 [LICENSE](LICENSE)。
