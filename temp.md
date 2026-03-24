## 🎉 EasyMate v2.4.0 - [Everything to Text](https://zhida.zhihu.com/search?content_id=271839857&content_type=Article&match_order=1&q=Everything+to+Text&zhida_source=entity) 重磅发布！

**让 AI 真正看懂世界，从「能说」到「能看」的跨越！**

经过近一个月的迭代，[EasyMate 终于迎来了 v2.4.0 版本](https://link.zhihu.com/?target=https%3A//github.com/MateUnion/EasyMate)——**Everything to Text**。这是继 v2.0.0「GUI Awakening」之后，EasyMate 的又一次里程碑式跃迁。从现在起，你的 AI 伙伴不仅能听懂你的话，还能**看懂图片、视频、Word、Excel、PDF……一切都能变成它理解的语言**。

### ✨ 核心亮点：[多模态理解](https://zhida.zhihu.com/search?content_id=271839857&content_type=Article&match_order=1&q=%E5%A4%9A%E6%A8%A1%E6%80%81%E7%90%86%E8%A7%A3&zhida_source=entity)（ETT）

- 🖼️ **图片理解**：上传一张照片，AI 能描述内容、识别物体、分析场景。
- 🎥 **视频分析**：给一个短视频，AI 能总结关键信息、描述画面变化。
- 📄 **文档解析**：Word、Excel、PDF 直接丢给 AI，它会提取文字、表格、要点，秒变“文档总结器”。
- 🛠️ **零门槛使用**：工具 `ett` 已内置，只需在聊天中发送文件或链接，AI 自动调用，无需手动干预。
- 🔐 **安全可控**：支持自定义 API 密钥（智谱 GLM-4.6V-Flash），可单独配置超时、重试次数，应对高峰时段。

**示例对话**：

```text
用户：这张图里有什么？C:\pics\cat.jpg
AI：调用 ett 工具… 图片中是一只橘猫在阳光下打盹，旁边有一盆绿萝。
```

### 🧩 完美融入现有工具箱

- 与 `read`、`write`、`search`、`command` 等工具无缝协作。
- 支持公网 URL 或本地文件，自动 base64 编码，大文件有友好提示。
- 可在 `config.json` 中为 `ett` 单独配置 `api_key`、`model`、`max_retries`，灵活适配不同模型。

### 🚀 从「看懂」到「创造」：v3.0.0 预告

v2.4.0 让 EasyMate 装上了“眼睛”，而下一站——**v3.0.0 - From Words to Worlds**，我们将为它装上“双手”！

通过即将到来的 **MCP（Model Context Protocol）集成**，EasyMate 将能调用任何支持 [MCP 协议](https://zhida.zhihu.com/search?content_id=271839857&content_type=Article&match_order=1&q=+MCP+%E5%8D%8F%E8%AE%AE&zhida_source=entity)的工具：截图、操控鼠标键盘、控制浏览器、甚至连接智能硬件……一切皆有可能。

届时，你只需要在 `config.json` 里加一行配置，EasyMate 就能瞬间获得无限能力。从文字到世界，只隔着一个协议！

### 📜 版本故事线

- **v1.0.0 - Source of All**：万物之源，EasyMate 的诞生。
- **v2.0.0 - GUI Awakening**：界面觉醒，从命令行走向可视化交互。
- **v2.4.0 - Everything to Text**：看懂万物，让 AI 真正理解世界。
- **v3.0.0 - From Words to Worlds**：连接世界，让 AI 操控万物。（即将到来）

### 🙏 致谢

感谢所有使用 EasyMate 的朋友，你们的每一次反馈都是我们前进的动力。特别感谢：

- [MateUnion](https://link.zhihu.com/?target=https%3A//github.com/MateUnion) 团队的伙伴们
- [xhdlphzr](https://link.zhihu.com/?target=https%3A//github.com/xhdlphzr)（就是我自己，一个爱折腾的初中生）
- [zhiziwj](https://link.zhihu.com/?target=https%3A//github.com/zhiziwj) 和 [humanity687](https://link.zhihu.com/?target=https%3A//github.com/humanity687) 的宝贵建议

### 🚀 立即体验

```text
git clone https://github.com/MateUnion/EasyMate.git
cd EasyMate
# 双击 start.bat (Windows) 或 ./start.sh (macOS)
# 在 config.json 中配置智谱 API 密钥
# 开始聊天，发送文件或链接，AI 自动分析！
```

从 **Everything to Text** 到 **From Words to Worlds**，我们正一步步让 AI 成为你真正可靠的伙伴。未来已来，你来见证！

---

🎉 **祝贺 EasyMate v2.4.0 发布！**  
🌟 如果你喜欢这个项目，请给 GitHub 仓库点个 Star，让更多人看到它！  
💬 目前其实有挺多待修复的问题，也是我们一周内比较简陋的成果，有任何问题或建议，欢迎提 Issue 或加入讨论。
