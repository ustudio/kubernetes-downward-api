# kubernetes-downward-api

Parse Kubernetes Downward API Volumes in Python

## Installing ##

Install via pip:

```
pip install kubernetes-downward-api
```

## Basic Usage ##

Given a list of files mounted via a Kubernetes Downward API Volume,
`parse` will return a dictionary, mapping files names to
values. Simple values will be strings, complex values will be
dictionaries:

```python
from pprint import pprint
from kubernetes_downward_api import parse


metadata = parse(['/etc/namespace', '/etc/labels'])

pprint(metadata)

# Prints:
# {
#   "namespace": "default",
#   "labels": {
#     "label1": "value"
#     "label2": "value"
#   }
# }
```

## Directory Parsing ##

Paths passed to `parse` may also be directories, in which case all
files in the directory will be parsed, assuming they are all generated
via the Downward API Volume. This is handy if the Downward API Volume
is mounted to an otherwise empty or non-existent directory:

```python
from pprint import pprint
from kubernetes_downward_api import parse


metadata = parse(['/etc/downward-api'])

pprint(metadata)

# Assuming namespace and labels are the items exposed
# Prints:
# {
#   "namespace": "default",
#   "labels": {
#     "label1": "value"
#     "label2": "value"
#   }
# }
```
