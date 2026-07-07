from AppKit import NSAlert,NSTextField,NSSecureTextField,NSAlertFirstButtonReturn

class Alert:
    @staticmethod
    def show(title,message,buttons=["OK"]):
        alert = NSAlert.alloc().init()
        alert.setMessageText_(title)
        alert.setInformativeText_(message)
        for button in buttons:
            alert.addButtonWithTitle_(button)
        clicked = alert.runModal()
        return clicked == NSAlertFirstButtonReturn
        
class InputAlert:
    @staticmethod
    def show(title,message,default="",placeholder="",rounded=False,hidden=False):
        alert = NSAlert.alloc().init()
        alert.setMessageText_(title)
        alert.setInformativeText_(message)
        alert.addButtonWithTitle_("OK")
        alert.addButtonWithTitle_("Cancel")
        field_class = NSSecureTextField if hidden else NSTextField
        input_field = field_class.alloc().initWithFrame_(((0,0),(200,24)))
        input_field.setStringValue_(default)
        input_field.setPlaceholderString_(placeholder)
        if rounded:
            input_field.setBezelStyle_(1)
        alert.setAccessoryView_(input_field)
        response = alert.runModal()
        if response == NSAlertFirstButtonReturn:
            return input_field.stringValue()
        else:
            return None