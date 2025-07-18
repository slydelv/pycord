from __future__ import annotations

import os
from typing import TYPE_CHECKING

from ..components import InputText as InputTextComponent
from ..enums import ComponentType, InputTextStyle

__all__ = ("InputText",)

if TYPE_CHECKING:
    from ..types.components import InputText as InputTextComponentPayload


class InputText:
    """Represents a UI text input field.

    .. versionadded:: 2.0

    Parameters
    ----------
    style: :class:`~discord.InputTextStyle`
        The style of the input text field.
    custom_id: Optional[:class:`str`]
        The ID of the input text field that gets received during an interaction.
    label: :class:`str`
        The label for the input text field.
        Must be 45 characters or fewer.
    placeholder: Optional[:class:`str`]
        The placeholder text that is shown if nothing is selected, if any.
        Must be 100 characters or fewer.
    min_length: Optional[:class:`int`]
        The minimum number of characters that must be entered.
        Defaults to 0 and must be less than 4000.
    max_length: Optional[:class:`int`]
        The maximum number of characters that can be entered.
        Must be between 1 and 4000.
    required: Optional[:class:`bool`]
        Whether the input text field is required or not. Defaults to ``True``.
    value: Optional[:class:`str`]
        Pre-fills the input text field with this value.
        Must be 4000 characters or fewer.
    row: Optional[:class:`int`]
        The relative row this input text field belongs to. A modal dialog can only have 5
        rows. By default, items are arranged automatically into those 5 rows. If you'd
        like to control the relative positioning of the row then passing an index is advised.
        For example, row=1 will show up before row=2. Defaults to ``None``, which is automatic
        ordering. The row number must be between 0 and 4 (i.e. zero indexed).
    """

    __item_repr_attributes__: tuple[str, ...] = (
        "label",
        "placeholder",
        "value",
        "required",
        "style",
        "min_length",
        "max_length",
        "custom_id",
        "id",
    )

    def __init__(
        self,
        *,
        style: InputTextStyle = InputTextStyle.short,
        custom_id: str | None = None,
        label: str,
        placeholder: str | None = None,
        min_length: int | None = None,
        max_length: int | None = None,
        required: bool | None = True,
        value: str | None = None,
        row: int | None = None,
        id: int | None = None,
    ):
        super().__init__()
        if len(str(label)) > 45:
            raise ValueError("label must be 45 characters or fewer")
        if min_length and (min_length < 0 or min_length > 4000):
            raise ValueError("min_length must be between 0 and 4000")
        if max_length and (max_length < 0 or max_length > 4000):
            raise ValueError("max_length must be between 1 and 4000")
        if value and len(str(value)) > 4000:
            raise ValueError("value must be 4000 characters or fewer")
        if placeholder and len(str(placeholder)) > 100:
            raise ValueError("placeholder must be 100 characters or fewer")
        if not isinstance(custom_id, str) and custom_id is not None:
            raise TypeError(
                f"expected custom_id to be str, not {custom_id.__class__.__name__}"
            )
        custom_id = os.urandom(16).hex() if custom_id is None else custom_id

        self._underlying = InputTextComponent._raw_construct(
            type=ComponentType.input_text,
            style=style,
            custom_id=custom_id,
            label=label,
            placeholder=placeholder,
            min_length=min_length,
            max_length=max_length,
            required=required,
            value=value,
            id=id,
        )
        self._input_value = False
        self.row = row
        self._rendered_row: int | None = None

    def __repr__(self) -> str:
        attrs = " ".join(
            f"{key}={getattr(self, key)!r}" for key in self.__item_repr_attributes__
        )
        return f"<{self.__class__.__name__} {attrs}>"

    @property
    def type(self) -> ComponentType:
        return self._underlying.type

    @property
    def style(self) -> InputTextStyle:
        """The style of the input text field."""
        return self._underlying.style

    @property
    def id(self) -> int | None:
        """The input text's ID. If not provided by the user, it is set sequentially by Discord."""
        return self._underlying.id

    @style.setter
    def style(self, value: InputTextStyle):
        if not isinstance(value, InputTextStyle):
            raise TypeError(
                f"style must be of type InputTextStyle not {value.__class__.__name__}"
            )
        self._underlying.style = value

    @property
    def custom_id(self) -> str:
        """The ID of the input text field that gets received during an interaction."""
        return self._underlying.custom_id

    @custom_id.setter
    def custom_id(self, value: str):
        if not isinstance(value, str):
            raise TypeError(
                f"custom_id must be None or str not {value.__class__.__name__}"
            )
        self._underlying.custom_id = value

    @property
    def label(self) -> str:
        """The label of the input text field."""
        return self._underlying.label

    @label.setter
    def label(self, value: str):
        if not isinstance(value, str):
            raise TypeError(f"label should be str not {value.__class__.__name__}")
        if len(value) > 45:
            raise ValueError("label must be 45 characters or fewer")
        self._underlying.label = value

    @property
    def placeholder(self) -> str | None:
        """The placeholder text that is shown before anything is entered, if any."""
        return self._underlying.placeholder

    @placeholder.setter
    def placeholder(self, value: str | None):
        if value and not isinstance(value, str):
            raise TypeError(f"placeholder must be None or str not {value.__class__.__name__}")  # type: ignore
        if value and len(value) > 100:
            raise ValueError("placeholder must be 100 characters or fewer")
        self._underlying.placeholder = value

    @property
    def min_length(self) -> int | None:
        """The minimum number of characters that must be entered. Defaults to 0."""
        return self._underlying.min_length

    @min_length.setter
    def min_length(self, value: int | None):
        if value and not isinstance(value, int):
            raise TypeError(f"min_length must be None or int not {value.__class__.__name__}")  # type: ignore
        if value and (value < 0 or value) > 4000:
            raise ValueError("min_length must be between 0 and 4000")
        self._underlying.min_length = value

    @property
    def max_length(self) -> int | None:
        """The maximum number of characters that can be entered."""
        return self._underlying.max_length

    @max_length.setter
    def max_length(self, value: int | None):
        if value and not isinstance(value, int):
            raise TypeError(f"min_length must be None or int not {value.__class__.__name__}")  # type: ignore
        if value and (value <= 0 or value > 4000):
            raise ValueError("max_length must be between 1 and 4000")
        self._underlying.max_length = value

    @property
    def required(self) -> bool | None:
        """Whether the input text field is required or not. Defaults to ``True``."""
        return self._underlying.required

    @required.setter
    def required(self, value: bool | None):
        if not isinstance(value, bool):
            raise TypeError(f"required must be bool not {value.__class__.__name__}")  # type: ignore
        self._underlying.required = bool(value)

    @property
    def value(self) -> str | None:
        """The value entered in the text field."""
        if self._input_value is not False:
            # only False on init, otherwise the value was either set or cleared
            return self._input_value  # type: ignore
        return self._underlying.value

    @value.setter
    def value(self, value: str | None):
        if value and not isinstance(value, str):
            raise TypeError(f"value must be None or str not {value.__class__.__name__}")  # type: ignore
        if value and len(str(value)) > 4000:
            raise ValueError("value must be 4000 characters or fewer")
        self._underlying.value = value

    @property
    def width(self) -> int:
        return 5

    def to_component_dict(self) -> InputTextComponentPayload:
        return self._underlying.to_dict()

    def refresh_state(self, data) -> None:
        self._input_value = data["value"]
