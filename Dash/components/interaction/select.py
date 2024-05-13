import dash_mantine_components as dmc

def select(options, label,id, allowDeselect=False, placeholder="Select an option", value=None):
    return dmc.Select(
            label=label,
            value=value,
            id=id,
            allowDeselect=allowDeselect,
            data=options,
            radius="md",
            placeholder=placeholder,
            classNames={
                "dropdown": "rounded-xl p-1",
                "label": "font-medium text-sm",
                "item": "hover:bg-gray-100 mb-2 last:mb-0 rounded-lg",
                "input": "focus:border-gray-500 px-5",
            },
            className="flex flex-col gap-2",

        )
