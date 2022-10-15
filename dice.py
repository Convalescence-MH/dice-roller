#!/usr/bin/env python3

"""
A simple program for rolling virtual dice of various sizes. Right now it can
only handle simple rolls of polyhedral dice, but in the future it will also
be able to handle things like addition and counting successes.

I'll also add support for Genesys RPG dice, which would actually be useful to
have. It'll probably use the number conversion table from the core book, but
will have to handle things like canceling success/failure and advantage/threat.

Pyglet's text_input.py was the starting point for this project.
"""

from random import randint
import pyglet

class Rectangle(object):
    def __init__(self, x_1, y_1, x_2, y_2, batch) -> None:
        self.vertext_list = batch.add(4, pyglet.gl.GL_QUADS, None,
            ('v2i', [x_1, y_1, x_2, y_1, x_2, y_2, x_1, y_2]),
            ('c4B', [90, 90, 70, 100] * 4))

class TextWidget(object):
    def __init__(self, text, x, y, width, batch) -> None:
        self.document = pyglet.text.document.UnformattedDocument(text)
        self.document.set_style(0, len(self.document.text),
            dict(color=(220, 220, 50, 255))
        )
        font = self.document.get_font()
        height = font.ascent - font.descent

        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document, width, height, multiline=False, batch=batch)
        self.caret = pyglet.text.caret.Caret(self.layout)
        
        self.layout.x = x
        self.layout.y = y

        pad = 2
        self.rectangle = Rectangle(x - pad, y - pad,
            x + width + pad, y + height + pad, batch)
        
    def hit_test(self, x, y):
        return (0 < x - self.layout.x < self.layout.width and
                0 < y - self.layout.y < self.layout.height)
 
class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(400, 140, caption="Dice Roller")
        self.batch = pyglet.graphics.Batch()

        self.labels = [
            pyglet.text.Label("Enter your dice to roll:", x=25, y=100, anchor_y="bottom",
            color=(180,180,45,255), batch  = self.batch),
            pyglet.text.Label("[Result]", font_size = 20, x = self.width//2, y = self.height//2 - 20,
            anchor_x = "center", anchor_y = "center", color=(180,180,45,255), batch = self.batch)
        ]

        self.widgets = [TextWidget("", 250, 100, self.width - 300, self.batch)]
        self.text_cursor = self.get_system_mouse_cursor("text")

        self.focus = None
        self.set_focus(self.widgets[0])
    
    def on_resize(self, width, height):
        super(Window, self).on_resize(width, height)
        for widget in self.widgets:
            widget.width = width - 110
    
    def on_draw(self):
        pyglet.gl.glClearColor(0.153, 0.153, 0.133, 1)
        self.clear()
        self.widgets[0].document.text = self.widgets[0].document.text.strip()
        self.batch.draw()
    
    def on_mouse_motion(self, x, y, dx, dy):
        for widget in self.widgets:
            if widget.hit_test(x, y):
                self.set_mouse_cursor(self.text_cursor)
                break
        else:
            self.set_mouse_cursor(None)
    
    def on_mouse_press(self, x, y, button, modifiers):
        for widget in self.widgets:
            if widget.hit_test(x, y):
                self.set_focus(widget)
                break
        else:
            self.set_focus(None)

        if self.focus:
            self.focus.caret.on_mouse_press(x, y, button, modifiers)
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.focus:
            self.focus.caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
    
    def on_text(self, text):
        if self.focus:
            self.focus.caret.on_text(text)
    
    def on_text_motion(self, motion):
        if self.focus:
            self.focus.caret.on_text_motion(motion)
    
    def on_text_motion_select(self, motion):
        if self.focus:
            self.focus.caret.on_text_motion_select(motion)
    
    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.TAB:
            if modifiers and pyglet.window.key.MOD_SHIFT:
                dir = -1
            else:
                dir = 1
        
            if self.focus in self.widgets:
                i = self.widgets.index(self.focus)
            else:
                i = 0
                dir = 0
            
            self.set_focus(self.widgets[(i + dir) % len(self.widgets)])
        
        elif symbol == pyglet.window.key.ENTER:         
            roll = self.widgets[0].document.text
            roll = [eval(num) for num in roll.split("d")]
            roll = [randint(1, roll[1]) for x in range(roll[0])]
            self.labels[1].text = f"{sum(roll)}: {roll}"

        elif symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()
    
    def set_focus(self, focus):
        if self.focus:
            self.focus.caret.visible = False
            self.focus.caret.mark = self.focus.caret.postion = 0
        
        self.focus = focus
        if self.focus:
            self.focus.caret.visible = True
            self.focus.caret.mark = 0
            self.focus.caret.position = len(self.focus.document.text)

if __name__ == "__main__":
    window = Window(resizable=True)
    pyglet.app.run()
