# Copyright (C) 2024-2026 Burak Günaydin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# A dumb algorithm that estimates the plural form of words, based on the last letter
def pluralize(word:str) -> str:
    """
    Estimate the plural form of a given word based on its last letter.
    word: The singular form of the word to be pluralized.
    Returns the estimated plural form of the word.
    """
    last_letter = word[-1].lower()
    if last_letter in ['s', 'x', 'z']:
        return word + 'es'
    elif last_letter == 'y' and len(word) > 1 and word[-2].lower() not in 'aeiou':
        return word[:-1] + 'ies'
    else:
        return word + 's'