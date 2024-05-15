import dash_svg as svg


def home_icon(color, width):
    return svg.Svg(
        viewBox="0 0 24 24",
        width=width,
        fill="none",
        children=[
            svg.Path(
                d="M14.5003 3.89485L19.5522 8.02962C20.6727 8.94684 21.2019 10.4049 20.9295 11.8269L19.7867 17.7912C19.4307 19.6509 17.8034 20.9961 15.9096 20.9961H8.08947C6.1957 20.9961 4.56942 19.6509 4.21245 17.7912L3.07055 11.8269C2.79821 10.4049 3.32636 8.94684 4.44686 8.02962L9.49885 3.89485C10.9539 2.70432 13.0461 2.70432 14.5003 3.89485Z",
                stroke=color,
                strokeWidth="1.5",
                strokeLinecap="round",
                strokeLinejoin="round"
            ),
            svg.Path(
                d="M8.80469 14.1348C9.58184 15.1463 10.7267 15.7776 11.997 15.7776C13.2682 15.7776 14.413 15.1463 15.1902 14.1348",
                stroke=color,
                strokeWidth="1.5",
                strokeLinecap="round",
                strokeLinejoin="round"
            )
        ]
    )
