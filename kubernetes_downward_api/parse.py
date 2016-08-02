import os.path


def _parse_file(path):
    name = os.path.basename(path)

    with open(path) as f:
        first = f.readline()

        if '="' not in first:
            return {name: first}

        data = {}

        for line in [first] + f.readlines():
            key, value = line.split('=')
            data[key] = value.strip('"\n')

        return {name: data}


def _parse(path):
    if os.path.isfile(path):
        return _parse_file(path)


def parse(paths):
    metadata = {}

    for path in paths:
        metadata.update(_parse(path))

    return metadata
