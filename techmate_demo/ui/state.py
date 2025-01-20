import reflex as rx

from techmate_demo import navigation


class SideBarItemState(rx.State):
    # active_style: dict = {
    #     "opacity": "1",
    #     "background": "#FFFFFF1A",
    #     "border": "0.1em solid #FFFFFF1A",
    # }
    # disabled_style: dict = {
    #     "pointerEvents": "none",
    #     "color": "#FFFFFF40",
    #     "fill": "#FFFFFF40",
    # }
    # styles: list[dict] = [active_style, "", disabled_style]
    # active_index: int = 0

    @rx.event
    async def handleClick(self, index: int):
        # if (
        #     self.styles[index] != self.active_style
        #     and self.styles[index] != self.disabled_style
        # ):
        #     self.styles[self.active_index] = {}
        #     self.active_index = index
        #     self.styles[self.active_index] = {
        #         "opacity": "1",
        #         "background": "#FFFFFF1A",
        #         "border": "0.1em solid #FFFFFF1A",
        #     }
        route = await self.get_state(navigation.state.NavState)
        return rx.redirect(route.routes_dict[str(index)])
