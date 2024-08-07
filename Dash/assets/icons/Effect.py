# <svg width="24px"  height="24px"  viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
# <circle cx="5.2917" cy="4.83858" r="1.9167" stroke="#000000"  stroke-width="1.5"  stroke-linecap="round" stroke-linejoin="round"/>
# <circle cx="10.0837" cy="9.62959" r="1.9167" stroke="#000000"  stroke-width="1.5"  stroke-linecap="round" stroke-linejoin="round"/>
# <path d="M6.67871 6.16797L8.7386 8.22786" stroke="#000000"  stroke-width="1.5"  stroke-linecap="round" stroke-linejoin="round"/>
# <path d="M15.1472 19.3145C14.1562 19.8355 13.8496 21.5009 13.8496 21.5009" stroke="#000000"  stroke-width="1.5"  stroke-linecap="round"/>
# <path
# d="M11.4707 2.50345C13.3472 2.46169 15.1285 2.78923 16.5952 4.02633C18.4783 5.61445 19.5797 7.55752 19.0094 10.1413C18.7054 11.5186 19.711 13.083 20.4235 14.0401C20.7372 14.4615 20.5791 15.026 20.0889 15.215L19.1614 15.5727C18.8938 15.6759 18.6983 15.9098 18.6443 16.1914L18.334 18.8346C18.2311 19.5205 17.648 19.8464 16.9964 19.7092L14.2119 19.0814C13.3014 18.8807 13.3413 18.0571 13.1034 17.1952" stroke="#000000"  stroke-width="1.5"  stroke-linecap="round"/>

# <path d="M4.26855 12.8633C5.72377 15.468 6.39593 18.4308 5.15331 21.2646" stroke="#000000"  stroke-width="1.5"  stroke-linecap="round"/>
# </svg>

import dash_svg as svg

def effect_icon(width, color):
    return svg.Svg(
        width=width,
        viewBox="0 0 24 24",
        fill="none",
        children=[
            svg.Circle(
                cx="5.2917",
                cy="4.83858",
                r="1.9167",
                stroke=color,
                strokeWidth="1.5",
            ),
            svg.Circle(
                cx="10.0837",
                cy="9.62959",
                r="1.9167",
                stroke=color,
                strokeWidth="1.5",
            ),
            svg.Path(
                d="M6.67871 6.16797L8.7386 8.22786",
                stroke=color,
                strokeWidth="1.5",
                strokeLinecap="round",
                strokeLinejoin="round"
            ),
            svg.Path(
                d="M15.1472 19.3145C14.1562 19.8355 13.8496 21.5009 13.8496 21.5009",
                stroke=color,
                strokeWidth="1.5",
                strokeLinecap="round"
            ),
            svg.Path(
                d="M11.4707 2.50345C13.3472 2.46169 15.1285 2.78923 16.5952 4.02633C18.4783 5.61445 19.5797 7.55752 19.0094 10.1413C18.7054 11.5186 19.711 13.083 20.4235 14.0401C20.7372 14.4615 20.5791 15.026 20.0889 15.215L19.1614 15.5727C18.8938 15.6759 18.6983 15.9098 18.6443 16.1914L18.334 18.8346C18.2311 19.5205 17.648 19.8464 16.9964 19.7092L14.2119 19.0814C13.3014 18.8807 13.3413 18.0571 13.1034 17.1952",
                stroke=color,
                strokeWidth="1.5",
                strokeLinecap="round",
            ),
            svg.Path(
                d="M4.26855 12.8633C5.72377 15.468 6.39593 18.4308 5.15331 21.2646",
                stroke=color,
                strokeWidth="1.5",
                strokeLinecap="round"
            ),
        ]
    )



