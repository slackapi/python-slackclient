import logging
from typing import List, Union, Dict, Any

from .basic_objects import BaseObject
from .basic_objects import EnumValidator
from .basic_objects import JsonObject
from .basic_objects import JsonValidator


# NOTE: used only for legacy components - don't use this for Block Kit
def extract_json(
    item_or_items: Union[JsonObject, List[JsonObject]], *format_args
) -> Union[Dict[Any, Any], List[Dict[Any, Any]]]:
    """
    Given a sequence (or single item), attempt to call the to_dict() method on each
    item and return a plain list. If item is not the expected type, return it
    unmodified, in case it's already a plain dict or some other user created class.

    Args:
      item_or_items: item(s) to go through
      format_args: Any formatting specifiers to pass into the object's to_dict
            method
    """
    try:
        return [
            elem.to_dict(*format_args) if isinstance(elem, JsonObject) else elem
            for elem in item_or_items
        ]
    except TypeError:  # not iterable, so try returning it as a single item
        return (
            item_or_items.to_dict(*format_args)
            if isinstance(item_or_items, JsonObject)
            else item_or_items
        )


def show_unknown_key_warning(name: Union[str, object], others: dict):
    if "type" in others:
        others.pop("type")
    if len(others) > 0:
        keys = ", ".join(others.keys())
        logger = logging.getLogger(__name__)
        if isinstance(name, object):
            name = name.__class__.__name__
        logger.debug(
            f"!!! {name}'s constructor args ({keys}) were ignored."
            f"If they should be supported by this library, report this issue to the project :bow: "
            f"https://github.com/slackapi/python-slackclient/issues"
        )
