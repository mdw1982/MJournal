from tkhtmlview import html_parser
import FreeSimpleGUI as sg

def set_html(widget, readme, strip=True):
    prev_state = widget.cget('state')
    widget.config(state=sg.tk.NORMAL)
    widget.delete('1.0', sg.tk.END)
    widget.tag_delete(widget.tag_names)
    html_parser.w_set_html(widget, readme, strip=strip)
    widget.config(state=prev_state)

with open('README.html', 'r') as h:
    readme = h.read()


layout = [[sg.Multiline(readme, key='content', expand_y=True, expand_x=True, text_color='Black', background_color='White')],
          [sg.Push(),sg.B('Close', key='quit')]
          ]

window = sg.Window('MJournal HowTo',layout, size=(950,600), location=(550, 245), modal=True,finalize=True, resizable=True)
advertise = window['content'].Widget
html_parser = html_parser.HTMLTextParser()
set_html(advertise, readme)
width, height = advertise.winfo_width(), advertise.winfo_height()

while True:
    event, values = window.read()
    match event:
        case 'quit':
            break
    window.close()
