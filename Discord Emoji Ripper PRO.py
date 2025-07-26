def build_sticker_url(sticker_id: int):
    """
    Build the sticker URL for a given sticker ID.
    """
    return f"https://media.discordapp.net/stickers/{sticker_id}.png"

def build_emoji_gif_url(emoji_id: int):
    """
    Build the emoji GIF URL for a given emoji ID.
    """
    return f"https://cdn.discordapp.com/emojis/{emoji_id}.gif?size=48"

def build_emoji_url(emoji_id: int):
    """
    Build the emoji URL for a given emoji ID.
    """
    return f"https://cdn.discordapp.com/emojis/{emoji_id}.png?size=48"

from pyperclip import PyperclipException as ClipboardException

def check_clipboard():
    """
    Get the current content of the clipboard.
    """
    from pyperclip import paste as get_clipboard
    try:
        clipboard =  get_clipboard()
        if clipboard.isdigit():
            try:
                int(clipboard)
                return clipboard
            except ValueError:
                return None
    except ClipboardException:
        return None

def check_valid_link(link_list: list):
    """
    Check if the clipboard contains a valid link.
    """
    from pyperclip import copy as set_clipboard
    from requests import get as requests_get
    from requests.exceptions import RequestException

    for link in link_list:
        try:
            response = requests_get(link)
            if response.status_code == 200:
                try:
                    set_clipboard(link)
                    return
                except ClipboardException:
                    return None
        except RequestException:
            return None
        
def main():
    """
    Main function to run the script.
    """
    id = check_clipboard()
    if id is not None:
        sticker_url = build_sticker_url(id)
        emoji_gif_url = build_emoji_gif_url(id)
        emoji_url = build_emoji_url(id)
        link_list = [sticker_url, emoji_gif_url, emoji_url]
        check_valid_link(link_list)

if __name__ == "__main__":
    main()