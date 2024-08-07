# <svg width="24px"  height="24px"  viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
# <path d="M11.6337 14.8767V10.8504M11.6289 8.03731V7.9585" stroke="#000000"  stroke-width="1.5"  stroke-linecap="round" stroke-linejoin="round"/>
# <path d="M3.21484 11.4171C3.21484 16.0659 6.98312 19.8351 11.6319 19.8351C16.2807 19.8351 20.049 16.0659 20.049 11.4171C20.049 6.76827 16.2807 3 11.6319 3C8.36901 3 5.53989 4.85639 4.14305 7.57067" stroke="#000000"  stroke-width="1.5"  stroke-linecap="round" stroke-linejoin="round"/>
# <path d="M17.3604 17.584L20.7853 21.0002" stroke="#000000"  stroke-width="1.5"  stroke-linecap="round" stroke-linejoin="round"/>
# </svg>
import dash_svg as svg

def information_icon(color, width):
    return svg.Svg(
        viewBox="0 0 24 24",
        width=width,
        fill="none",
        children=[
            svg.Path(
                d="M11.6337 14.8767V10.8504",
                stroke=color,
                strokeWidth="1.5",
                strokeLinecap="round",
                strokeLinejoin="round"
            ),
            svg.Path(
                d="M11.6289 8.03731V7.9585",
                stroke=color,
                strokeWidth="1.5",
                strokeLinecap="round",
                strokeLinejoin="round"
            ),
            svg.Path(
                d="M3.21484 11.4171C3.21484 16.0659 6.98312 19.8351 11.6319 19.8351C16.2807 19.8351 20.049 16.0659 20.049 11.4171C20.049 6.76827 16.2807 3 11.6319 3C8.36901 3 5.53989 4.85639 4.14305 7.57067",
                stroke=color,
                strokeWidth="1.5",
                strokeLinecap="round",
                strokeLinejoin="round"
            ),
            svg.Path(
                d="M17.3604 17.584L20.7853 21.0002",
                stroke=color,
                strokeWidth="1.5",
                strokeLinecap="round",
                strokeLinejoin="round"
            )
        ]
    )