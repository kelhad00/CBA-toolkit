from dash import dcc, html
import dash_svg as svg
def delete_icon(color, width):
    return svg.Svg(
        viewBox='0 0 24 24',
        width=width,
        children=[
            svg.G(
                id="Iconly/Light/Delete",
                fill="none",
                children=[
                    svg.G(
                        id="Delete",
                        transform="translate(3.000000, 2.000000)",
                        children=[
                            svg.Path(
                                d="M16.3249,7.4682 C16.3249,7.4682 15.7819,14.2032 15.4669,17.0402 C15.3169,18.3952 14.4799,19.1892 13.1089,19.2142 C10.4999,19.2612 7.8879,19.2642 5.2799,19.2092 C3.9609,19.1822 3.1379,18.3782 2.9909,17.0472 C2.6739,14.1852 2.1339,7.4682 2.1339,7.4682",
                                id="Stroke-1",
                                stroke=color,
                                strokeWidth="2"
                            ),
                            svg.Line(
                                x1="17.7082",
                                y1="4.2397",
                                x2="0.7502",
                                y2="4.2397",
                                id="Stroke-3",
                                stroke=color,
                                strokeWidth="2"
                            ),
                            svg.Path(
                                d="M14.4406,4.2397 C13.6556,4.2397 12.9796,3.6847 12.8256,2.9157 L12.5826,1.6997 C12.4326,1.1387 11.9246,0.7507 11.3456,0.7507 L7.1126,0.7507 C6.5336,0.7507 6.0256,1.1387 5.8756,1.6997 L5.6326,2.9157 C5.4786,3.6847 4.8026,4.2397 4.0176,4.2397",
                                id="Stroke-5",
                                stroke=color,
                                strokeWidth="2"
                            )
                        ]
                    )
                ]
            )
        ]
    )

