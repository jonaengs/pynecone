"""Dynamically compile classes for all HTML elements and output them to the
elements directory.

This script generates the element classes in the pynecone.el.elements module.
Run as follows:

    python -m pynecone.el.precompile

Make sure to delete the __init__.py file in the elements directory before
running this script.
"""

import os

from pynecone.compiler.templates import join

from .constants import ELEMENT_TO_PROPS, ELEMENTS

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
ELEMENTS_DIR = os.path.join(FILE_DIR, "elements")
INIT_PY_PATH = os.path.join(ELEMENTS_DIR, "__init__.py")


def element_path(element: str) -> str:
    """Get the name of the Python file for the given element."""
    return os.path.join(ELEMENTS_DIR, f"{element}.py")


PROP = "    {prop}: PCVar[Union[str, int, bool]]".format


def compile_pyclass_props(element: str):
    """Compile props for an element."""
    return join(PROP(prop=prop) for prop in ELEMENT_TO_PROPS[element])


PYCLASS = join(
    [
        "",
        "class {name}(Element):  # noqa: E742",
        '    """Display the {element} element."""',
        "",
        '    tag = "{element}"',
        "",
        "{props}",
        "",
        "{call_name} = {name}.create",
        "",
    ]
).format


def compile_pyclass(element: str):
    """Compile a Python class for an element."""
    name = element.capitalize()
    props = compile_pyclass_props(element)

    # Handle the `del` element, which is a Python keyword. Note that the class
    # name is still `Del`.
    call_name = "del_" if element == "del" else element

    return PYCLASS(
        name=name,
        element=element,
        props=props,
        call_name=call_name,
    )


INIT_PY = [
    '"""Element classes. This is an auto-generated file. Do not edit. See ../generate.py."""',
    "from typing import Union",
    "",
    "from pynecone.el.element import Element",
    "from pynecone.var import Var as PCVar",
    "",
]


for element in sorted(ELEMENTS):
    INIT_PY.append(compile_pyclass(element))


os.makedirs(ELEMENTS_DIR, exist_ok=True)
with open(INIT_PY_PATH, "w+") as f:
    f.write(join(INIT_PY))
