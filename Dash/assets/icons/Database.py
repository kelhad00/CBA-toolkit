from dash import dcc, html
import dash_svg as svg

def database_search_icon(color, width):
    return svg.Svg(
        viewBox="0 0 25 24",
        width=width,
        children=[
            svg.Path(
                fillRule="evenodd",
                clipRule="evenodd",
                d="M13.7695 17.6271C13.7695 15.7182 15.3174 14.1689 17.2277 14.1689C19.1383 14.1689 20.6849 15.7186 20.6849 17.6271C20.6849 18.313 20.4856 18.9478 20.1448 19.4846L21.1297 20.4694C21.4226 20.7623 21.4226 21.2372 21.1297 21.5301C20.8368 21.823 20.3619 21.823 20.069 21.5301L19.0854 20.5464C18.5492 20.8867 17.9117 21.0853 17.2277 21.0853C15.3174 21.0853 13.7695 19.536 13.7695 17.6271ZM18.6124 19.0165C18.9705 18.6492 19.1849 18.1644 19.1849 17.6271C19.1849 16.5459 18.3088 15.6689 17.2277 15.6689C16.1462 15.6689 15.2695 16.5463 15.2695 17.6271C15.2695 18.7079 16.1462 19.5853 17.2277 19.5853C17.7689 19.5853 18.2572 19.3677 18.6124 19.0165Z",
                fill=color
            ),
            svg.Path(
                fillRule="evenodd",
                clipRule="evenodd",
                d="M3.85352 5.27734C4.26773 5.27734 4.60352 5.61313 4.60352 6.02734V11.8128C4.60402 11.8165 4.60479 11.8215 4.60593 11.8278C4.61138 11.858 4.62531 11.9181 4.65942 11.9991C4.72559 12.1563 4.87781 12.4169 5.23631 12.7008C5.96432 13.2773 7.60107 13.9914 11.191 13.9914C11.6052 13.9914 11.941 14.3271 11.941 14.7414C11.941 15.1556 11.6052 15.4914 11.191 15.4914C7.44346 15.4914 5.41146 14.7528 4.3051 13.8767C3.74641 13.4343 3.44003 12.9686 3.27691 12.581C3.19636 12.3897 3.15297 12.2228 3.12976 12.0941C3.11817 12.0299 3.11161 11.9752 3.10795 11.9317C3.10612 11.9099 3.10501 11.891 3.10436 11.875L3.10369 11.8533L3.10356 11.8441L3.10353 11.84L3.10352 11.838C3.10352 11.8371 3.10352 11.8361 3.85352 11.8361H3.10352V6.02734C3.10352 5.61313 3.4393 5.27734 3.85352 5.27734Z",
                fill=color,
            ),
            svg.Path(
                fillRule="evenodd",
                clipRule="evenodd",
                d="M18.5293 5.27734C18.9435 5.27734 19.2793 5.61313 19.2793 6.02734V10.8682C19.2793 11.2825 18.9435 11.6182 18.5293 11.6182C18.1151 11.6182 17.7793 11.2825 17.7793 10.8682V6.02734C17.7793 5.61313 18.1151 5.27734 18.5293 5.27734Z",
                fill=color
            ),
            svg.Path(
                fillRule="evenodd",
                clipRule="evenodd",
                d="M3.85352 11.0859C4.26773 11.0859 4.60352 11.4217 4.60352 11.8359V17.6223C4.60402 17.6259 4.60479 17.6309 4.60593 17.6372C4.61137 17.6674 4.62529 17.7274 4.65939 17.8084C4.72554 17.9655 4.87773 18.2259 5.23622 18.5097C5.96424 19.0861 7.60103 19.7999 11.191 19.7999C11.6052 19.7999 11.941 20.1357 11.941 20.5499C11.941 20.9642 11.6052 21.2999 11.191 21.2999C7.44349 21.2999 5.41153 20.5617 4.30518 19.6858C3.74649 19.2435 3.44009 18.7779 3.27694 18.3905C3.19639 18.1991 3.15298 18.0322 3.12977 17.9036C3.11817 17.8393 3.11161 17.7846 3.10795 17.7412C3.10612 17.7194 3.10501 17.7005 3.10436 17.6845L3.10369 17.6627L3.10356 17.6536L3.10353 17.6495L3.10352 17.6475C3.10352 17.6465 3.10352 17.6456 3.85352 17.6456H3.10352V11.8359C3.10352 11.4217 3.4393 11.0859 3.85352 11.0859Z",
                fill=color
            ),
            svg.Path(
                fillRule="evenodd",
                clipRule="evenodd",
                d="M4.94696 5.34802C4.66965 5.6125 4.60352 5.81799 4.60352 5.95583C4.60352 6.09367 4.66965 6.29916 4.94696 6.56364C5.2261 6.82987 5.66992 7.10419 6.2802 7.35038C7.4968 7.84116 9.22907 8.16166 11.1808 8.16166C13.1325 8.16166 14.8648 7.84116 16.0814 7.35038C16.6917 7.10419 17.1355 6.82987 17.4146 6.56364C17.6919 6.29916 17.7581 6.09367 17.7581 5.95583C17.7581 5.81799 17.6919 5.6125 17.4146 5.34802C17.1355 5.08179 16.6917 4.80747 16.0814 4.56128C14.8648 4.0705 13.1325 3.75 11.1808 3.75C9.22907 3.75 7.4968 4.0705 6.2802 4.56128C5.66992 4.80747 5.2261 5.08179 4.94696 5.34802ZM5.71904 3.1702C7.15439 2.59118 9.08576 2.25 11.1808 2.25C13.2758 2.25 15.2072 2.59118 16.6425 3.1702C17.3582 3.45891 17.9875 3.82152 18.4499 4.26256C18.9141 4.70533 19.2581 5.27744 19.2581 5.95583C19.2581 6.63422 18.9141 7.20633 18.4499 7.64911C17.9875 8.09014 17.3582 8.45275 16.6425 8.74146C15.2072 9.32048 13.2758 9.66166 11.1808 9.66166C9.08576 9.66166 7.15439 9.32048 5.71904 8.74146C5.00336 8.45275 4.37412 8.09014 3.9117 7.64911C3.44745 7.20633 3.10352 6.63422 3.10352 5.95583C3.10352 5.27744 3.44745 4.70533 3.9117 4.26256C4.37412 3.82152 5.00336 3.45891 5.71904 3.1702Z",
                fill=color
            )
        ])