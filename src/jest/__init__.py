def load_ipython_extension(ipython):
    """Called by IPython when this module is loaded as an IPython extension."""
    from src.jest.magic import _cell_magic

    ipython.register_magic_function(
        _cell_magic, magic_kind="cell", magic_name="jest"
    )