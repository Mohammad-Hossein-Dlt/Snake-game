import re
from enum import Enum
from typing import Literal

divider_char = "│"
v_divider_back = 1
v_divider_front = 2

# Vertical dividers
left_divider = (" " * v_divider_back) + divider_char + (" " * v_divider_front)
right_divider = (" " * v_divider_front) + divider_char + (" " * v_divider_back)

class Color(str, Enum):
    BLACK = "1;30"
    RED = "1;31"
    GREEN = "1;32"
    YELLOW = "1;33"
    BLUE = "1;34"
    PURPLE = "1;35"
    TURQUOISE = "1;36"
    WHITE = "1;37"
    GOLD = "38;2;255;215;0"
    GRAY = "90"

def tag_text(
    text: str,
    color: Color,
):
    text = text.strip()  
    text_lines = text.split("\n")
    
    tagged_text = ""
    for line in text_lines:
        tagged_text += f"<{color.name}>" + line + f"</{color.name}>"
        tagged_text += "\n"    
    
    return tagged_text.strip()

def remove_tag(
    tagged_text: str,
    with_tag_name: bool = False,
) -> tuple[str, str] | str:
        
    tag_name, content = "", ""
    
    pattern = r"<(\w+)>(.*?)</\1>"
    matches = re.findall(pattern, tagged_text)
    if matches:
        for index, (t_name, cntnt) in enumerate(matches):
            tag_name = t_name
            content += cntnt + ("\n" if index != len(matches) - 1 else "") 
    
    tag_name = tag_name.strip()
    content = content or tagged_text
        
    return [tag_name, content] if with_tag_name else content

def colorize_text(
    text: str,
    code: Color | None = None,
    tag: str | None = None,
):
    color_code = ""
    
    if code:
        color_code = code.value
    elif tag:
        try:
            color_code = Color[tag].value
        except Exception:
            color_code = Color.WHITE.value
    
    return f"\033[{color_code}m" + text + "\033[0m" if color_code else text

def create_horizontal_divider(
    offset: int,
    length: int,
    position: Literal["top", "bottom"],
) -> str:
    """Create horizontal top/bottom dividers."""
    if position == "top":
        return (" " * offset) + "┌" + ("─" * length) + "┐"
    if position == "bottom":
        return (" " * offset) + "└" + ("─" * length) + "┘"

def create_horizontal_indicator(
    index: int,
    padding_size: int,
    position: Literal["left", "right"],
) -> str:
    if position == "left":
        return str(index).rjust(padding_size) + left_divider
    if position == "right":
        return right_divider + str(index).ljust(padding_size)
    
def show(
    data: list[list[str]],
    footer: str,
    footer_color: Color,
) -> str:
    """
    Render a table-like structure with row/column indicators and dividers.
    """
    # ─── Configurations ────────────────────────────────────────────────
    column_count = len(data[0])
    max_column_digits_count = len(str(column_count))

    # Ensure column digit width is odd
    if max_column_digits_count % 2 == 0:
        max_column_digits_count += 1

    # Maximum width & height among all cells
    max_cell_width = max(
        len(remove_tag(tagged_text=line, with_tag_name=False))
        for row in data
        for cell in row
        for line in cell.split("\n")
    )
        
    max_cell_height = max(
        len(remove_tag(tagged_text=cell, with_tag_name=False).split("\n"))
        for row in data
        for cell in row
    )
        
    half_height = (max_cell_height - 1) // 2 if max_cell_height % 2 != 0 else max_cell_height // 2
    half_height = max(1, half_height)
        
    # Column width must fit both digits and item content
    max_width = max(max_cell_width, max_column_digits_count)

    # Padding inside cells
    padding_size = 2 if max_cell_width > 1 else 4
    padding = " " * padding_size

    # Horizontal spacing between columns
    row_spacing = " " * (
        (column_count * max_width)
        + (padding_size * (column_count - 1))
    )

    # ─── Build Content ────────────────────────────────────────────────
    content = "\n"
    
    for row_index, row in enumerate(data):

        # Prepare empty lines
        top_list: list[list[str]] = [ [" " for _ in range(column_count)] for _ in range(half_height) ]
        middle_list: list[str] = [ " " for _ in range(column_count) ]
        bottom_list: list[list[str]] = [ [" " for _ in range(column_count)] for _ in range(half_height) ]

        for cell_index, cell in enumerate(row):
            cell = cell.strip()
            
            cell_lines = cell.split("\n")
            cell_lines_length = len(cell_lines)
            
            half_cell_height = (cell_lines_length - 1) // 2 if cell_lines_length % 2 != 0 else cell_lines_length // 2
            half_cell_height = max(1, half_cell_height)

            if cell_lines_length > 1:
                
                for line_index, line in enumerate(cell_lines):
                    tag_name, text = remove_tag(tagged_text=line, with_tag_name=True)
                    text = text.center(max_width)
                    cell_lines[line_index] = colorize_text(text, tag=tag_name)
                                                
                for half_cell_index in range(half_cell_height):
                    top_list[half_cell_index+(half_height-half_cell_height)][cell_index] = cell_lines.pop(0)
                    bottom_list[half_cell_index+(half_height-half_cell_height)][cell_index] = cell_lines.pop()                    
                
                if cell_lines:
                    middle_list[cell_index] = cell_lines[0]
                else:
                    middle_list[cell_index] = " ".center(max_width)
            else:
                tag_name, text = remove_tag(tagged_text=cell, with_tag_name=True)
                cell = text.center(max_width)
                cell = colorize_text(cell, tag=tag_name)
                middle_list[cell_index] = cell
                
        bottom_list.reverse()

        # ── Format top rows ──
        before = "".join(
            padding
            + left_divider
            + padding.join(val.center(max_width) for val in row_top)
            + right_divider
            + padding
            + "\n"
            for row_top in top_list
        )
        
        # ── Format middle rows ──
        middle = (
            create_horizontal_indicator(row_index, padding_size, "left")
            + padding.join(val.center(max_width) for val in middle_list)
            + create_horizontal_indicator(row_index, padding_size, "right")
            + "\n"
        )
        
        # ── Format bottom rows ──
        after = "".join(
            padding
            + left_divider
            + padding.join(val.center(max_width) for val in row_bottom)
            + right_divider
            + padding
            + "\n"
            for row_bottom in bottom_list
        )

        content += before + middle + after
        
    # ─── Axis Indicators ─────────────────────────────────────────────
    x_indicator = [str(i).center(max_width) for i in range(column_count)]
    horizontal_indicator = padding + (" " * len(left_divider)) + padding.join(x_indicator)

    top_horizontal_divider = create_horizontal_divider(
        padding_size + v_divider_back,
        v_divider_front + len(row_spacing) + v_divider_front,
        "top",
    )
    bottom_horizontal_divider = create_horizontal_divider(
        padding_size + v_divider_back,
        v_divider_front + len(row_spacing) + v_divider_front,
        "bottom",
    )

    # ─── Final Assembly ──────────────────────────────────────────────
    content = (
        "\n"
        + horizontal_indicator
        + "\n"
        + top_horizontal_divider
        + content
        + bottom_horizontal_divider
        + "\n"
        + horizontal_indicator
        + "\n"
    )
    
    if footer:
        
        footer_padding = (
            (
                padding_size
                +
                v_divider_back
                + len(divider_char)
            )
            * " "
        )
        
        content += (
            "\n\n"
            + footer_padding
            + colorize_text(footer, code=footer_color)
            + "\n"
        )
                
    return content + "\n"
