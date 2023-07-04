import re


def replace_words(text, words, replace_start='<span>', replace_end='</span>', case_insensitive=False):
    positions = []
    replaced_text = text

    flags = re.IGNORECASE if case_insensitive else 0

    for word in words:
        pattern = re.compile(re.escape(word), flags)
        matches = pattern.finditer(replaced_text)
        for match in matches:
            start, end = match.start(), match.end()

            # Check if the current match overlaps with any existing positions
            is_overlapping = False
            for pos_start, pos_end in positions:
                if start <= pos_end and end >= pos_start:
                    is_overlapping = True
                    if end - start > pos_end - pos_start:
                        # Replace the existing overlapping position with the longer match
                        positions.remove((pos_start, pos_end))
                        positions.append((start, end))
                    break

            # If the match is not overlapping with any existing positions, add it to the list
            if not is_overlapping:
                positions.append((start, end))

    # Replace words in reverse order to avoid modifying newly added <span> tags
    positions.sort(key=lambda pos: pos[0], reverse=True)
    for start, end in positions:
        replaced_text = replaced_text[:start] + replace_start + replaced_text[start:end] + replace_end + replaced_text[end:]

    return replaced_text
