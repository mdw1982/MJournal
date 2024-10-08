import FreeSimpleGUI as sg
from settings import detect_os

sg.Window._move_all_windows = True



def show_splash():
    # filename='images/SplashScreen.png',
    if detect_os() == 'windows':
        background_layout = [[sg.Image(size=(650,450), background_color='white')]]
        window_background = sg.Window('Background', background_layout, transparent_color='white', location=(520, 340), no_titlebar=True, finalize=True, margins=(0, 0),
                                      element_padding=(0, 0), right_click_menu=[[''], ['Exit', ]])
    '''Commented out 9-23-24 because it wasn't behaving itself, because it won't use transparent backgrounds in Linux - limitation of the API
       and I've noticed in Hyprland its just plain ugly.'''
    # if detect_os() == 'Linux':
    #     background_layout = [[sg.Image(filename='images/SplashScreen.png',size=(650, 500), background_color='white')]]
    #     window_background = sg.Window('Background', background_layout,location=(3880, 340), no_titlebar=True, finalize=True, margins=(0, 0),
    #                                   element_padding=(0, 0), right_click_menu=[[''], ['Exit', ]])

    layout = [
        [sg.Push(), sg.Text('MJoural  - Simple Database Drive Journaling Program', font=('Helectiva', 10)), sg.Push()],
        [sg.Push(), sg.ProgressBar(1, bar_color='purple', orientation='h', size=(30, 20), key='progress',
                                   border_width=0, pad=(0,0)), sg.Push()]
    ]


    top_window = sg.Window('Everything bagel', layout, location=(660, 510), finalize=True, keep_on_top=True, grab_anywhere=False, no_titlebar=True)
    progress_bar = top_window['progress']
    # window_background.send_to_back()
    # top_window.bring_to_front()
    for i in range(10095):
        window, event, values = sg.read_all_windows(timeout=0)
        #print(event, values)
        if event is None or event == 'Cancel' or event == 'Exit':
            print(f'closing window = {window.Title}')
            break
        progress_bar.update_bar(i + 1, 10095)

    top_window.close()
    #window_background.close()


if __name__ == '__main__':
    show_splash()