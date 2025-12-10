def welcome_sequence(items: list):
    max_chars = len(max(items, key=len))
    line_len =  max_chars + 10 * 2
    items = [''] + items + ['']
    hor_bar = line_len * "░"

    print(hor_bar)

    for item in items:
        print(f"{item:^{line_len-2}}")

    print(hor_bar)


def identify_path(basename: str):
    pass