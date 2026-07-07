from AppKit import (
    NSViewMinYMargin,
    NSViewWidthSizable,
    NSMakePoint
)

#MARK: VLayout
class VLayout:
    """Vertical layout manager."""
    def __init__(self,margin_top=10,margin_left=10,spacing=8):
        self.container = None
        self.widgets = []
        self.margin_top = margin_top
        self.margin_left = margin_left
        self.spacing = spacing

    def attach(self,container):
        self.container = container
        self.relayout()

    def add_widget(self,widget):
        self.widgets.append(widget)
        self.container.content_view().addSubview_(widget.w)
        self.relayout()

    def relayout(self):
        if self.container is None:
            return

        view = self.container.content_view()
        y = view.frame().size.height-self.margin_top
        width = view.frame().size.width-self.margin_left*2

        for widget in self.widgets:
            height = widget.w.frame().size.height

            if hasattr(widget,"set_size"):
                widget.set_size(width,height)

            widget.w.setAutoresizingMask_(NSViewWidthSizable | NSViewMinYMargin)
            widget.w.setFrameOrigin_(NSMakePoint(self.margin_left,y-height))
            y -= height+self.spacing
            
#MARK: HLayout
class HLayout:
    """Horizontal layout manager."""
    def __init__(self,margin_top=10,margin_left=10,spacing=8):
        self.container = None
        self.widgets = []
        self.margin_top = margin_top
        self.margin_left = margin_left
        self.spacing = spacing

    def attach(self,container):
        self.container = container
        self.relayout()

    def add_widget(self,widget):
        self.widgets.append(widget)
        self.container.content_view().addSubview_(widget.w)
        self.relayout()

    def relayout(self):
        if self.container is None:
            return

        view = self.container.content_view()
        x = self.margin_left
        top = view.frame().size.height-self.margin_top

        for widget in self.widgets:
            wheight = widget.w.frame().size.height

            if hasattr(widget,"set_size"):
                widget.set_size(widget.w.frame().size.width,wheight)

            frame = widget.w.frame()
            widget.w.setAutoresizingMask_(NSViewMinYMargin)
            widget.w.setFrameOrigin_(NSMakePoint(x,top-frame.size.height))
            x += frame.size.width+self.spacing
