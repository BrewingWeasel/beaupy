from unittest import mock

from beaupy import _beaupy as b
from yakh.key import Keys
from ward import raises, test

from beaupy._beaupy import Config, Live, select_multiple, warnings
import beaupy


def raise_keyboard_interrupt():
    raise KeyboardInterrupt()


@test("`select_multiple` with no options permissive")
def _():
    b.get_key = lambda: Keys.ENTER
    res = select_multiple(options=[])
    assert res == []


@test("`select_multiple` with no options strict")
def _():
    b.get_key = lambda: Keys.ENTER
    with raises(ValueError) as e:
        select_multiple(options=[], strict=True)

    assert str(e.raised) == "`options` cannot be empty"


@test("`select_multiple` with 2 options starting from first selecting going down and selecting second also")
def _():
    steps = iter([' ', Keys.DOWN_ARROW, ' ', Keys.ENTER])

    b.get_key = lambda: next(steps)
    Live.update = mock.MagicMock()
    res = select_multiple(options=["test1", "test2"], tick_character="😋")
    assert Live.update.call_args_list == [
        mock.call(
            renderable="\\[  ] [pink1]test1[/pink1]\n\\[  ] test2\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
        mock.call(
            renderable="\\[[pink1]😋[/pink1]] [pink1]test1[/pink1]\n\\[  ] test2\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
        mock.call(
            renderable="\\[[pink1]😋[/pink1]] test1\n\\[  ] [pink1]test2[/pink1]\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
        mock.call(
            renderable="\\[[pink1]😋[/pink1]] test1\n\\[[pink1]😋[/pink1]] [pink1]test2[/pink1]\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
    ]
    assert Live.update.call_count == 4
    assert res == ["test1", "test2"]


@test("`select_multiple` with 2 options pressing escape")
def _():
    steps = iter([Keys.ESC])

    b.get_key = lambda: next(steps)
    Live.update = mock.MagicMock()
    res = select_multiple(options=["test1", "test2"], tick_character="😋")
    assert Live.update.call_args_list == [
        mock.call(
            renderable="\\[  ] [pink1]test1[/pink1]\n\\[  ] test2\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
    ]
    assert Live.update.call_count == 1
    assert res == []



@test("`select_multiple` with 2 options starting from first selecting going down, selecting second one and going down again")
def _():
    steps = iter([' ', Keys.DOWN_ARROW, ' ', Keys.DOWN_ARROW, Keys.ENTER])

    b.get_key = lambda: next(steps)
    Live.update = mock.MagicMock()
    res = select_multiple(options=["test1", "test2"], tick_character="😋")
    assert Live.update.call_args_list == [
        mock.call(
            renderable="\\[  ] [pink1]test1[/pink1]\n\\[  ] test2\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
        mock.call(
            renderable="\\[[pink1]😋[/pink1]] [pink1]test1[/pink1]\n\\[  ] test2\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
        mock.call(
            renderable="\\[[pink1]😋[/pink1]] test1\n\\[  ] [pink1]test2[/pink1]\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
        mock.call(
            renderable="\\[[pink1]😋[/pink1]] test1\n\\[[pink1]😋[/pink1]] [pink1]test2[/pink1]\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
        mock.call(
            renderable="\\[[pink1]😋[/pink1]] [pink1]test1[/pink1]\n\\[[pink1]😋[/pink1]] test2\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
    ]
    assert Live.update.call_count == 5
    assert res == ["test1", "test2"]



@test("`select_multiple` with 2 options starting from first selecting going up and selecting again")
def _():
    steps = iter([' ', Keys.UP_ARROW, ' ', Keys.ENTER])

    b.get_key = lambda: next(steps)
    Live.update = mock.MagicMock()
    res = select_multiple(options=["test1", "test2"], tick_character="😋")
    assert Live.update.call_args_list == [
        mock.call(
            renderable="\\[  ] [pink1]test1[/pink1]\n\\[  ] test2\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
        mock.call(
            renderable="\\[[pink1]😋[/pink1]] [pink1]test1[/pink1]\n\\[  ] test2\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
        mock.call(
            renderable="\\[[pink1]😋[/pink1]] test1\n\\[  ] [pink1]test2[/pink1]\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
        mock.call(
            renderable="\\[[pink1]😋[/pink1]] test1\n\\[[pink1]😋[/pink1]] [pink1]test2[/pink1]\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
    ]
    assert Live.update.call_count == 4
    assert res == ['test1', 'test2']


@test(
    "`select_multiple` with 2 options starting from first selecting going down and selecting second also with return_indices as True",
)
def _():
    steps = iter([' ', Keys.DOWN_ARROW, ' ', Keys.ENTER])

    b.get_key = lambda: next(steps)
    Live.update = mock.MagicMock()
    res = select_multiple(options=["test1", "test2"], tick_character="😋", return_indices=True)
    assert Live.update.call_args_list == [
        mock.call(
            renderable="\\[  ] [pink1]test1[/pink1]\n\\[  ] test2\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
        mock.call(
            renderable="\\[[pink1]😋[/pink1]] [pink1]test1[/pink1]\n\\[  ] test2\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
        mock.call(
            renderable="\\[[pink1]😋[/pink1]] test1\n\\[  ] [pink1]test2[/pink1]\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
        mock.call(
            renderable="\\[[pink1]😋[/pink1]] test1\n\\[[pink1]😋[/pink1]] [pink1]test2[/pink1]\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
    ]
    assert Live.update.call_count == 4
    assert res == [0, 1]


@test("`select_multiple` with moving down then pressing home and selecting first")
def _():
    steps = iter([Keys.DOWN_ARROW, Keys.HOME, ' ', Keys.ENTER])
    b.get_key = lambda: next(steps)
    Live.update = mock.MagicMock()
    res = select_multiple(options=["test1", "test2"], tick_character="😋")

    assert Live.update.call_args_list == [
        mock.call(
            renderable="\\[  ] [pink1]test1[/pink1]\n\\[  ] test2\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
        mock.call(
            renderable="\\[  ] test1\n\\[  ] [pink1]test2[/pink1]\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
        mock.call(
            renderable="\\[  ] [pink1]test1[/pink1]\n\\[  ] test2\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
       mock.call(
            renderable="\\[[pink1]😋[/pink1]] [pink1]test1[/pink1]\n\\[  ] test2\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
    ]

    assert Live.update.call_count == 4
    assert res == ["test1"]


@test("`select_multiple` with pressing end and selecting last")
def _():
    steps = iter([Keys.END, ' ', Keys.ENTER])
    b.get_key = lambda: next(steps)
    Live.update = mock.MagicMock()
    res = select_multiple(options=["test1", "test2"], tick_character="😋")

    assert Live.update.call_args_list == [
        mock.call(
            renderable="\\[  ] [pink1]test1[/pink1]\n\\[  ] test2\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
        mock.call(
            renderable="\\[  ] test1\n\\[  ] [pink1]test2[/pink1]\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
        mock.call(
            renderable="\\[  ] test1\n\\[[pink1]😋[/pink1]] [pink1]test2[/pink1]\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
    ]

    assert Live.update.call_count == 3
    assert res == ["test2"]


@test(
    "`select_multiple` with 2 options `x` as tick character and yellow1 as color starting from second selecting and going up",
)
def _():
    steps = iter([' ', Keys.UP_ARROW, Keys.ENTER])

    b.get_key = lambda: next(steps)
    Live.update = mock.MagicMock()
    res = select_multiple(
        options=["test1", "test2"],
        tick_character="x",
        tick_style="yellow1",
        cursor_index=1,
    )
    assert Live.update.call_args_list == [
        mock.call(renderable="\\[ ] test1\n\\[ ] [pink1]test2[/pink1]\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"),
        mock.call(
            renderable="\\[ ] test1\n\\[[yellow1]x[/yellow1]] [pink1]test2[/pink1]\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
        mock.call(
            renderable="\\[ ] [pink1]test1[/pink1]\n\\[[yellow1]x[/yellow1]] test2\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
    ]
    assert Live.update.call_count == 3
    assert res == ["test2"]


@test(
    "`select_multiple` with 2 options `x` as tick character and yellow1 as color starting from second selecting and going up with 1st option preselected",
)
def _():
    steps = iter([' ', Keys.UP_ARROW, Keys.ENTER])

    b.get_key = lambda: next(steps)
    Live.update = mock.MagicMock()
    res = select_multiple(
        options=["test1", "test2"],
        tick_character="x",
        tick_style="yellow1",
        cursor_index=1,
        ticked_indices=[0],
    )
    assert Live.update.call_args_list == [
        mock.call(
            renderable="\\[[yellow1]x[/yellow1]] test1\n\\[ ] [pink1]test2[/pink1]\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
        mock.call(
            renderable="\\[[yellow1]x[/yellow1]] test1\n\\[[yellow1]x[/yellow1]] [pink1]test2[/pink1]\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
        mock.call(
            renderable="\\[[yellow1]x[/yellow1]] [pink1]test1[/pink1]\n\\[[yellow1]x[/yellow1]] test2\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
    ]
    assert Live.update.call_count == 3
    assert res == ["test1", "test2"]


@test(
    "`select_multiple` with 2 options starting from first selecting going down and selecting second also with `maximal_count` of 1",
)
def _():
    steps = iter([' ', Keys.DOWN_ARROW, ' ', Keys.ENTER])

    b.get_key = lambda: next(steps)
    Live.update = mock.MagicMock()
    res = select_multiple(options=["test1", "test2"], tick_character="😋", maximal_count=1)

    assert Live.update.call_args_list[:4] == [
        mock.call(
            renderable="\\[  ] [pink1]test1[/pink1]\n\\[  ] test2\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
        mock.call(
            renderable="\\[[pink1]😋[/pink1]] [pink1]test1[/pink1]\n\\[  ] test2\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
        mock.call(
            renderable="\\[[pink1]😋[/pink1]] test1\n\\[  ] [pink1]test2[/pink1]\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
        mock.call(
            renderable="\\[[pink1]😋[/pink1]] test1\n\\[  ] [pink1]test2[/pink1]\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])\n[red]Error:[/red] Must select at most 1 options"
        ),
    ]
    assert Live.update.call_count == 4
    assert res == ["test1"]


@test(
    "`select_multiple` with 2 options starting from first selecting going down and selecting second also with `minimal_count` of 2",
)
def _():
    steps = iter(
        [
            ' ',
            Keys.DOWN_ARROW,
            Keys.ENTER,
            ' ',
            Keys.ENTER,
        ]
    )

    b.get_key = lambda: next(steps)
    Live.update = mock.MagicMock()
    res = select_multiple(options=["test1", "test2"], tick_character="😋", minimal_count=2)
    assert Live.update.call_args_list == [
        mock.call(
            renderable="\\[  ] [pink1]test1[/pink1]\n\\[  ] test2\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
        mock.call(
            renderable="\\[[pink1]😋[/pink1]] [pink1]test1[/pink1]\n\\[  ] test2\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
        mock.call(
            renderable="\\[[pink1]😋[/pink1]] test1\n\\[  ] [pink1]test2[/pink1]\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
        mock.call(
            renderable="\\[[pink1]😋[/pink1]] test1\n\\[  ] [pink1]test2[/pink1]\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])\n[red]Error:[/red] Must select at least 2 options"
        ),
        mock.call(
            renderable="\\[[pink1]😋[/pink1]] test1\n\\[[pink1]😋[/pink1]] [pink1]test2[/pink1]\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
    ]
    assert Live.update.call_count == 5
    assert res == ["test1", "test2"]


@test("`select_multiple` with 2 options and calling `Ctrl+C` with raise on keyboard interrupt False")
def _():
    Config.raise_on_interrupt = False
    Live.update = mock.MagicMock()
    b.get_key = lambda: Keys.CTRL_C
    res = select_multiple(options=["test1", "test2"], tick_character="😋")
    assert Live.update.call_args_list == [
        mock.call(renderable="\\[  ] [pink1]test1[/pink1]\n\\[  ] test2\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])")
    ]
    assert Live.update.call_count == 1
    assert res == []


@test("`select_multiple` with 2 options and calling `Ctrl+C` with raise on keyboard interrupt True")
def _():
    Config.raise_on_interrupt = True
    Live.update = mock.MagicMock()
    b.get_key = lambda: Keys.CTRL_C
    with raises(KeyboardInterrupt):
        select_multiple(options=["test1", "test2"], tick_character="😋")


@test("`select_multiple` with 2 options and invalid tick style")
def _():
    steps = iter([Keys.ENTER])
    b.get_key = lambda: next(steps)
    warnings.warn = mock.MagicMock()
    select_multiple(options=["test1", "test2"], tick_style="")
    warnings.warn.assert_called_once_with("`tick_style` should be a valid style, defaulting to `white`")


@test("`select_multiple` with 2 options and invalid cursor style")
def _():
    steps = iter([Keys.ENTER])
    b.get_key = lambda: next(steps)
    warnings.warn = mock.MagicMock()
    select_multiple(options=["test1", "test2"], cursor_style="")
    warnings.warn.assert_called_once_with("`cursor_style` should be a valid style, defaulting to `white`")


@test(
    "`select_multiple` with 2 options starting from first selecting going down and selecting second, then deselecting, with preprocessor",
)
def _():
    steps = iter([' ', Keys.DOWN_ARROW, ' ', ' ', Keys.ENTER])

    b.get_key = lambda: next(steps)
    Live.update = mock.MagicMock()
    res = select_multiple(options=["test1", "test2"], tick_character="😋", preprocessor=lambda val: val[-1])
    assert Live.update.call_args_list == [
        mock.call(renderable="\\[  ] [pink1]1[/pink1]\n\\[  ] 2\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"),
        mock.call(
            renderable="\\[[pink1]😋[/pink1]] [pink1]1[/pink1]\n\\[  ] 2\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
        mock.call(
            renderable="\\[[pink1]😋[/pink1]] 1\n\\[  ] [pink1]2[/pink1]\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
        mock.call(
            renderable="\\[[pink1]😋[/pink1]] 1\n\\[[pink1]😋[/pink1]] [pink1]2[/pink1]\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
        mock.call(
            renderable="\\[[pink1]😋[/pink1]] 1\n\\[  ] [pink1]2[/pink1]\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
    ]
    assert Live.update.call_count == 5
    assert res == ["test1"]

@test(
    "`select_multiple` return `[]` when ESC is pressed"
)
def _():
    steps = iter([' ', Keys.ESC])

    b.get_key = lambda: next(steps)
    Live.update = mock.MagicMock()
    res = select_multiple(options=["test1", "test2"], tick_character="😋", return_indices=True)
    assert Live.update.call_args_list == [
        mock.call(
            renderable="\\[  ] [pink1]test1[/pink1]\n\\[  ] test2\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
        mock.call(
            renderable="\\[[pink1]😋[/pink1]] [pink1]test1[/pink1]\n\\[  ] test2\n\n(Mark with [bold]space[/bold], confirm with [bold]enter[/bold])"
        ),
    ]
    assert Live.update.call_count == 2
    assert res == []
