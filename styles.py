import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

        :root {
            --ink: #17251f;
            --muted: #61716a;
            --paper: #f6f3ec;
            --panel: #fffdf8;
            --line: #dfe4dc;
            --green: #1e6049;
            --mint: #d9eee2;
            --coral: #e9765b;
            --yellow: #f4c95d;
        }

        html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color: var(--ink); }
        .stApp { background: var(--paper); }
        [data-testid="stSidebar"] { background: #e7efe8; border-right: 1px solid var(--line); }
        [data-testid="stSidebar"] > div:first-child { padding: 2rem 1.35rem; }
        h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: 0 !important; }
        h1 { font-size: clamp(2.2rem, 4vw, 4.6rem) !important; line-height: .98 !important; }
        .eyebrow { color: var(--coral); font-size: .76rem; font-weight: 700; letter-spacing: .16em; text-transform: uppercase; }
        .hero-copy { max-width: 720px; color: var(--muted); font-size: 1.08rem; line-height: 1.6; }
        div[data-testid="stImage"] img { border-radius: 10px; height: 250px; object-fit: cover; width: 100%; }
        .travel-note { background: var(--mint); border-left: 4px solid var(--green); border-radius: 0 8px 8px 0; color: var(--green); padding: .85rem 1rem; }
        .brand { color: var(--green); font-family: 'Space Grotesk'; font-size: 1.25rem; font-weight: 700; letter-spacing: -.04em; margin-bottom: 3rem; }
        .brand span { color: var(--coral); }
        .section-label { color: var(--muted); font-size: .75rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; margin: 1.7rem 0 .65rem; }
        .result-head { border-top: 1px solid var(--line); margin-top: 2.8rem; padding-top: 2.2rem; }
        .route-pill { color: var(--green); background: var(--mint); border-radius: 99px; display: inline-block; font-size: .78rem; font-weight: 700; padding: .45rem .8rem; }
        .itinerary-card { background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 1.2rem 1.3rem; margin: .7rem 0; }
        .day-title { font-family: 'Space Grotesk'; font-size: 1.18rem; font-weight: 600; }
        .mini-stat { background: #edf4ef; border-radius: 8px; min-height: 96px; padding: 1rem; }
        .mini-stat strong { display: block; font-family: 'Space Grotesk'; font-size: 1.45rem; }
        .mini-stat span { color: var(--muted); font-size: .8rem; }
        .tip { background: #f7e7c0; border-left: 4px solid var(--yellow); border-radius: 0 7px 7px 0; padding: 1rem 1.1rem; }
        .stButton > button { border-radius: 5px; font-weight: 700; min-height: 2.8rem; }
        .stButton > button[kind="primary"] { background: var(--green); border-color: var(--green); }
        @media (max-width: 700px) {
            div[data-testid="stImage"] img { height: 190px; margin-top: 1rem; }
            h1 { font-size: 2.7rem !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
