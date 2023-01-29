import random
from colorama import Fore, Style

from utils import is_matrix

def generate_new_map(width_in_characters: int, height_in_characters: int) -> list[list[str]]:
    new_map = []
    row = []

    for i in range(width_in_characters): 
        row.append(" ")
    for i in range(height_in_characters): 
        new_map.append(row[:])

    return new_map


def map_loading(previos_frame: list[list[str]]) -> list[list[str]]: 
    previos_frame = [list(i) for i in previos_frame]
    row_length = is_matrix(previos_frame)
    previos_frame.pop()

    new_row = []
    for i in range(row_length):
        new_row.append(" ")

    if random.randint(0, 2) == 0:
        new_row[random.randint(0, row_length-1)] = f"{Fore.LIGHTBLACK_EX}.{Style.RESET_ALL}"
    next_frame = [new_row[:]] + previos_frame[:]

    return next_frame


def objects_loading(matrix: list[list[str]], entities:list, prokectiles:list):

    matrix = [list(i) for i in matrix]

    for j in prokectiles:
        matrix[j.y][j.x] = j.skin
    for j in entities:
        matrix[j.y][j.x] = j.skin

    return matrix


def matrix_to_string(matrix: list[list[str]]) -> str:
    return "\n" + "\n".join([" ".join(i) for i in matrix])