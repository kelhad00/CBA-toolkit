# <svg width="24px"  height="24px"  viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
# <path d="M15.8108 10.3828C18.6733 10.3828 20.9996 12.7092 20.9996 15.5813C20.9996 18.4438 18.6733 20.7701 15.8108 20.7701C12.9387 20.7701 10.6123 18.4438 10.6123 15.5813" stroke="#000000"  stroke-width="1.5"  stroke-linecap="round" stroke-linejoin="round"/>
# <path d="M8.19659 13.6236C11.0668 13.6236 13.3932 11.2973 13.3932 8.42706C13.3932 5.55682 11.0668 3.23047 8.19659 3.23047C5.32635 3.23047 3 5.55682 3 8.42706C3 11.2973 5.32635 13.6236 8.19659 13.6236Z" stroke="#000000"  stroke-width="1.5"  stroke-linecap="round" stroke-linejoin="round"/>
# <path d="M6.75684 6.86307V6.80469M9.69092 6.80469V6.86307" stroke="#000000"  stroke-width="1.5"  stroke-linecap="round" stroke-linejoin="round"/>
# <path d="M6.74023 9.55469C7.05645 9.99739 7.59255 10.2795 8.1987 10.2795C8.80486 10.2795 9.34096 9.99739 9.65717 9.55469" stroke="#000000"  stroke-width="1.5"  stroke-linecap="round" stroke-linejoin="round"/>
# <path d="M14.3682 14.0086V13.9609M17.3023 14.0052V13.9643" stroke="#000000"  stroke-width="1.5"  stroke-linecap="round" stroke-linejoin="round"/>
# <path d="M14.3506 17.4241C14.6668 16.9814 15.2029 16.6992 15.8091 16.6992C16.4152 16.6992 16.9513 16.9814 17.2675 17.4241" stroke="#000000"  stroke-width="1.5"  stroke-linecap="round" stroke-linejoin="round"/>
# <path d="M4.82617 16.2734C4.82617 17.8856 6.13286 19.1923 7.74506 19.1923" stroke="#000000"  stroke-width="1.5"  stroke-linecap="round" stroke-linejoin="round"/>
# <path d="M19.1757 7.72357C19.1757 6.11137 17.869 4.80469 16.2568 4.80469" stroke="#000000"  stroke-width="1.5"  stroke-linecap="round" stroke-linejoin="round"/>
# </svg>

import dash_svg as svg

def mimicry_icon(width, color):
    return svg.Svg(
        width=width,
        viewBox="0 0 24 24",
        fill="none",
        children=[
            svg.Path(
                d="M15.8108 10.3828C18.6733 10.3828 20.9996 12.7092 20.9996 15.5813C20.9996 18.4438 18.6733 20.7701 15.8108 20.7701C12.9387 20.7701 10.6123 18.4438 10.6123 15.5813",
                stroke=color,
                strokeWidth="1.5",
                strokeLinecap="round",
                strokeLinejoin="round"
            ),
            svg.Path(
                d="M8.19659 13.6236C11.0668 13.6236 13.3932 11.2973 13.3932 8.42706C13.3932 5.55682 11.0668 3.23047 8.19659 3.23047C5.32635 3.23047 3 5.55682 3 8.42706C3 11.2973 5.32635 13.6236 8.19659 13.6236Z",
                stroke=color,
                strokeWidth="1.5",
                strokeLinecap="round",
                strokeLinejoin="round"
            ),
            svg.Path(
                d="M6.75684 6.86307V6.80469",
                stroke=color,
                strokeWidth="1.5",
                strokeLinecap="round",
                strokeLinejoin="round"
            ),
            svg.Path(
                d="M9.69092 6.80469V6.86307",
                stroke=color,
                strokeWidth="1.5",
                strokeLinecap="round",
                strokeLinejoin="round"
            ),
            svg.Path(
                d="M6.74023 9.55469C7.05645 9.99739 7.59255 10.2795 8.1987 10.2795C8.80486 10.2795 9.34096 9.99739 9.65717 9.55469",
                stroke=color,
                strokeWidth="1.5",
                strokeLinecap="round",
                strokeLinejoin="round"
            ),
            svg.Path(
                d="M14.3682 14.0086V13.9609",
                stroke=color,
                strokeWidth="1.5",
                strokeLinecap="round",
                strokeLinejoin="round"
            ),
            svg.Path(
                d="M17.3023 14.0052V13.9643",
                stroke=color,
                strokeWidth="1.5",
                strokeLinecap="round",
                strokeLinejoin="round"
            ),
            svg.Path(
                d="M14.3506 17.4241C14.6668 16.9814 15.2029 16.6992 15.8091 16.6992C16.4152 16.6992 16.9513 16.9814 17.2675 17.4241",
                stroke=color,
                strokeWidth="1.5",
                strokeLinecap="round",
                strokeLinejoin="round"
            ),
            svg.Path(
                d="M4.82617 16.2734C4.82617 17.8856 6.13286 19.1923 7.74506 19.1923",
                stroke=color,
                strokeWidth="1.5",
                strokeLinecap="round",
                strokeLinejoin="round"
            ),
            svg.Path(
                d="M19.1757 7.72357C19.1757 6.11137 17.869 4.80469 16.2568 4.80469",
                stroke=color,
                strokeWidth="1.5",
                strokeLinecap="round",
                strokeLinejoin="round"
            )
        ]
    )
