def save_html(svg_render):
    with open('role/static/upload/role.html', 'w', encoding="utf-8") as file:
        file.write(svg_render)


def save_svg(svg_render):
    with open('role/static/upload/role.svg', 'w', encoding="utf-8") as file:
        file.write(svg_render)

def create_html():
    html = f'<embed src="tree.svg" type="image/svg+xml">'
    with open('sem_synt/static/upload/tree.html', 'w') as file:
        file.write(html)
