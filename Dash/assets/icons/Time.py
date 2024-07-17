import dash_svg as svg
def time_icon(color, width):
    return svg.Svg(
        viewBox="0 0 24 24",
        width=width,
        fill="none",
        children=[
            svg.G(
                id="Iconly/Light/Time Circle",
                fill="none",
                children=[
                    svg.G(
                        id="Time-Circle",
                        transform="translate(2.000000, 2.000000)",
                        children=[
                            svg.Path(
                                d="M19.2498,10.0005 C19.2498,15.1095 15.1088,19.2505 9.9998,19.2505 C4.8908,19.2505 0.7498,15.1095 0.7498,10.0005 C0.7498,4.8915 4.8908,0.7505 9.9998,0.7505 C15.1088,0.7505 19.2498,4.8915 19.2498,10.0005 Z",
                                id="Stroke-1",
                                strokeWidth="1.5",
                                stroke=color,

                            ),
                            svg.Polyline(
                                points="13.4314 12.9429 9.6614 10.6939 9.6614 5.8469",
                                id="Stroke-3",
                                strokeWidth="1.5",
                                stroke=color,
                            )
                        ]
                    )
                ]
            )
        ]
    )