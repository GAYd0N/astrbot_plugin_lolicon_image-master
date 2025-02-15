from astrbot.api.message_components import *
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
import httpx
import json
import asyncio

@register("setu", "FateTrial", "一个发送随机涩图的插件", "2.0.0")
class SetuPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.r18 = 0
        self.cd = 10  # 默认冷却时间为 10 秒
        self.last_usage = {} # 存储每个用户上次使用指令的时间
        self.semaphore = asyncio.Semaphore(10)  # 限制并发请求数量为 10

    async def fetch_setu(self, msg: str):
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get("https://api.lolicon.app/setu/v2?r18=0&tag="+str(msg))
            resp.raise_for_status()
            return resp.json()
    async def fetch_taisele(self, msg: str):
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get("https://api.lolicon.app/setu/v2?r18=1&tag="+str(msg))
            resp.raise_for_status()
            return resp.json()

    @filter.command("setu")
    async def setu(self, event: AstrMessageEvent):
        user_id = event.get_sender_id()
        now = asyncio.get_event_loop().time()
        msg = event.message_str.replace("setu", "").strip()

        if user_id in self.last_usage and (now - self.last_usage[user_id]) < self.cd:
            remaining_time = self.cd - (now - self.last_usage[user_id])
            yield event.plain_result(f"冷却中，请等待 {remaining_time:.1f} 秒后重试。")
            return

        async with self.semaphore:  # 获取信号量，限制并发
            try:
                data = await self.fetch_setu(msg) # 使用单独的函数获取数据
                if data['data']:
                    image_pid = data['data'][0]['pid']
                    image_url = data['data'][0]['urls']['original']
                    # chain = [
                    #     At(qq=event.get_sender_id()),
                    #     Plain("pid:"+str(image_pid)),
                    #     Image.fromURL(image_url, size='small'),
                    # ]
                    node = Node(
                        uin=2901292139,
                        name="爱丽丝在网上就是跌",
                        content=[
                            Plain("pid:"+str(image_pid)),
                            Image.fromURL(image_url, size='small')
                        ]
                    )
                    yield event.chain_result([node])
                    self.last_usage[user_id] = now
                else:
                    yield event.plain_result("没有找到涩图。")
            except httpx.HTTPStatusError as e:
                yield event.plain_result(f"获取涩图时发生HTTP错误: {e.response.status_code}")
            except httpx.TimeoutException:
                yield event.plain_result("获取涩图超时，请稍后重试。")
            except httpx.HTTPError as e:
                yield event.plain_result(f"获取涩图时发生网络错误: {e}")
            except json.JSONDecodeError as e:
                yield event.plain_result(f"解析JSON时发生错误: {e}")
            except Exception as e:
                # self.context.logger.exception("Setu command error:") # 记录异常，方便调试
                yield event.plain_result(f"发生未知错误: {e}")

    @filter.command("taisele")
    async def taisele(self, event: AstrMessageEvent):
        if self.r18 == 0:
            yield event.plain_result("🔞禁止涩涩")
            return
        user_id = event.get_sender_id()
        now = asyncio.get_event_loop().time()
        msg = event.message_str.replace("taisele", "").strip()
        if user_id in self.last_usage and (now - self.last_usage[user_id]) < self.cd:
            remaining_time = self.cd - (now - self.last_usage[user_id])
            yield event.plain_result(f"冷却中，请等待 {remaining_time:.1f} 秒后重试。")
            return

        async with self.semaphore:  # 获取信号量，限制并发
            try:
                data = await self.fetch_taisele(msg) # 使用单独的函数获取数据
                if data['data']:
                    image_pid = data['data'][0]['pid']
                    image_url = data['data'][0]['urls']['original']
                    # chain = [
                    #     At(qq=event.get_sender_id()),
                    #     Plain("pid:"+str(image_pid)),
                    #     Image.fromURL(image_url, size='small'),
                    # ]
                    node = Node(
                        uin=2901292139,
                        name="爱丽丝在网上就是跌",
                        content=[
                            Plain("pid:"+str(image_pid)),
                            Image.fromURL(image_url, size='small')
                        ]
                    )
                    yield event.chain_result([node])
                    self.last_usage[user_id] = now
                else:
                    yield event.plain_result("没有找到涩图。")
            except httpx.HTTPStatusError as e:
                yield event.plain_result(f"获取涩图时发生HTTP错误: {e.response.status_code}")
            except httpx.TimeoutException:
                yield event.plain_result("获取涩图超时，请稍后重试。")
            except httpx.HTTPError as e:
                yield event.plain_result(f"获取涩图时发生网络错误: {e}")
            except json.JSONDecodeError as e:
                yield event.plain_result(f"解析JSON时发生错误: {e}")
            except Exception as e:
                # self.context.logger.exception("Setu command error:") # 记录异常，方便调试
                yield event.plain_result(f"发生未知错误: {e}")


    @filter.command("setucd")
    async def set_setu_cd(self, event: AstrMessageEvent, cd: int):
        if cd <= 0:
            yield event.plain_result("冷却时间必须大于 0。")
            return
        self.cd = cd
        yield event.plain_result(f"涩图指令冷却时间已设置为 {cd} 秒。")

    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("r18")
    async def test(self, event: AstrMessageEvent, status: int):
        if status > 0:
            self.r18 = 1
            yield event.plain_result("taisele")
        if status == 0:
            self.r18 = 0
            yield event.plain_result("🔞禁止涩涩")

    @filter.command("setu_help")
    async def setu_help(self, event: AstrMessageEvent):
        help_text = """
        **涩图插件帮助**

        **可用命令:**
        - `/setu`: 发送一张随机涩图。
        - `/taisele`: 发送一张随机R18涩图。
        - `/setucd <冷却时间>`: 设置涩图指令的冷却时间（秒）。
        - `/setu_help`: 显示此帮助信息。

        **使用方法:**
        - 直接发送 `/setu` 即可获取一张随机涩图。
        - 直接发送 `/taisele` 即可获取一张随机R18涩图。
        - 使用 `/setucd 15` 将冷却时间设置为 15 秒。

        **注意:**
        - 涩图图片大小为 small。
        - 冷却时间默认为 10 秒。
        """
        yield event.plain_result(help_text)