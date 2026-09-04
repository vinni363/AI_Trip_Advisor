import os
from datetime import date, timedelta

from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

from rag import generate_plan
from travel_knowledge import estimate_daily_budget, format_context, retrieve_city_context, short_city_name_error
from styles import apply_styles

load_dotenv()


st.set_page_config(
    page_title="Wanderwise | AI Trip Advisor",
    page_icon="✈",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_styles()


with st.sidebar:
    st.markdown('<div class="brand">wander<span>wise</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Your trip</div>', unsafe_allow_html=True)
    destination = st.text_input("Destination city", value="Kochi", placeholder="e.g. Kochi", label_visibility="visible")
    start_day = date.today() + timedelta(days=14)
    days = st.slider("Length of stay", 2, 10, 5, format="%d days")
    travel_style = "Slow & local"
    budget, has_city_budget = estimate_daily_budget(destination)
    budget_note = "based on this city's typical travel costs" if has_city_budget else "planning estimate; verify local costs"
    st.caption(f"A {days}-day slow and local plan, estimated at ₹{budget * days:,} total ({budget_note}).")
    api_key = os.getenv("OPENROUTER_API_KEY", "") or os.getenv("OPENAI_API_KEY", "")
    is_openrouter = api_key.startswith("sk-or-")

st.markdown('<div class="eyebrow">A better way to wander</div>', unsafe_allow_html=True)
hero_copy, hero_image = st.columns([1.15, .85], gap="large")
with hero_copy:
    st.title("Make room for the\nmemorable bits.")
    st.markdown(
        '<p class="hero-copy">Plan a thoughtful trip around the places, stays, and tables that make a destination feel alive.</p>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="travel-note"><strong>Built for curious travellers.</strong><br>Recommendations are grounded in destination knowledge and current web sources when needed.</div>', unsafe_allow_html=True)
with hero_image:
    st.image(
        "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1200&q=85",
        caption="Kerala backwaters, a slower way to travel",
        use_container_width=True,
    )

if st.button("Build my trip", type="primary", use_container_width=False):
    if not api_key.strip():
        st.session_state["trip_error"] = "Add OPENAI_API_KEY or OPENROUTER_API_KEY to your local .env file, then restart the app."
        st.session_state["trip_built"] = False
    else:
        try:
            with st.spinner("Finding the right details and shaping your route..."):
                city_error = short_city_name_error(destination)
                if city_error:
                    raise ValueError(city_error)
                context_records = retrieve_city_context(destination)
                if context_records:
                    context = format_context(context_records)
                    source_labels = [record["place"] for record in context_records]
                    model = "openai/gpt-4o-mini"
                    web_search = False
                else:
                    if not is_openrouter:
                        raise ValueError("Web search for an unknown city requires an OpenRouter API key.")
                    context = (
                        f"Live web research is required for {destination}. Search specifically for this city: "
                        "attractions, hotels, restaurants, transport, and safety. "
                        "Do not use generic information about another city."
                    )
                    source_labels = ["OpenRouter web search"]
                    model = "openai/gpt-4o-mini:online"
                    web_search = True
                client_kwargs = {"api_key": api_key.strip()}
                if is_openrouter:
                    client_kwargs["base_url"] = "https://openrouter.ai/api/v1"
                st.session_state["trip_plan"] = generate_plan(
                    OpenAI(**client_kwargs),
                    model,
                    destination,
                    days,
                    travel_style,
                    budget,
                    start_day,
                    context,
                    web_search,
                )
                st.session_state["trip_sources"] = source_labels
                st.session_state["trip_built"] = True
                st.session_state.pop("trip_error", None)
        except Exception as error:
            st.session_state["trip_error"] = f"The AI request could not be completed: {error}"
            st.session_state["trip_built"] = False

if st.session_state.get("trip_error"):
    st.error(st.session_state["trip_error"])

if st.session_state.get("trip_built"):
    st.markdown('<div class="result-head"></div>', unsafe_allow_html=True)
    col_title, col_tag = st.columns([3, 1])
    with col_title:
        st.markdown(f"## {destination.strip().title() or 'Lisbon'}, your way")
        st.caption(f"{days} days · {travel_style.lower()} · estimated total ₹{budget * days:,}")
    with col_tag:
        st.markdown('<div class="route-pill">✦ Just for you</div>', unsafe_allow_html=True)

    stats = st.columns(3)
    for column, value, label in zip(stats, [f"₹{budget * days:,}", f"{days * 2 + 1}", "flexible"], ["estimated trip total", "anchor moments", "pace"]):
        with column:
            st.markdown(f'<div class="mini-stat"><strong>{value}</strong><span>{label}</span></div>', unsafe_allow_html=True)

    left, right = st.columns([1.5, 1], gap="large")
    with left:
        st.markdown("### Your rhythm")
        st.markdown(st.session_state["trip_plan"])
        sources = st.session_state.get("trip_sources", [])
        if sources:
            st.caption("Grounded in: " + ", ".join(sources))
    with right:
        st.markdown("### Keep in mind")
        st.markdown('<div class="tip"><strong>Leave one afternoon open.</strong><br><span style="color:#6a614d;">The best travel stories tend to arrive when the schedule has somewhere to put them.</span></div>', unsafe_allow_html=True)
        st.markdown("### Bring along")
        essentials = ["Comfortable walking shoes", "A light layer for late evenings", "A reusable water bottle", "One outfit that feels like you"]
        for item in essentials:
            st.checkbox(item, value=True, key=f"pack_{item}")
else:
    st.markdown("### Start with a destination")
    st.caption("Choose a city and trip length. Wanderwise will shape a practical route with places to visit, stay, and eat.")
    preview_cols = st.columns(3)
    for column, title, text in zip(
        preview_cols,
        ["Go deeper", "Taste widely", "Move lightly"],
        ["Small streets, local rituals, unhurried mornings.", "Markets, memorable tables, and one more bite.", "A thoughtful route with room to follow the light."],
    ):
        with column:
            st.markdown(f'<div class="itinerary-card"><div class="day-title">{title}</div><p style="color:#61716a;">{text}</p></div>', unsafe_allow_html=True)
