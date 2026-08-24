def extract_title(markdown):
    for line in markdown.splitlines():
        normalized_line = line.lstrip("\ufeff").strip()
        if normalized_line.startswith("# ") and not normalized_line.startswith("##"):
            return normalized_line[2:].strip()

    raise Exception("No h1 header found")
