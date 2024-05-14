import dash_mantine_components as dmc


def radio(id, options, label, value=None):
    return dmc.RadioGroup(
        [dmc.Radio(l, value=k) for k, l in options],
        id=id,
        value=value,
        label=label,
    )
