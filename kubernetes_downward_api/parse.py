import os
import os.path


def _parse_file(path):
    name = os.path.basename(path)

    with open(path) as f:
        data = {}

        for line in f:
            line = line.strip()

            if line is '':
                continue

            if '="' not in line:
                if len(data) == 0:
                    return {name: line}
                raise ValueError(
                    "Line in complex file lacks key/value pair: {0}".format(
                        line))

            key, value = line.split('=')
            data[key] = value.strip('"')

        return {name: data}


def _parse_dir(path):
    metadata = {}

    for filename in os.listdir(path):
        abs_path = os.path.join(path, filename)

        if not filename.startswith('.') and os.path.isfile(abs_path):
            metadata.update(_parse_file(abs_path))

    return metadata


def _parse(path):
    if os.path.isfile(path):
        return _parse_file(path)
    else:
        return _parse_dir(path)


def parse(paths):
    metadata = {}

    for path in paths:
        metadata.update(_parse(path))

    return metadata
