def save_html(svg_render):
    with open('role/static/upload/role.html', 'w', encoding="utf-8") as file:
        file.write(svg_render)


def save_svg(svg_render):
    with open('role/static/upload/role.svg', 'w', encoding="utf-8") as file:
        file.write(svg_render)
