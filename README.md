# setu

基于原作者插件进行修改！原作者仓库链接：[astrbot_plugin_lolicon_image-master](https://github.com/rikkamiss/astrbot_plugin_lolicon_image)

*修改说明:**
1.  **导入 `asyncio`:** 用于获取当前时间。
2.  **添加 `self.cd` 和 `self.last_usage`:**
    *   `self.cd`: 存储冷却时间，默认为 10 秒。
    *   `self.last_usage`: 字典，存储每个用户上次使用 `/setu` 指令的时间。
3.  **修改 `setu` 方法:**
    *   获取当前时间 `now`。
    *   检查用户是否在冷却时间内。如果在冷却时间内，回复剩余时间并返回。
    *   如果不在冷却时间内，执行原有的涩图获取逻辑，并在成功发送图片后更新 `last_usage`。
4.  **添加 `setucd` 指令:**
    *   `@filter.command("setucd")` 注册 `setucd` 指令，用于设置冷却时间。
    *   `async def set_setu_cd(self, event: AstrMessageEvent, cd: int)`:  接收用户输入的冷却时间 `cd`。
    *   检查 `cd` 是否大于 0，如果不是则返回错误消息。
    *   更新 `self.cd` 的值，并返回设置成功的消息
5.  **添加 `setu_help` 指令:**
    *   `@filter.command("setu_help")` 注册 `setu_help` 指令。
    *   `async def setu_help(self, event: AstrMessageEvent)`:  定义 `setu_help` 方法。
    *   `help_text`: 包含插件的使用说明、可用命令和注意事项的文本。
    *   使用 `yield event.plain_result(help_text)` 发送帮助文本。
6. **添加 `taisele` 指令:**
   * 基于原作者的setu插件进行功能升级，使机器人可以发送R18图片
7. **添加 `setur18` 指令:**
   * 设置是否允许发送R18图片，仅机器人管理员可用

**使用方法:**
1.  重新加载或重启你的 AstrBot 插件。
4.  使用  `/setu_help`获取使用帮助
2.  使用 `/setu` 指令，你会受到冷却时间限制。
3.  使用 `/taisele` 指令，你会受到冷却时间限制。
4.  使用 `/setucd <冷却时间>` (例如 `/setucd 30`) 设置冷却时间，单位为秒。
# 支持

[帮助文档](https://astrbot.soulter.top/center/docs/%E5%BC%80%E5%8F%91/%E6%8F%92%E4%BB%B6%E5%BC%80%E5%8F%91/
)
