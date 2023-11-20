import re

transliter_dict = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "є": "ye",
    "ж": "j",
    "з": "z",
    "и": "y",
    "і": "i",
    "ї": "i",
    "й": "i",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "h",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "sch",
    "ю": "yu",
    "я": "ya",
    "ь": "",
    "ы": "y",
    "э": "e",
    "ъ": ""
}


def normalize(file_name):
    str = ""
    for char in file_name:
        low_char = char.lower()
        if low_char in transliter_dict:
            if char.isupper():
                str = str + transliter_dict[low_char].capitalize()
            else:
                str = str + transliter_dict[char]
        elif re.match(r"[0-9a-zA-Z]", char):
            str += char
        else:
            str += "_"
    return str
