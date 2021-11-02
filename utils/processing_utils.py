def get_hyphenated_str(text, font, width_img) -> str:
    """
    This function changes the line break in the text to fit into images.
    :param text: Text to change.
    :param font: Read font.
    :param width_img: Width image.
    :return: Edited text.
    """

    width, height = font.getsize(text)
    if font.getsize(text)[0] >= width_img:
        result = [i for i, chr in enumerate(text) if chr == ' ']
        if not result:
            print('Error get_hyphenated_str')

        for index, pos in enumerate(result):
            if text[pos - 1] == ',':
                text = "\n".join([text[:pos], text[pos + 1:]])

                if font.getsize(text[pos + 3:])[0] < width_img:
                    return text

    text = text.replace(' ', '\n')
    return text