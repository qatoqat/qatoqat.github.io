from pages import home


def generate_html(base, title, content, scripts, destination):
    with open(base) as base_file:
        with open(destination, "w") as f:
            f.write(
                base_file.read()
                .replace("{{ title }}", title + " - " if title else "", 1)
                .replace("{{ content }}", content, 1)
                .replace(
                    "{{ scripts }}",
                    "".join([f'<script src="{src}"></script>' for src in scripts]) if scripts else ""
                )
            )


generate_html(home.base, home.title, home.content, home.scripts, home.destination)
