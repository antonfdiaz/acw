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
        self.alignment = None

    def attach(self,container):
        self.container = container
        self.relayout()

    def add_widget(self,widget):
        self.widgets.append(widget)
        self.container.content_view().addSubview_(widget.w)
        self.relayout()

    def set_alignment(self,alignment):
        if alignment not in ("left","center","right"):
            return
        self.alignment = alignment
        self.relayout()

    def relayout(self):
        if self.container is None:
            return

        view = self.container.content_view()
        y = view.frame().size.height-self.margin_top
        width = view.frame().size.width-self.margin_left*2

        for widget in self.widgets:
            height = widget.w.frame().size.height

            if hasattr(widget,"set_size") and self.alignment is None:
                widget.set_size(width,height)

            frame = widget.w.frame()
            if self.alignment == "center":
                x = self.margin_left+(width-frame.size.width)/2
            elif self.alignment == "right":
                x = self.margin_left+width-frame.size.width
            else:
                x = self.margin_left

            mask = NSViewMinYMargin
            if self.alignment is None:
                mask |= NSViewWidthSizable
            widget.w.setAutoresizingMask_(mask)
            widget.w.setFrameOrigin_(NSMakePoint(x,y-frame.size.height))
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
        self.alignment = "left"

    def attach(self,container):
        self.container = container
        self.relayout()

    def add_widget(self,widget):
        self.widgets.append(widget)
        self.container.content_view().addSubview_(widget.w)
        self.relayout()

    def set_alignment(self,alignment):
        if alignment not in ("left","center","right"):
            return
        self.alignment = alignment
        self.relayout()

    def relayout(self):
        if self.container is None:
            return

        view = self.container.content_view()
        top = view.frame().size.height-self.margin_top
        width = view.frame().size.width-self.margin_left*2
        total_width = sum(widget.w.frame().size.width for widget in self.widgets)
        if self.widgets:
            total_width += self.spacing*(len(self.widgets)-1)

        if self.alignment == "center":
            x = self.margin_left+(width-total_width)/2
        elif self.alignment == "right":
            x = self.margin_left+width-total_width
        else:
            x = self.margin_left

        for widget in self.widgets:
            wheight = widget.w.frame().size.height

            if hasattr(widget,"set_size"):
                widget.set_size(widget.w.frame().size.width,wheight)

            frame = widget.w.frame()
            widget.w.setAutoresizingMask_(NSViewMinYMargin)
            widget.w.setFrameOrigin_(NSMakePoint(x,top-frame.size.height))
            x += frame.size.width+self.spacing
