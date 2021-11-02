def get_box_size_to_draw(markup: dict, number=False) -> tuple:
    """
    This function returns the size of  box by 4 coordinates.
    :param markup: Background markup of entity.
    :param number: Is it a number or not.
    :return: Width and height of the box.
    """

    left_upper_point = markup[0]
    right_upper_point = markup[1]
    down_point = markup[3]
    if number:
        x = down_point[1] - left_upper_point[1]
        y = x
    else:
        x = right_upper_point[0] - left_upper_point[0]
        y = down_point[1] - left_upper_point[1]
    return x, y


def get_box_corner_to_draw(markup, number=False) -> tuple:
    """
    Returns the coordinate of corner box to draw.
    :param markup: Background markup  of entity.
    :param number: Is it a number or not.
    :return: Coordinate of corner box.
    """
    if number:
        # Чтобы от этого избавиться, надо найти как вставлять по вернему левому углу.
        extra_space = get_box_size_to_draw(markup)
        return markup[0][0] - (extra_space[1] - extra_space[0]), markup[0][1]
    else:
        return markup[0][0], markup[0][1]
