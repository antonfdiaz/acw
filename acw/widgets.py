import objc
from AppKit import (
    NSApp,
    NSApplication,
    NSApplicationActivationPolicyRegular,
    NSBackingStoreBuffered,
    NSMakeRect,
    NSTitledWindowMask,
    NSClosableWindowMask,
    NSMiniaturizableWindowMask,
    NSResizableWindowMask,
    NSWindow,
    NSTextField,
    NSButton,
    NSTextView,
    NSScrollView,
    NSTableView,
    NSTableColumn,
    NSColor,
    NSFont,
    NSForegroundColorAttributeName,
    NSViewWidthSizable,
    NSView,
    NSImageView,
    NSImage,
    NSImageLeft,
    NSImageRight,
    NSImageAbove,
    NSImageBelow,
)
from objc import super
from Foundation import NSObject,NSMakePoint,NSMutableAttributedString

#MARK: Widget
class Widget:
    """Base class for all widgets."""
    def __init__(self):
        self.layout = None
        self.custom_text_color = False
        self._setting_inherited_text_color = False

    def content_view(self):
        return self.w

    def set_layout(self,layout):
        self.layout = layout
        self.layout.attach(self)

    def add_widget(self,widget):
        if self.layout is None:
            self.content_view().addSubview_(widget.w)
        else:
            self.layout.add_widget(widget)

    def relayout(self):
        if self.layout is not None:
            self.layout.relayout()

    def apply_inherited_text_color(self,color):
        if hasattr(self,"set_text_color"):
            self._setting_inherited_text_color = True
            self.set_text_color(color)
            self._setting_inherited_text_color = False

    def mark_custom_text_color(self):
        if not self._setting_inherited_text_color:
            self.custom_text_color = True

#MARK: Window
class Window(Widget):
    def __init__(self):
        Widget.__init__(self)
        self.widgets = []
        self.text_color = None
        with objc.autorelease_pool():
            NSApplication.sharedApplication()
            NSApp.setActivationPolicy_(NSApplicationActivationPolicyRegular)
            
            style = (
                NSTitledWindowMask |
                NSClosableWindowMask |
                NSMiniaturizableWindowMask |
                NSResizableWindowMask
            )
            
            self.width = 200
            self.height = 200

            self.window = (
                NSWindow.alloc()
                .initWithContentRect_styleMask_backing_defer_(
                    NSMakeRect(0,0,self.width,self.height),
                    style,
                    NSBackingStoreBuffered,
                    False,
                )
                .autorelease()
            )
            self.window.cascadeTopLeftFromPoint_(NSMakePoint(20,20))
            self.window.makeKeyAndOrderFront_(None)
            
    def titlebar_hidden(self,hidden=True):
        self.window.setTitleVisibility_(2 if hidden else 0)
        self.window.setTitlebarAppearsTransparent_(hidden)

    def content_view(self):
        return self.window.contentView()

    def add_widget(self,widget):
        self.widgets.append(widget)
        Widget.add_widget(self,widget)
        if self.text_color is not None and not widget.custom_text_color:
            widget.apply_inherited_text_color(self.text_color)
            
    def set_title(self,title):
        self.window.setTitle_(title)
        
    def close_btn_disabled(self,hidden=True):
        self.window.setStyleMask_(self.window.styleMask() & ~NSClosableWindowMask if hidden else self.window.styleMask() | NSClosableWindowMask)
        
    def minimize_btn_disabled(self,hidden=True):
        self.window.setStyleMask_(self.window.styleMask() & ~NSMiniaturizableWindowMask if hidden else self.window.styleMask() | NSMiniaturizableWindowMask)
        
    def maximize_btn_disabled(self,hidden=True):
        self.window.setStyleMask_(self.window.styleMask() & ~NSResizableWindowMask if hidden else self.window.styleMask() | NSResizableWindowMask)

    def run(self):
        NSApp.activateIgnoringOtherApps_(True)
        NSApp.run()
        
    def set_size(self,width,height):
        self.width = width
        self.height = height
        self.window.setContentSize_((width,height))
        self.relayout()
        
    def set_background_color(self,color):
        color = NSColor.colorWithCalibratedRed_green_blue_alpha_(int(color[1:3],16)/255.0,int(color[3:5],16)/255.0,int(color[5:7],16)/255.0,1.0)
        self.window.setBackgroundColor_(color)
        self.content_view().setNeedsDisplay_(True)
        
    def set_text_color(self,color):
        self.text_color = color
        for widget in self.widgets:
            if not widget.custom_text_color:
                widget.apply_inherited_text_color(color)
                
    def set_dock_icon(self,image_path):
        image = NSImage.alloc().initByReferencingFile_(image_path)
        NSApp.setApplicationIconImage_(image)
    
#MARK: Label    
class Label(Widget):
    def __init__(self,text):
        Widget.__init__(self)
        self.w = (
            NSTextField.alloc()
            .initWithFrame_(NSMakeRect(0,0,160,20))
            .autorelease()
        )
        self.w.setStringValue_(text)
        self.w.setBezeled_(False)
        self.w.setDrawsBackground_(False)
        self.w.setEditable_(False)
        self.w.setSelectable_(False)
        
    def set_text(self,text):
        self.w.setStringValue_(text)
        
    def set_size(self,width,height):
        self.w.setFrameSize_((width,height))
        self.relayout()
        
    def set_text_color(self,color):
        self.mark_custom_text_color()
        color = NSColor.colorWithCalibratedRed_green_blue_alpha_(int(color[1:3],16)/255.0,int(color[3:5],16)/255.0,int(color[5:7],16)/255.0,1.0)
        self.w.setTextColor_(color)
        self.w.setNeedsDisplay_(True)
        
    def set_font(self,font):
        if isinstance(font,tuple) and len(font) == 2:
            font = NSFont.fontWithName_size_(font[0],font[1])
        if font is not None:
            self.w.setFont_(font)
            self.w.setNeedsDisplay_(True)
   
#MARK: TextField     
class TextField(Widget):
    def __init__(self,text="",placeholder=""):
        Widget.__init__(self)
        self.w = (
            NSTextField.alloc()
            .initWithFrame_(NSMakeRect(0,0,160,20))
            .autorelease()
        )
        self.w.setPlaceholderString_(placeholder)
        self.w.setStringValue_(text)
    
    def get_text(self):
        return self.w.stringValue()
    
    def set_text(self,text):
        self.w.setStringValue_(text)
        
    def set_placeholder(self,placeholder):
        self.w.setPlaceholderString_(placeholder)
        
    def set_size(self,width,height):
        self.w.setFrameSize_((width,height))
        self.relayout()
        
    def set_background_color(self,color):
        color = NSColor.colorWithCalibratedRed_green_blue_alpha_(int(color[1:3],16)/255.0,int(color[3:5],16)/255.0,int(color[5:7],16)/255.0,1.0)
        self.w.setBackgroundColor_(color)
        self.w.setNeedsDisplay_(True)
        
    def set_text_color(self,color):
        self.mark_custom_text_color()
        color = NSColor.colorWithCalibratedRed_green_blue_alpha_(int(color[1:3],16)/255.0,int(color[3:5],16)/255.0,int(color[5:7],16)/255.0,1.0)
        self.w.setTextColor_(color)
        self.w.setNeedsDisplay_(True)
        
    def set_bezeled(self,bezeled=True):
        self.w.setBezeled_(bezeled)
        self.w.setNeedsDisplay_(True)
        
    def set_font(self,font):
        if isinstance(font,tuple) and len(font) == 2:
            font = NSFont.fontWithName_size_(font[0],font[1])
        if font is not None:
            self.w.setFont_(font)
            self.w.setNeedsDisplay_(True)
        
#MARK: TextArea
class TextArea(Widget):
    def __init__(self,text="",placeholder=""):
        Widget.__init__(self)
        self.w = (
            NSScrollView.alloc()
            .initWithFrame_(NSMakeRect(0,0,160,80))
            .autorelease()
        )
        self.w.setHasVerticalScroller_(True)
        self.tv = (
            NSTextView.alloc()
            .initWithFrame_(NSMakeRect(0,0,160,80))
            .autorelease()
        )
        self.tv.setAutoresizingMask_(NSViewWidthSizable)
        self.w.setDocumentView_(self.tv)
        self.tv.setPlaceholderString_(placeholder)
        self.tv.setString_(text)
        self.tv.setEditable_(True)
    
    def get_text(self):
        return self.tv.string()
    
    def set_text(self,text):
        self.tv.setString_(text)

    def append_text(self,text):
        current_text = self.tv.string()
        self.tv.setString_(current_text+text)
        self.tv.scrollRangeToVisible_((len(current_text)+len(text),0))

    def clear_text(self):
        self.tv.setString_("")

    def set_editable(self,editable=True):
        self.tv.setEditable_(editable)
        
    def set_placeholder(self,placeholder):
        self.tv.setPlaceholderString_(placeholder)
        
    def show_scrollbar(self,show=True):
        self.w.setHasVerticalScroller_(show)
        
    def set_size(self,width,height):
        self.w.setFrameSize_((width,height))
        self.tv.setFrameSize_((width,height))
        self.relayout()
        
    def set_background_color(self,color):
        color = NSColor.colorWithCalibratedRed_green_blue_alpha_(int(color[1:3],16)/255.0,int(color[3:5],16)/255.0,int(color[5:7],16)/255.0,1.0)
        self.tv.setBackgroundColor_(color)
        self.tv.setNeedsDisplay_(True)
        
    def set_text_color(self,color):
        self.mark_custom_text_color()
        color = NSColor.colorWithCalibratedRed_green_blue_alpha_(int(color[1:3],16)/255.0,int(color[3:5],16)/255.0,int(color[5:7],16)/255.0,1.0)
        self.tv.setTextColor_(color)
        self.tv.setNeedsDisplay_(True)
        
    def set_bezeled(self,bezeled=True):
        self.tv.setBezeled_(bezeled)
        self.tv.setNeedsDisplay_(True)
        
    def set_font(self,font):
        if isinstance(font,tuple) and len(font) == 2:
            font = NSFont.fontWithName_size_(font[0],font[1])
        if font is not None:
            self.tv.setFont_(font)
            self.tv.setNeedsDisplay_(True)
        
#MARK: Button
class Button(Widget):
    def __init__(self,text,callback):
        Widget.__init__(self)
        self.text_color = None
        self.icon_aspect_ratio = None
        self.w = (
            NSButton.alloc()
            .initWithFrame_(NSMakeRect(0,0,160,20))
            .autorelease()
        )
        self.w.setTitle_(text)
        self.w.setTarget_(self)
        self.w.setAction_("button_clicked:")
        self.callback = callback
        
    def button_clicked_(self,sender):
        if callable(self.callback):
            self.callback()
            
    def set_text(self,text):
        self.w.setTitle_(text)
        if self.text_color is not None:
            self.set_text_color(self.text_color)
        
    def set_callback(self,callback):
        self.callback = callback
        
    def set_enabled(self,enabled):
        self.w.setEnabled_(enabled)

    def set_size(self,width,height):
        self.w.setFrameSize_((width,height))
        if self.icon_aspect_ratio is not None:
            self.w.image().setSize_((height*self.icon_aspect_ratio,height))
        self.relayout()
        
    def set_bezel_color(self,color):
        color = NSColor.colorWithCalibratedRed_green_blue_alpha_(int(color[1:3],16)/255.0,int(color[3:5],16)/255.0,int(color[5:7],16)/255.0,1.0)
        self.w.setBezelColor_(color)
        self.w.setNeedsDisplay_(True)
        
    def set_font(self,font):
        if isinstance(font,tuple) and len(font) == 2:
            font = NSFont.fontWithName_size_(font[0],font[1])
        if font is not None:
            self.w.setFont_(font)
            self.w.setNeedsDisplay_(True)
            
    def set_text_color(self,color):
        self.mark_custom_text_color()
        self.text_color = color
        color = NSColor.colorWithCalibratedRed_green_blue_alpha_(int(color[1:3],16)/255.0,int(color[3:5],16)/255.0,int(color[5:7],16)/255.0,1.0)
        title = NSMutableAttributedString.alloc().initWithAttributedString_(self.w.attributedTitle())
        title.addAttribute_value_range_(NSForegroundColorAttributeName,color,(0,len(self.w.title())))
        self.w.setAttributedTitle_(title)
        self.w.setNeedsDisplay_(True)
        
    def set_icon(self,image_path,alignment="left"):
        image = NSImage.alloc().initByReferencingFile_(image_path)
        image_size = image.size()
        self.icon_aspect_ratio = image_size.width/image_size.height
        height = self.w.frame().size.height
        image.setSize_((height*self.icon_aspect_ratio,height))
        self.w.setImage_(image)
        if alignment == "left":
            self.w.setImagePosition_(NSImageLeft)
        elif alignment == "right":
            self.w.setImagePosition_(NSImageRight)
        self.w.setNeedsDisplay_(True)

def get_text(tf):
    print("TextField value:",tf.get_text())
    
class ImageButton(Button):
    def __init__(self,image_path,callback):
        Widget.__init__(self)
        self.text_color = None
        self.w = (
            NSButton.alloc()
            .initWithFrame_(NSMakeRect(0,0,160,20))
            .autorelease()
        )
        image = NSImage.alloc().initByReferencingFile_(image_path)
        self.w.setImage_(image)
        self.w.setBordered_(False)
        self.w.setTarget_(self)
        self.w.setAction_("button_clicked:")
        self.callback = callback

    def set_size(self,width,height):
        self.w.setFrameSize_((width,height))
        image = self.w.image()
        if image is not None:
            image.setSize_((width,height))
        self.relayout()

    def set_image(self,image_path):
        image = NSImage.alloc().initByReferencingFile_(image_path)
        image.setSize_(self.w.frame().size)
        self.w.setImage_(image)
        self.w.setNeedsDisplay_(True)

#MARK: Table
class Table(NSObject, Widget):
    def initWithColumns_(self,columns):
        self = objc.super(Table,self).init()
        if self is None:
            return None
        Widget.__init__(self)

        self.columns = list(columns)
        self.rows = []

        #create scroll view
        self.w = (
            NSScrollView.alloc()
            .initWithFrame_(NSMakeRect(0,0,180,170))
            .autorelease()
        )
        self.w.setHasVerticalScroller_(True)

        #create table view
        self.table = (
            NSTableView.alloc()
            .initWithFrame_(NSMakeRect(0,0,180,170))
            .autorelease()
        )

        self.table.setDataSource_(self)
        self.w.setDocumentView_(self.table) #wrap table in scroll view

        for col in self.columns:
            column = NSTableColumn.alloc().initWithIdentifier_(col)
            column.setTitle_(col)
            self.table.addTableColumn_(column)

        return self

    @objc.python_method
    def set_size(self,width,height):
        self.w.setFrameSize_((width,height))
        self.table.setFrameSize_((width,height))
        self.relayout()

    @objc.python_method
    def add_row(self,row_data):
        self.rows.append(list(row_data))
        self.table.reloadData()

    @objc.python_method
    def clear_rows(self):
        self.rows.clear()
        self.table.reloadData()

    @objc.python_method
    def set_multi_selection(self,enabled):
        if enabled:
            self.table.setAllowsMultipleSelection_(True)
        else:
            self.table.setAllowsMultipleSelection_(False)

    @objc.python_method
    def get_selected(self):
        selected_indexes = self.table.selectedRowIndexes()
        return [self.rows[i] for i in range(len(self.rows)) if selected_indexes.containsIndex_(i)]

    @objc.python_method
    def deselect_all(self):
        self.table.deselectAll_(None)

    @objc.python_method
    def set_background_color(self,color):
        color = NSColor.colorWithCalibratedRed_green_blue_alpha_(int(color[1:3],16)/255.0,int(color[3:5],16)/255.0,int(color[5:7],16)/255.0,1.0)
        self.table.setBackgroundColor_(color)
        self.table.setNeedsDisplay_(True)

    @objc.python_method
    def set_text_color(self,color):
        self.mark_custom_text_color()
        color = NSColor.colorWithCalibratedRed_green_blue_alpha_(int(color[1:3],16)/255.0,int(color[3:5],16)/255.0,int(color[5:7],16)/255.0,1.0)
        for column in self.table.tableColumns():
            column.dataCell().setTextColor_(color)
        self.table.setNeedsDisplay_(True)

    @objc.python_method
    def set_font(self,font):
        if isinstance(font,tuple) and len(font) == 2:
            font = NSFont.fontWithName_size_(font[0],font[1])
        if font is not None:
            for column in self.table.tableColumns():
                column.dataCell().setFont_(font)
            self.table.setNeedsDisplay_(True)

    def numberOfRowsInTableView_(self,tableView):
        return len(self.rows)

    def tableView_objectValueForTableColumn_row_(self,tableView,tableColumn,row):
        col_index = self.table.tableColumns().indexOfObject_(tableColumn)
        if row < len(self.rows) and col_index < len(self.rows[row]):
            return str(self.rows[row][col_index])
        return ""
    
    @objc.python_method
    def show_scrollbar(self,show=True):
        self.w.setHasVerticalScroller_(show)
    
#MARK: List
class List(NSObject, Widget):
    def init(self):
        self = super().init()
        if self is None:
            return None
        Widget.__init__(self)

        self.rows = []

        self.w = (
            NSScrollView.alloc()
            .initWithFrame_(NSMakeRect(0,0,180,170))
            .autorelease()
        )
        self.w.setHasVerticalScroller_(True)

        self.table = (
            NSTableView.alloc()
            .initWithFrame_(NSMakeRect(0,0,180,170))
            .autorelease()
        )

        self.table.setDataSource_(self)
        self.table.setDelegate_(self)
        self.table.setHeaderView_(None)
        self.w.setDocumentView_(self.table)

        column = NSTableColumn.alloc().initWithIdentifier_("main")
        column.setTitle_("Items")
        self.table.addTableColumn_(column)
        self.selection_callback = None

        return self

    @objc.python_method
    def set_size(self,width,height):
        self.w.setFrameSize_((width,height))
        self.table.setFrameSize_((width,height))
        self.relayout()

    @objc.python_method
    def add_row(self,text):
        self.rows.append(str(text))
        self.table.reloadData()
        
    @objc.python_method
    def clear_rows(self):
        self.rows.clear()
        self.table.reloadData()
        
    @objc.python_method
    def set_multi_selection(self,enabled):
        if enabled:
            self.table.setAllowsMultipleSelection_(True)
        else:
            self.table.setAllowsMultipleSelection_(False)
            
    @objc.python_method
    def get_selected(self):
        selected_indexes = self.table.selectedRowIndexes()
        return [self.rows[i] for i in range(len(self.rows)) if selected_indexes.containsIndex_(i)]

    @objc.python_method
    def get_selected_indexes(self):
        selected_indexes = self.table.selectedRowIndexes()
        return [i for i in range(len(self.rows)) if selected_indexes.containsIndex_(i)]

    @objc.python_method
    def set_on_selection_change(self,callback):
        self.selection_callback = callback
    
    @objc.python_method
    def deselect_all(self):
        self.table.deselectAll_(None)
        
    @objc.python_method
    def set_background_color(self,color):
        color = NSColor.colorWithCalibratedRed_green_blue_alpha_(int(color[1:3],16)/255.0,int(color[3:5],16)/255.0,int(color[5:7],16)/255.0,1.0)
        self.table.setBackgroundColor_(color)
        self.table.setNeedsDisplay_(True)
    
    @objc.python_method
    def set_text_color(self,color):
        self.mark_custom_text_color()
        color = NSColor.colorWithCalibratedRed_green_blue_alpha_(int(color[1:3],16)/255.0,int(color[3:5],16)/255.0,int(color[5:7],16)/255.0,1.0)
        column = self.table.tableColumns()[0]
        column.dataCell().setTextColor_(color)
        self.table.setNeedsDisplay_(True)
    
    @objc.python_method
    def set_font(self,font):
        if isinstance(font,tuple) and len(font) == 2:
            font = NSFont.fontWithName_size_(font[0],font[1])
        if font is not None:
            column = self.table.tableColumns()[0]
            column.dataCell().setFont_(font)
            self.table.setNeedsDisplay_(True)

    def numberOfRowsInTableView_(self,tableView):
        return len(self.rows)

    def tableView_objectValueForTableColumn_row_(self,tableView,tableColumn,row):
        if row < len(self.rows):
            return self.rows[row]
        return ""

    def tableViewSelectionDidChange_(self,notification):
        if callable(self.selection_callback):
            self.selection_callback()
    
    def show_scrollbar(self,show=True):
        self.w.setHasVerticalScroller_(show)
        
class Container(Widget):
    def __init__(self):
        Widget.__init__(self)
        self.w = (
            NSView.alloc()
            .initWithFrame_(NSMakeRect(0,0,200,200))
            .autorelease()
        )
        
    def set_size(self,width,height):
        self.w.setFrameSize_((width,height))
        self.relayout()

class Image(Widget):
    def __init__(self,image_path):
        Widget.__init__(self)
        self.w = NSImageView.alloc().initWithFrame_(NSMakeRect(0,0,100,100)).autorelease()
        image = NSImage.alloc().initByReferencingFile_(image_path)
        self.w.setImage_(image)
        
    def set_size(self,width,height):
        self.w.setFrameSize_((width,height))
        image = self.w.image()
        if image is not None:
            image.setSize_((width,height))
        self.relayout()
        
#MARK: Demo
if __name__ == "__main__":
    from alerts import Alert
    from layout import VLayout,HLayout
    def show_msg():
        selected_items = list_widget.get_selected()
        if selected_items:
            Alert.show("Selected Items","\n".join(selected_items))
        else:
            Alert.show("No Selection","No items selected.")
    win = Window()
    win.set_title("demo")
    win.set_size(420,330)
    win.set_layout(VLayout())
    win.titlebar_hidden(True)
    win.set_background_color("#F0F0F0")
    label = Label("ACW demo!")
    label.set_text_color("#006F14")
    label.set_size(160,30)
    label.set_font(("Arial",18))
    win.add_widget(label)
    list_widget = List()
    list_widget.set_size(160,200)
    list_widget.add_row("Item 1")
    list_widget.add_row("Item 2")
    list_widget.add_row("Item 3")
    list_widget.set_multi_selection(True)
    win.add_widget(list_widget)
    btn_container = Container()
    btn_container.set_size(160,84)
    btn_layout = HLayout(spacing=10)
    btn_layout.set_alignment("center")
    btn_container.set_layout(btn_layout)
    win.add_widget(btn_container)
    button = Button("Get Selected",show_msg)
    btn_container.add_widget(button)
    exit_button = Button("Exit",lambda: NSApp.terminate_(None))
    exit_button.set_bezel_color("#FF0000")
    exit_button.set_text_color("#FFFFFF")
    btn_container.add_widget(exit_button)
    image_btn = ImageButton("acw.png",lambda: Alert.show("ACW","ImageButton example!"))
    image_btn.set_size(64,64)
    btn_container.add_widget(image_btn)
    win.run()
