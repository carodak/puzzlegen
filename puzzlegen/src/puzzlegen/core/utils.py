"""
Utility functions for puzzle generation and manipulation.
"""

import random
from typing import List, Tuple, Dict, Any

def assign_blocks_per_color(nb_blocks: int, colors: List[str]) -> List[Tuple[str, int]]:
    """
    Randomly assign a color to each block, ensuring at least 3 blocks per color.

    Args:
        nb_blocks (int): Total number of blocks to assign.
        colors (list): List of color names.

    Returns:
        list: List of tuples (color, number_of_blocks).
    """
    blocks_per_color = []
    nb_blocks_to_assign = nb_blocks

    for color in colors:
        blocks_per_color.append([color, 3])
        nb_blocks_to_assign -= 3

    while nb_blocks_to_assign > 0:
        random_color = random.choice(colors)
        random_blocks = random.randint(1, nb_blocks_to_assign)
        for block in blocks_per_color:
            if block[0] == random_color:
                block[1] += random_blocks
                break
        nb_blocks_to_assign -= random_blocks

    return [(color, count) for color, count in blocks_per_color]

def sort_blocks_by_rows(set_blocks: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    Sort blocks by their row index.

    Args:
        set_blocks (dict): Dictionary with positions as keys.

    Returns:
        dict: Sorted dictionary by row.
    """
    return dict(sorted(set_blocks.items(), key=lambda x: x[0]))

def sort_blocks_by_columns(set_blocks: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    Sort blocks by their column index.

    Args:
        set_blocks (dict): Dictionary with positions as keys.

    Returns:
        dict: Sorted dictionary by column.
    """
    return dict(sorted(set_blocks.items(), key=lambda x: x[0][1]))