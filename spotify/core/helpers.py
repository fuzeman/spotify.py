def set_defaults(d, defaults):
    if d is None:
        d = {}

    for key, value in defaults.items():
        d.setdefault(key, value)

    return d


def etree_convert(node):
    if node.text and node.text.strip():
        return node.text

    if len(node) and node.tag.startswith(node[0].tag):
        return etree_list(node)

    return etree_dict(node)


def etree_dict(node):
    return dict([
        (sub.tag, etree_convert(sub))
        for sub in node
    ] + node.attrib.items())


def etree_list(node):
    return [etree_convert(sub) for sub in node]
