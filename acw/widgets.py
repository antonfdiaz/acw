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
    NSViewMinYMargin,
    NSViewWidthSizable,
    NSColor,
    NSFont
)
from objc import super
from Foundation import NSObject,NSMakePoint

#MARK: Window
class Window:
    def __init__(self):
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
            
            self.layout_margin_left = 10
            self.layout_margin_top = 10
            self.layout_y = self.window.contentView().frame().size.height-self.layout_margin_top
            self.layout_spacing = 8
            
    def set_title(self,title):
        self.window.setTitle_(title)
        
    def close_btn_disabled(self,hidden=True):
        self.window.setStyleMask_(self.window.styleMask() & ~NSClosableWindowMask if hidden else self.window.styleMask() | NSClosableWindowMask)
        
    def minimize_btn_disabled(self,hidden=True):
        self.window.setStyleMask_(self.window.styleMask() & ~NSMiniaturizableWindowMask if hidden else self.window.styleMask() | NSMiniaturizableWindowMask)
        
    def maximize_btn_disabled(self,hidden=True):
        self.window.setStyleMask_(self.window.styleMask() & ~NSResizableWindowMask if hidden else self.window.styleMask() | NSResizableWindowMask)

    def add_widget(self,widget):
        available_width = self.window.contentView().frame().size.width - (self.layout_margin_left * 2)
        widget_height = widget.w.frame().size.height
        if hasattr(widget, "set_size"):
            widget.set_size(available_width, widget_height)
        widget.w.setAutoresizingMask_(NSViewWidthSizable | NSViewMinYMargin)
        widget.w.setFrameOrigin_(NSMakePoint(self.layout_margin_left,self.layout_y-widget_height))
        self.layout_y -= widget_height+self.layout_spacing
        self.window.contentView().addSubview_(widget.w)

    def run(self):
        NSApp.activateIgnoringOtherApps_(True)
        NSApp.run()
        
    def set_size(self,width,height):
        self.width = width
        self.height = height
        self.window.setContentSize_((width,height))
        self.layout_y = self.window.contentView().frame().size.height-self.layout_margin_top
    
#MARK: Label    
class Label:
    def __init__(self,text):
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
        
    def set_text_color(self,color):
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
class TextField:
    def __init__(self,text="",placeholder=""):
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
        
    def set_background_color(self,color):
        color = NSColor.colorWithCalibratedRed_green_blue_alpha_(int(color[1:3],16)/255.0,int(color[3:5],16)/255.0,int(color[5:7],16)/255.0,1.0)
        self.w.setBackgroundColor_(color)
        self.w.setNeedsDisplay_(True)
        
    def set_text_color(self,color):
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
class TextArea:
    def __init__(self,text="",placeholder=""):
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
        
    def set_placeholder(self,placeholder):
        self.tv.setPlaceholderString_(placeholder)
        
    def show_scrollbar(self,show=True):
        self.w.setHasVerticalScroller_(show)
        
    def set_size(self,width,height):
        self.w.setFrameSize_((width,height))
        self.tv.setFrameSize_((width,height))
        
    def set_background_color(self,color):
        color = NSColor.colorWithCalibratedRed_green_blue_alpha_(int(color[1:3],16)/255.0,int(color[3:5],16)/255.0,int(color[5:7],16)/255.0,1.0)
        self.tv.setBackgroundColor_(color)
        self.tv.setNeedsDisplay_(True)
        
    def set_text_color(self,color):
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
class Button:
    def __init__(self,text,callback):
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
        
    def set_callback(self,callback):
        self.callback = callback
        
    def set_enabled(self,enabled):
        self.w.setEnabled_(enabled)
        
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
        
def get_text(tf):
    print("TextField value:",tf.get_text())
    
#MARK: Table
class Table(NSObject):
    def initWithColumns_(self,columns):
        self = objc.super(Table,self).init()
        if self is None:
            return None

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

    def set_size(self,width,height):
        self.w.setFrameSize_((width,height))
        self.table.setFrameSize_((width,height))

    def add_row(self,row_data):
        self.rows.append(list(row_data))
        self.table.reloadData()

    def numberOfRowsInTableView_(self,tableView):
        return len(self.rows)

    def tableView_objectValueForTableColumn_row_(self,tableView,tableColumn,row):
        col_index = self.table.tableColumns().indexOfObject_(tableColumn)
        if row < len(self.rows) and col_index < len(self.rows[row]):
            return str(self.rows[row][col_index])
        return ""
    
    def show_scrollbar(self,show=True):
        self.w.setHasVerticalScroller_(show)
    
#MARK: List
class List(NSObject):
    def init(self):
        self = super().init()
        if self is None:
            return None

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
        self.table.setHeaderView_(None)
        self.w.setDocumentView_(self.table)

        column = NSTableColumn.alloc().initWithIdentifier_("main")
        column.setTitle_("Items")
        self.table.addTableColumn_(column)

        return self

    @objc.python_method
    def set_size(self,width,height):
        self.w.setFrameSize_((width,height))
        self.table.setFrameSize_((width,height))

    @objc.python_method
    def add_row(self,text):
        self.rows.append(str(text))
        self.table.reloadData()

    def numberOfRowsInTableView_(self,tableView):
        return len(self.rows)

    def tableView_objectValueForTableColumn_row_(self,tableView,tableColumn,row):
        if row < len(self.rows):
            return self.rows[row]
        return ""
    
    def show_scrollbar(self,show=True):
        self.w.setHasVerticalScroller_(show)
        
#MARK: Demo
if __name__ == "__main__":
    win = Window()
    win.set_title("demo")
    win.set_size(400,300)
    label = Label("ACW demo!")
    label.set_text_color("#006F14")
    label.set_size(400,30)
    label.set_font(("Arial",18))
    win.add_widget(label)
    textfield = TextField("Default text","Placeholder text")
    textfield.set_background_color("#FF0000")
    textfield.set_text_color("#FFFFFF")
    textfield.set_bezeled(False)
    win.add_widget(textfield)
    textarea = TextArea("Default text in textarea","Placeholder text in textarea")
    textarea.set_background_color("#00FF00")
    textarea.set_text_color("#000000")
    textarea.set_font(("Comic Sans MS",12))
    win.add_widget(textarea)
    btn = Button("Purple button!",lambda: print("Button clicked!"))
    btn.set_bezel_color("#2F001FFF")
    win.add_widget(btn)
    btn = Button("Blue button!",lambda: print("Button clicked!"))
    btn.set_bezel_color("#00357AFF")
    win.add_widget(btn)
    btn = Button("Custom font!",lambda: print("Button clicked!"))
    btn.set_font(("Courier",12))
    win.add_widget(btn)
    win.run()