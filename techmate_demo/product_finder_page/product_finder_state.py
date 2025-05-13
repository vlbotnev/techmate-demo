import reflex as rx
import asyncio
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
import sys
from pathlib import Path
from datetime import datetime, timezone

# Добавляем путь до thrift интерфейсов
file = __file__
thrift_interface_path = str(
    Path(file).resolve().parent.parent.parent.parent
    / "hack-april"
    / "backend_server"
    / "interface"
    / "gen-py"
)
sys.path.append(thrift_interface_path)

from wizium_backend import LLMService  # noqa: E402
from wizium_backend.LLMService import CreateAnalysisRequest  # noqa: E402
from wizium_backend.ttypes import (  # noqa: E402
    GetLastStateRequest,
    State as ThriftState,
    StatesEnum,
    Product,
)


class ProductFinderState(rx.State):
    processing: bool = False
    keyword: str = "baby toys"
    num_niche_to_find: int = 3
    num_products_per_niche: int = 3
    num_products_to_analyse: int = 20
    message: str = ""

    @rx.event
    def set_keyword(self, keyword: str):
        """Вызывается при изменении поля keyword."""
        self.keyword = str(keyword)

    @rx.event
    def set_num_niches(self, num_niches: int):
        """Вызывается при изменении количества ниш."""
        self.num_niche_to_find = int(num_niches)

    @rx.event
    def set_num_products(self, num_products: int):
        """Вызывается при изменении количества продуктов на нишу."""
        self.num_products_per_niche = int(num_products)

    @rx.event
    def set_num_to_analyse(self, num_to_analyse: int):
        """Вызывается при изменении общего числа продуктов для анализа."""
        self.num_products_to_analyse = int(num_to_analyse)

    def get_product_string(self, product: Product) -> str:
        lines = [f"**{product.product_name}**"]  # Сделаем заголовок жирным

        if product.asin:
            lines.append(f"- **ASIN:** {product.asin}")

        url = product.product_url or (
            f"https://www.amazon.com/dp/{product.asin}" if product.asin else None
        )
        if url:
            lines.append(f"- [Amazon Link]({url})")

        if product.product_score:
            lines.append(f"- **Score:** {product.product_score}")

        if product.price:
            currency = product.price_currency or ""
            lines.append(f"- **Price:** {product.price} {currency}")

        if product.rating:
            lines.append(f"- **Rating:** {product.rating}")

        if product.reviews_summary:
            lines.append(f"- **Reviews:** {product.reviews_summary}")

        if product.product_desc:
            lines.append(f"- **Description:** {product.product_desc}")

        return "\n".join(lines) + "\n\n"

    def get_markdown_from_state(
        self, state: ThriftState, update_datetime: str = ""
    ) -> str:
        intro = (
            f"Update at {datetime.fromisoformat(update_datetime).strftime('%Y-%m-%d %H:%M:%S')}:\n\n"
            if update_datetime
            else "Final results:\n\n"
        )
        lines = []
        for i, niche in enumerate(state.niches or [], 1):  # начинаем с 1
            header = f"### {i}: {niche.keyword}"
            prods = "\n".join(self.get_product_string(p) for p in niche.products or [])
            lines.append(f"{header}\n\n{prods}")
        return intro + "\n".join(lines)

    @rx.background
    async def generating_result(self):
        async with self:
            self.processing = True
            self.message = "Analysis starting..."
        transport = TSocket.TSocket("10.88.88.90", 9099)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = LLMService.Client(protocol)
        transport.open()

        req = CreateAnalysisRequest(
            keyword=self.keyword,
            num_niche_to_find=self.num_niche_to_find,
            num_products_per_niche=self.num_products_per_niche,
            num_keywords_to_analyse=4,
            num_products_to_analyse=self.num_products_to_analyse,
        )
        resp = client.createAnalysis(req)
        analysis_id = resp.analysis_id
        transport.close()
        print("Analysis Created id", analysis_id)
        last_time_check = datetime.now(timezone.utc).isoformat()

        while True:
            print(self.message)
            await asyncio.sleep(10)
            transport.open()
            state_resp = client.getLastState(
                GetLastStateRequest(analysis_id, last_time_check)
            )
            transport.close()

            thrift_state = state_resp.state
            if thrift_state:
                last_time = datetime.now(timezone.utc).isoformat()
                async with self:
                    self.message = self.get_markdown_from_state(thrift_state, last_time)

            if thrift_state and thrift_state.stage == StatesEnum.DONE:
                break

        async with self:
            self.processing = False
            self.message = self.get_markdown_from_state(thrift_state)
