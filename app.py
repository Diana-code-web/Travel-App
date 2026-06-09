import streamlit as st
import streamlit.components.v1 as components

from modules.auth          import (init_db, register_user, login_user,
                                   get_user_profile, save_itinerary,
                                   get_user_itineraries, update_user_name,
                                   delete_itinerary)
from modules.recommender   import load_destinations, recommend_destinations
from modules.itinerary     import generate_itinerary
from modules.budget        import calculate_budget
from modules.chatbot       import chat_with_assistant
from modules.api_handler   import (get_weather, get_weather_emoji,
                                   get_coordinates, get_multiple_coordinates)
from modules.map_component import create_single_map, create_multi_map
from modules.currency      import (get_exchange_rates, convert_currency,
                                   get_destination_currency, format_currency,
                                   SUPPORTED_CURRENCIES, BASE_CURRENCY)
from styles import load_css

# ── Init ─────────────────────────────────────────────────────
st.set_page_config(page_title="AI Travel Assistant", page_icon="🌍", layout="centered")
st.markdown(load_css(), unsafe_allow_html=True)
init_db()   # Create tables if they don't exist

# ── Load exchange rates once ──────────────────────────────────
if "exchange_rates" not in st.session_state:
    result = get_exchange_rates("USD")
    st.session_state["exchange_rates"] = result["rates"] if result["success"] else None

# ── Auth session defaults ─────────────────────────────────────
if "logged_in"  not in st.session_state: st.session_state["logged_in"]  = False
if "user"       not in st.session_state: st.session_state["user"]       = None
if "auth_page"  not in st.session_state: st.session_state["auth_page"]  = "login"

# ── Helpers ───────────────────────────────────────────────────
def convert_from_usd(amount_usd, to_currency):
    rates = st.session_state.get("exchange_rates")
    if rates and to_currency != "USD":
        return convert_currency(amount_usd, "USD", to_currency, rates)
    return amount_usd

def disp_cur():
    return st.session_state.get("display_currency", "USD")

def disp(amount_usd):
    cur       = disp_cur()
    converted = convert_from_usd(amount_usd, cur)
    return format_currency(converted if converted is not None else amount_usd, cur)

def to_usd(amount, from_currency):
    rates = st.session_state.get("exchange_rates")
    if not rates or from_currency == "USD":
        return amount
    rate = rates.get(from_currency)
    if not rate or rate == 0:
        return amount
    return amount / rate

def logout():
    for key in ["logged_in","user","results","name","budget_usd","budget_input",
                "budget_currency","duration","num_people","interests",
                "chat_history","display_messages","quick_prompt"]:
        st.session_state.pop(key, None)
    st.session_state["logged_in"] = False
    st.session_state["user"]      = None
    st.rerun()


# ══════════════════════════════════════════════════════════════
# AUTH SCREENS  (shown when NOT logged in)
# ══════════════════════════════════════════════════════════════
def show_auth():
    st.markdown("""
    <div class="hero-banner">
        <h1 class="hero-title">🌍 AI Travel Assistant</h1>
        <p class="hero-subtitle">Plan your perfect trip anywhere in the world</p>
    </div>
    """, unsafe_allow_html=True)

    # Tab switcher buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔑 Login", use_container_width=True,
                     type="primary" if st.session_state["auth_page"] == "login" else "secondary"):
            st.session_state["auth_page"] = "login"
            st.rerun()
    with col2:
        if st.button("📝 Register", use_container_width=True,
                     type="primary" if st.session_state["auth_page"] == "register" else "secondary"):
            st.session_state["auth_page"] = "register"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── LOGIN ─────────────────────────────────────────────────
    if st.session_state["auth_page"] == "login":
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center;margin-bottom:20px;">
            <div style="font-size:2.5em;">🔑</div>
            <div style="font-size:1.2em;font-weight:600;color:#FFD700;">
                Welcome Back
            </div>
            <div style="font-size:0.85em;color:rgba(255,255,255,0.5);">
                Log in to access your travel plans
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            email    = st.text_input("📧 Email Address", placeholder="your@email.com")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("🔑 Log In", use_container_width=True)

        if submitted:
            success, result = login_user(email, password)
            if success:
                st.session_state["logged_in"] = True
                st.session_state["user"]      = result
                st.session_state["name"]      = result["name"]
                st.success(f"✅ Welcome back, {result['name']}!")
                st.rerun()
            else:
                st.error(f"❌ {result}")

        st.markdown("""
        <div style="text-align:center;margin-top:16px;color:rgba(255,255,255,0.5);font-size:0.85em;">
            Don't have an account?
            <span style="color:#FFA500;"> Click Register above</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── REGISTER ──────────────────────────────────────────────
    else:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center;margin-bottom:20px;">
            <div style="font-size:2.5em;">📝</div>
            <div style="font-size:1.2em;font-weight:600;color:#FFD700;">
                Create Your Account
            </div>
            <div style="font-size:0.85em;color:rgba(255,255,255,0.5);">
                Join thousands of smart travellers
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("register_form"):
            name      = st.text_input("👤 Full Name",      placeholder="e.g. Diana Kabura")
            email     = st.text_input("📧 Email Address",  placeholder="your@email.com")
            password  = st.text_input("🔒 Password",       type="password",
                                      placeholder="At least 6 characters")
            password2 = st.text_input("🔒 Confirm Password", type="password",
                                      placeholder="Repeat your password")
            submitted = st.form_submit_button("📝 Create Account", use_container_width=True)

        if submitted:
            if password != password2:
                st.error("❌ Passwords do not match.")
            else:
                success, result = register_user(name, email, password)
                if success:
                    st.success("✅ Account created! Please log in.")
                    st.session_state["auth_page"] = "login"
                    st.rerun()
                else:
                    st.error(f"❌ {result}")

        st.markdown("""
        <div style="text-align:center;margin-top:16px;color:rgba(255,255,255,0.5);font-size:0.85em;">
            Already have an account?
            <span style="color:#FFA500;"> Click Login above</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# MAIN APP  (shown when logged in)
# ══════════════════════════════════════════════════════════════
def show_main_app():
    user = st.session_state["user"]

    # ── Sidebar ───────────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-logo">
            <span class="logo-icon">✈️</span>
            <span class="logo-title">TravelBot AI</span>
            <span class="logo-sub">Your Global Travel Companion</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        page = st.radio(
            "Navigation",
            options=[
                "🏠 Home",
                "💱 Currency Converter",
                "🗺️ Map Explorer",
                "🌤️ Weather Checker",
                "🤖 Chat Assistant",
                "👤 My Profile",
            ],
            label_visibility="collapsed"
        )

        st.markdown("---")

        # Display currency selector
        st.markdown("""
        <p style="color:rgba(255,255,255,0.55);font-size:0.8em;margin-bottom:5px;">
            🌐 Display Currency
        </p>
        """, unsafe_allow_html=True)

        selected_currency = st.selectbox(
            "Display Currency",
            options=list(SUPPORTED_CURRENCIES.keys()),
            format_func=lambda x: f"{SUPPORTED_CURRENCIES[x]['symbol']}  {x} — {SUPPORTED_CURRENCIES[x]['name']}",
            index=0,
            label_visibility="collapsed",
            key="display_currency"
        )

        rates = st.session_state.get("exchange_rates")
        if rates:
            rate_val = rates.get(selected_currency, 1)
            rate_str = format_currency(rate_val, selected_currency)
            st.markdown(
                '<div style="background:rgba(255,165,0,0.1);border:1px solid rgba(255,165,0,0.28);'
                'border-radius:10px;padding:9px 12px;margin-top:6px;text-align:center;">'
                '<p style="margin:0;font-size:0.72em;color:rgba(255,255,255,0.45);">Live Rate</p>'
                '<p style="margin:3px 0 0;font-size:0.92em;font-weight:600;color:#FFD700;">'
                '$1 USD = ' + rate_str + '</p></div>',
                unsafe_allow_html=True
            )

        st.markdown("---")

        # Logged-in user info
        st.markdown(
            '<div style="background:rgba(255,165,0,0.08);border:1px solid rgba(255,165,0,0.25);'
            'border-radius:10px;padding:10px 14px;margin-bottom:8px;">'
            '<p style="margin:0;font-size:0.75em;color:rgba(255,255,255,0.45);">Logged in as</p>'
            '<p style="margin:3px 0 0;font-weight:600;color:#FFD700;">👤 ' + user["name"] + '</p>'
            '<p style="margin:2px 0 0;font-size:0.75em;color:rgba(255,255,255,0.4);">'
            + user["email"] + '</p></div>',
            unsafe_allow_html=True
        )

        if "budget_usd" in st.session_state:
            cur  = disp_cur()
            bval = convert_from_usd(st.session_state["budget_usd"], cur)
            st.markdown(
                '<div style="background:rgba(255,165,0,0.08);border:1px solid rgba(255,165,0,0.25);'
                'border-radius:10px;padding:10px 14px;margin-bottom:8px;">'
                '<p style="margin:0;font-size:0.75em;color:rgba(255,255,255,0.45);">Budget</p>'
                '<p style="margin:3px 0 0;font-weight:600;color:#FFD700;">💰 '
                + format_currency(bval, cur) + '</p></div>',
                unsafe_allow_html=True
            )

        if st.button("🚪 Logout", use_container_width=True):
            logout()

        st.markdown("""
        <div class="app-footer">© 2026 TravelBot AI</div>
        """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # PAGE 1 — HOME
    # ══════════════════════════════════════════════════════════
    if page == "🏠 Home":

        st.markdown(
            '<div class="hero-banner">'
            '<h1 class="hero-title">🌍 AI Travel Assistant</h1>'
            '<p class="hero-subtitle">Welcome back, ' + user["name"] + '! Plan your perfect trip.</p>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown("""
        <div class="step-header">
            <span class="step-badge">1</span>
            <span class="step-title">Tell Us About Your Trip</span>
        </div>
        """, unsafe_allow_html=True)

        with st.form("travel_form"):
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                duration = st.number_input("📅 Trip Duration (days)", min_value=1, max_value=30, value=7)
            with col2:
                num_people = st.number_input("👥 Number of Travellers", min_value=1, max_value=20, value=1)

            col1, col2 = st.columns(2)
            with col1:
                budget_currency = st.selectbox(
                    "💱 Enter budget in:",
                    options=list(SUPPORTED_CURRENCIES.keys()),
                    format_func=lambda x: f"{SUPPORTED_CURRENCIES[x]['symbol']} {x} — {SUPPORTED_CURRENCIES[x]['name']}",
                    index=0
                )
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)

            slider_max_map = {
                "USD":1000000,"EUR":900000,"GBP":800000,"JPY":100000000,
                "AUD":1500000,"CAD":1400000,"AED":4000000,"INR":80000000,
                "KES":130000000,"TZS":2500000000,"ZAR":18000000,"NGN":800000000,
                "IDR":15000000000,"THB":35000000,"MYR":5000000,"SGD":1400000,
                "CHF":900000,"TRY":30000000,"EGP":30000000,"MAD":10000000,
                "MXN":17000000,"BRL":5000000,"ARS":900000000,"CZK":23000000,
                "RWF":1000000000,"ETB":55000000,"GHS":120000,"UGX":3700000000,
                "CNY":7000000,
            }
            s_max     = slider_max_map.get(budget_currency, 1000000)
            s_default = int(s_max * 0.02)
            cur_sym   = SUPPORTED_CURRENCIES[budget_currency]["symbol"]

            budget_input = st.slider(
                f"💰 Your Budget ({cur_sym} {budget_currency})",
                min_value=0, max_value=s_max,
                value=s_default, step=max(1, s_max // 1000)
            )

            budget_usd = to_usd(budget_input, budget_currency)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(
                    '<div class="metric-card">'
                    '<div class="metric-value">' + format_currency(budget_input, budget_currency) + '</div>'
                    '<div class="metric-label">Your Budget (' + budget_currency + ')</div>'
                    '</div>', unsafe_allow_html=True)
            with col2:
                st.markdown(
                    '<div class="metric-card">'
                    '<div class="metric-value">$' + f"{budget_usd:,.0f}" + '</div>'
                    '<div class="metric-label">Equivalent USD</div>'
                    '</div>', unsafe_allow_html=True)
            with col3:
                st.markdown(
                    '<div class="metric-card">'
                    '<div class="metric-value">' + str(int(duration)) + ' days</div>'
                    '<div class="metric-label">Trip Duration</div>'
                    '</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            interests = st.multiselect(
                "🎯 What are you interested in?",
                options=["Safari","Wildlife","Beach","Swimming","Hiking","Culture",
                         "Photography","Adventure","Snorkeling","Climbing","Food",
                         "Shopping","History","Music","Diving","Cycling"],
                default=["Culture","Adventure"]
            )

            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("✈️ Find My Perfect Destinations", use_container_width=True)

        if submitted:
            if not interests:
                st.warning("⚠️ Please select at least one interest!")
            elif budget_usd < 10:
                st.warning("⚠️ Please set a higher budget!")
            else:
                st.session_state["budget_usd"]      = budget_usd
                st.session_state["budget_input"]    = budget_input
                st.session_state["budget_currency"] = budget_currency
                st.session_state["duration"]        = int(duration)
                st.session_state["num_people"]      = int(num_people)
                st.session_state["interests"]       = interests

                with st.spinner("🤖 AI is finding your perfect destinations..."):
                    df      = load_destinations()
                    results = recommend_destinations(interests, budget_usd, df)
                    st.session_state["results"] = results

                st.success(f"✅ Found top destinations for you, {user['name']}!")

        # ── Recommendations ───────────────────────────────────
        if "results" in st.session_state:
            results = st.session_state["results"]
            cur     = disp_cur()

            st.markdown("---")
            st.markdown("""
            <div class="step-header">
                <span class="step-badge">2</span>
                <span class="step-title">Your AI Recommended Destinations 🌟</span>
            </div>
            """, unsafe_allow_html=True)

            if results.empty:
                st.error("😔 No destinations found in your budget. Try increasing it!")
            else:
                for rank, (i, row) in enumerate(results.iterrows(), 1):
                    dest_cur_info  = get_destination_currency(row["destination"])
                    local_cur_code = dest_cur_info["code"]
                    cost_display   = disp(row["avg_cost_usd"])
                    cost_local     = convert_from_usd(row["avg_cost_usd"], local_cur_code)
                    cost_local_fmt = format_currency(cost_local, local_cur_code) if cost_local else ""

                    activities_html = "".join(
                        '<span class="dest-badge">' + a.strip() + '</span>'
                        for a in row["activities"]
                    )

                    local_tag = ""
                    if local_cur_code != cur and cost_local_fmt:
                        local_tag = (
                            '<div style="font-size:0.82em;color:rgba(255,255,255,0.45);margin-top:3px;">'
                            + "≈ " + cost_local_fmt + " locally</div>"
                        )

                    right_col = (
                        '<div style="font-size:1.35em;font-weight:700;color:#FFD700;">' + str(cost_display) + "</div>"
                        + local_tag
                        + '<div style="color:rgba(255,255,255,0.45);font-size:0.78em;">per person / day</div>'
                        + '<div style="margin-top:6px;font-size:1.05em;">⭐ ' + str(row["rating"]) + "</div>"
                    )

                    card_html = (
                        '<div class="dest-card">'
                        '<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;">'
                        '<div style="flex:1;">'
                        '<div class="dest-name">#' + str(rank) + " 📍 " + str(row["destination"]) + ", " + str(row["country"]) + "</div>"
                        '<div class="dest-detail">🏷️ ' + str(row["type"]) + "</div>"
                        '<div class="dest-detail">🗓️ Best Season: ' + str(row["best_season"]) + "</div>"
                        '<div style="margin-top:10px;">' + activities_html + "</div>"
                        "</div>"
                        '<div style="text-align:right;min-width:130px;">' + right_col + "</div>"
                        "</div></div>"
                    )
                    st.markdown(card_html, unsafe_allow_html=True)

                # ── Step 3 ────────────────────────────────────
                st.markdown("---")
                st.markdown("""
                <div class="step-header">
                    <span class="step-badge">3</span>
                    <span class="step-title">Generate Your Full Trip Plan</span>
                </div>
                """, unsafe_allow_html=True)

                chosen = st.selectbox("📍 Choose your destination:", options=results["destination"].tolist())

                if st.button("🗓️ Generate Itinerary & Budget Plan", use_container_width=True):
                    chosen_row    = results[results["destination"] == chosen].iloc[0]
                    activities    = chosen_row["activities"]
                    dest_cost_usd = chosen_row["avg_cost_usd"]
                    duration      = st.session_state["duration"]
                    num_people    = st.session_state["num_people"]
                    dest_cur_info = get_destination_currency(chosen)
                    dest_cur_code = dest_cur_info["code"]
                    cur           = disp_cur()

                    # Itinerary
                    st.markdown("---")
                    st.markdown(
                        '<div class="step-header">'
                        '<span class="step-badge">4</span>'
                        '<span class="step-title">Your ' + str(duration) + '-Day Itinerary in ' + chosen + '</span>'
                        '</div>', unsafe_allow_html=True)

                    itinerary = generate_itinerary(chosen, duration, activities)

                    for day, plan in itinerary.items():
                        day_html = (
                            '<div class="day-card">'
                            '<div class="day-title">📅 ' + day + " — " + plan["Main Activity"] + "</div>"
                            '<div class="time-block morning">'
                            '<div class="time-label">🌅 Morning</div>'
                            '<div class="time-content">' + plan["Morning"] + "</div></div>"
                            '<div class="time-block afternoon">'
                            '<div class="time-label">☀️ Afternoon</div>'
                            '<div class="time-content">' + plan["Afternoon"] + "</div></div>"
                            '<div class="time-block evening">'
                            '<div class="time-label">🌙 Evening</div>'
                            '<div class="time-content">' + plan["Evening"] + "</div></div>"
                            "</div>"
                        )
                        st.markdown(day_html, unsafe_allow_html=True)

                    # Budget
                    st.markdown("---")
                    st.markdown("""
                    <div class="step-header">
                        <span class="step-badge">5</span>
                        <span class="step-title">Your Budget Breakdown</span>
                    </div>
                    """, unsafe_allow_html=True)

                    breakdown, total_usd = calculate_budget(dest_cost_usd, duration, num_people)
                    remaining_usd     = st.session_state["budget_usd"] - total_usd
                    cost_in_display   = convert_from_usd(total_usd, cur)
                    cost_in_dest      = convert_from_usd(total_usd, dest_cur_code)
                    budget_display    = convert_from_usd(st.session_state["budget_usd"], cur)
                    remaining_display = convert_from_usd(abs(remaining_usd), cur)

                    summary_html = (
                        '<div class="glass-card" style="margin-bottom:18px;">'
                        '<div style="display:flex;justify-content:space-around;flex-wrap:wrap;gap:16px;text-align:center;">'
                        '<div>'
                        '<div style="font-size:0.78em;color:rgba(255,255,255,0.45);">Your Budget (' + cur + ')</div>'
                        '<div style="font-size:1.35em;font-weight:700;color:#FFD700;">' + format_currency(budget_display, cur) + '</div></div>'
                        '<div>'
                        '<div style="font-size:0.78em;color:rgba(255,255,255,0.45);">Estimated Cost (' + cur + ')</div>'
                        '<div style="font-size:1.35em;font-weight:700;color:#FFD700;">' + format_currency(cost_in_display, cur) + '</div></div>'
                        '<div>'
                        '<div style="font-size:0.78em;color:rgba(255,255,255,0.45);">Local Currency (' + dest_cur_code + ')</div>'
                        '<div style="font-size:1.35em;font-weight:700;color:#4FC3F7;">' + (format_currency(cost_in_dest, dest_cur_code) if cost_in_dest else "N/A") + '</div></div>'
                        '<div>'
                        '<div style="font-size:0.78em;color:rgba(255,255,255,0.45);">' + ("✅ Remaining" if remaining_usd >= 0 else "⚠️ Shortfall") + '</div>'
                        '<div style="font-size:1.35em;font-weight:700;color:' + ("#A5D6A7" if remaining_usd >= 0 else "#EF9A9A") + ';">' + format_currency(remaining_display, cur) + '</div></div>'
                        '</div></div>'
                    )
                    st.markdown(summary_html, unsafe_allow_html=True)

                    for item, cost_usd in breakdown.items():
                        cost_disp_val  = convert_from_usd(cost_usd, cur)
                        cost_local_val = convert_from_usd(cost_usd, dest_cur_code)
                        local_str      = format_currency(cost_local_val, dest_cur_code) if cost_local_val else ""
                        row_html = (
                            '<div class="budget-item">'
                            '<span class="budget-item-name">' + item + "</span>"
                            '<span style="display:flex;gap:14px;align-items:center;">'
                            '<span style="color:rgba(255,255,255,0.38);font-size:0.82em;">' + local_str + "</span>"
                            '<span class="budget-item-cost">' + format_currency(cost_disp_val, cur) + "</span>"
                            "</span></div>"
                        )
                        st.markdown(row_html, unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)
                    st.bar_chart(breakdown)

                    # Auto-save itinerary
                    save_itinerary(
                        user["user_id"], chosen, duration,
                        str({day: plan for day, plan in itinerary.items()})
                    )

                    st.markdown("---")
                    st.success("🎉 Your trip to **" + chosen + "** is fully planned and saved to your profile!")
                    st.info("💡 View saved itineraries in **👤 My Profile**")


    # ══════════════════════════════════════════════════════════
    # PAGE 2 — CURRENCY CONVERTER
    # ══════════════════════════════════════════════════════════
    elif page == "💱 Currency Converter":

        st.markdown("""
        <div class="hero-banner">
            <h1 class="hero-title">💱 Currency Converter</h1>
            <p class="hero-subtitle">Live exchange rates — convert any currency instantly</p>
        </div>
        """, unsafe_allow_html=True)

        rates = st.session_state.get("exchange_rates")

        if not rates:
            st.error("❌ Could not load exchange rates. Check your EXCHANGERATE_API_KEY in .env")
        else:
            st.markdown('<div class="section-header">🔄 Live Currency Converter</div>',
                        unsafe_allow_html=True)

            col1, col2, col3 = st.columns([2, 1, 2])
            with col1:
                amount   = st.number_input("Amount", min_value=0.01, value=100.0, step=10.0, key="conv_amount")
                from_cur = st.selectbox(
                    "From",
                    options=list(SUPPORTED_CURRENCIES.keys()),
                    format_func=lambda x: f"{SUPPORTED_CURRENCIES[x]['symbol']} {x} — {SUPPORTED_CURRENCIES[x]['name']}",
                    index=0, key="conv_from"
                )
            with col2:
                st.markdown("<br><br><br>", unsafe_allow_html=True)
                st.markdown('<div style="text-align:center;font-size:2.2em;color:#FFD700;">⇄</div>',
                            unsafe_allow_html=True)
            with col3:
                to_cur = st.selectbox(
                    "To",
                    options=list(SUPPORTED_CURRENCIES.keys()),
                    format_func=lambda x: f"{SUPPORTED_CURRENCIES[x]['symbol']} {x} — {SUPPORTED_CURRENCIES[x]['name']}",
                    index=1, key="conv_to"
                )

            live_rates = get_exchange_rates(from_cur)
            if live_rates["success"]:
                converted = convert_currency(amount, from_cur, to_cur, live_rates["rates"])
                if converted is not None:
                    rate_val = live_rates["rates"].get(to_cur, 1)
                    result_html = (
                        '<div class="converter-result">'
                        '<div style="font-size:0.85em;color:rgba(255,255,255,0.5);margin-bottom:10px;">'
                        "🔴 Live Result — updates automatically</div>"
                        '<div style="font-size:2.4em;font-weight:700;color:#FFD700;">'
                        + format_currency(amount, from_cur) + " = " + format_currency(converted, to_cur) +
                        "</div>"
                        '<div style="font-size:0.88em;color:rgba(255,255,255,0.45);margin-top:10px;">'
                        "1 " + from_cur + " = " + format_currency(rate_val, to_cur) + "</div>"
                        "</div>"
                    )
                    st.markdown(result_html, unsafe_allow_html=True)
            else:
                st.error("❌ Could not fetch live rates.")

            st.markdown("---")
            st.markdown('<div class="section-header">🌍 Live USD Exchange Rates</div>',
                        unsafe_allow_html=True)

            world_currencies = [
                ("🇺🇸 United States","USD","$"),("🇪🇺 Europe","EUR","€"),
                ("🇬🇧 United Kingdom","GBP","£"),("🇯🇵 Japan","JPY","¥"),
                ("🇦🇺 Australia","AUD","A$"),("🇨🇦 Canada","CAD","C$"),
                ("🇨🇭 Switzerland","CHF","Fr"),("🇦🇪 UAE","AED","د.إ"),
                ("🇸🇬 Singapore","SGD","S$"),("🇮🇳 India","INR","₹"),
                ("🇨🇳 China","CNY","¥"),("🇲🇾 Malaysia","MYR","RM"),
                ("🇹🇭 Thailand","THB","฿"),("🇮🇩 Indonesia","IDR","Rp"),
                ("🇹🇷 Turkey","TRY","₺"),("🇪🇬 Egypt","EGP","E£"),
                ("🇲🇦 Morocco","MAD","MAD"),("🇰🇪 Kenya","KES","KSh"),
                ("🇹🇿 Tanzania","TZS","TSh"),("🇿🇦 South Africa","ZAR","R"),
                ("🇳🇬 Nigeria","NGN","₦"),("🇬🇭 Ghana","GHS","GH₵"),
                ("🇷🇼 Rwanda","RWF","RF"),("🇲🇽 Mexico","MXN","MX$"),
                ("🇧🇷 Brazil","BRL","R$"),("🇨🇿 Czech Republic","CZK","Kč"),
            ]

            for country, code, symbol in world_currencies:
                if code in rates:
                    rv = rates[code]
                    st.markdown(
                        '<div class="rate-table-row">'
                        '<span style="color:rgba(255,255,255,0.82);">' + country + "</span>"
                        '<span style="display:flex;gap:18px;align-items:center;">'
                        '<span style="color:rgba(255,255,255,0.38);font-size:0.82em;">' + code + "</span>"
                        '<span style="color:#FFD700;font-weight:600;">$1 = ' + symbol + f"{rv:,.4f}" + "</span>"
                        "</span></div>", unsafe_allow_html=True
                    )

            if "budget_usd" in st.session_state:
                st.markdown("---")
                st.markdown('<div class="section-header">💰 Your Travel Budget in All Currencies</div>',
                            unsafe_allow_html=True)
                budget_usd = st.session_state["budget_usd"]
                for country, code, symbol in world_currencies:
                    if code in rates:
                        val = budget_usd * rates[code]
                        st.markdown(
                            '<div class="budget-item">'
                            '<span class="budget-item-name">' + country + "</span>"
                            '<span class="budget-item-cost">' + format_currency(val, code) + "</span>"
                            "</div>", unsafe_allow_html=True
                        )
            else:
                st.info("💡 Set a budget on the Home page to see it converted into all world currencies!")


    # ══════════════════════════════════════════════════════════
    # PAGE 3 — MAP EXPLORER
    # ══════════════════════════════════════════════════════════
    elif page == "🗺️ Map Explorer":

        st.markdown("""
        <div class="hero-banner">
            <h1 class="hero-title">🗺️ Map Explorer</h1>
            <p class="hero-subtitle">Explore any destination interactively</p>
        </div>
        """, unsafe_allow_html=True)

        if "results" in st.session_state and not st.session_state["results"].empty:
            st.markdown('<div class="section-header">⚡ Quick Pick From Recommendations</div>',
                        unsafe_allow_html=True)
            dest_names = st.session_state["results"]["destination"].tolist()
            quick_pick = st.selectbox("Pick a destination:", ["-- Search below --"] + dest_names)
            city_input = quick_pick if quick_pick != "-- Search below --" else ""
            st.markdown("---")
        else:
            city_input = ""

        city = st.text_input("Enter a city or place:", value=city_input,
                             placeholder="e.g. Tokyo, Paris, Nairobi, New York")

        if st.button("🗺️ Show on Map", use_container_width=True):
            if not city:
                st.warning("Please enter a city name!")
            else:
                with st.spinner(f"🔍 Locating {city}..."):
                    coords = get_coordinates(city)
                if not coords["success"]:
                    st.error("❌ " + coords["error"])
                else:
                    col1, col2, col3 = st.columns(3)
                    col1.metric("📍 City",      city)
                    col2.metric("🌐 Latitude",  round(coords["lat"], 4))
                    col3.metric("🌐 Longitude", round(coords["lng"], 4))
                    st.caption("📮 " + coords["address"])
                    components.html(create_single_map(city, coords["lat"], coords["lng"]), height=470)
                    st.markdown("---")
                    city_enc = city.replace(" ", "+")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.link_button("🗺️ OpenStreetMap",
                            "https://www.openstreetmap.org/search?query=" + city_enc,
                            use_container_width=True)
                    with col2:
                        st.link_button("✈️ Search Flights",
                            "https://www.google.com/travel/flights/search?q=flights+to+" + city_enc,
                            use_container_width=True)
                    with col3:
                        st.link_button("🏨 Search Hotels",
                            "https://www.booking.com/search.html?ss=" + city_enc,
                            use_container_width=True)

        if "results" in st.session_state and not st.session_state["results"].empty:
            st.markdown("---")
            st.markdown('<div class="section-header">🌍 All Recommended Destinations</div>',
                        unsafe_allow_html=True)
            if st.button("📍 Plot All Destinations on Map", use_container_width=True):
                results = st.session_state["results"]
                with st.spinner("🌍 Plotting..."):
                    all_coords = get_multiple_coordinates(results["destination"].tolist())
                    dest_data  = []
                    for coord in all_coords:
                        match = results[results["destination"] == coord["city"]]
                        if not match.empty:
                            row = match.iloc[0]
                            dest_data.append({
                                "city": coord["city"], "lat": coord["lat"],
                                "lng": coord["lng"], "cost": disp(row["avg_cost_usd"]),
                                "rating": row["rating"],
                            })
                if dest_data:
                    components.html(create_multi_map(dest_data), height=520)
                    st.caption(f"📍 {len(dest_data)} destinations plotted.")


    # ══════════════════════════════════════════════════════════
    # PAGE 4 — WEATHER CHECKER
    # ══════════════════════════════════════════════════════════
    elif page == "🌤️ Weather Checker":

        st.markdown("""
        <div class="hero-banner">
            <h1 class="hero-title">🌤️ Weather Checker</h1>
            <p class="hero-subtitle">Real-time weather for any destination worldwide</p>
        </div>
        """, unsafe_allow_html=True)

        if "results" in st.session_state and not st.session_state["results"].empty:
            st.markdown('<div class="section-header">⚡ Quick Pick</div>', unsafe_allow_html=True)
            dest_names = st.session_state["results"]["destination"].tolist()
            quick_pick = st.selectbox("Pick a destination:", ["-- Search below --"] + dest_names)
            city_input = quick_pick if quick_pick != "-- Search below --" else ""
            st.markdown("---")
        else:
            city_input = ""

        city = st.text_input("🔍 Enter a city name:", value=city_input,
                             placeholder="e.g. Tokyo, Paris, Nairobi")

        if st.button("🌍 Get Weather", use_container_width=True):
            if not city:
                st.warning("Please enter a city name!")
            else:
                with st.spinner(f"Fetching weather for {city}..."):
                    result = get_weather(city)
                if not result["success"]:
                    st.error("❌ " + result["error"])
                else:
                    data  = result["data"]
                    emoji = get_weather_emoji(data["description"])
                    st.markdown(
                        '<div class="weather-card">'
                        '<div class="weather-city">📍 ' + data["city"] + ", " + data["country"] + "</div>"
                        '<div style="font-size:4.5em;line-height:1;margin:8px 0;">' + emoji + "</div>"
                        '<div class="weather-temp">' + str(data["temperature"]) + "°C</div>"
                        '<div class="weather-desc">' + data["description"] + "</div>"
                        '<div style="margin-top:18px;line-height:2.2;">'
                        '<span class="weather-pill">💧 ' + str(data["humidity"]) + "% humidity</span>"
                        '<span class="weather-pill">💨 ' + str(data["wind_speed"]) + " km/h</span>"
                        '<span class="weather-pill">🌡️ Feels ' + str(data["feels_like"]) + "°C</span>"
                        '<span class="weather-pill">🔽 ' + str(data["min_temp"]) + "°C</span>"
                        '<span class="weather-pill">🔼 ' + str(data["max_temp"]) + "°C</span>"
                        "</div></div>",
                        unsafe_allow_html=True
                    )
                    temp = data["temperature"]
                    desc = data["description"].lower()
                    st.markdown("---")
                    st.markdown('<div class="section-header">🎒 Travel Advice</div>', unsafe_allow_html=True)
                    if temp >= 25:
                        st.markdown('<div class="advice-success">☀️ Warm and pleasant — pack light clothes and sunscreen.</div>', unsafe_allow_html=True)
                    elif temp >= 15:
                        st.markdown('<div class="advice-warning">🌤️ Mild — bring a light jacket for evenings.</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="advice-warning">🧥 Cool — pack warm layers.</div>', unsafe_allow_html=True)
                    if "rain" in desc or "drizzle" in desc:
                        st.markdown('<div class="advice-warning">🌧️ Rain expected — pack a raincoat.</div>', unsafe_allow_html=True)
                    if "thunder" in desc or "storm" in desc:
                        st.markdown('<div class="advice-danger">⛈️ Storm — postpone outdoor activities.</div>', unsafe_allow_html=True)
                    if "clear" in desc:
                        st.markdown('<div class="advice-success">☀️ Clear skies — perfect for outdoor activities!</div>', unsafe_allow_html=True)

                    st.markdown("---")
                    with st.spinner("Loading map..."):
                        coords = get_coordinates(city)
                    if coords["success"]:
                        components.html(create_single_map(city, coords["lat"], coords["lng"]), height=370)


    # ══════════════════════════════════════════════════════════
    # PAGE 5 — CHAT ASSISTANT
    # ══════════════════════════════════════════════════════════
    elif page == "🤖 Chat Assistant":

        st.markdown("""
        <div class="hero-banner">
            <h1 class="hero-title">🤖 TravelBot AI</h1>
            <p class="hero-subtitle">Ask me anything about travel — anywhere in the world!</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">💡 Quick Questions</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🎒 Packing tips",         use_container_width=True):
                st.session_state["quick_prompt"] = "What should I pack for a safari in East Africa?"
        with col2:
            if st.button("💰 Budget travel tips",   use_container_width=True):
                st.session_state["quick_prompt"] = "Give me budget travel tips for international travel"
        with col3:
            if st.button("🏖️ Best beach spots",     use_container_width=True):
                st.session_state["quick_prompt"] = "What are the best beach destinations in the world?"

        st.markdown("---")

        if "chat_history"     not in st.session_state: st.session_state["chat_history"]     = []
        if "display_messages" not in st.session_state: st.session_state["display_messages"] = []

        if not st.session_state["display_messages"]:
            with st.chat_message("assistant"):
                st.write("👋 Hello **" + user["name"] + "**! I'm TravelBot. Ask me anything about destinations, packing, costs, culture, or trip planning!")

        for msg in st.session_state["display_messages"]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        prompt_to_send = st.session_state.pop("quick_prompt", None)
        user_input     = st.chat_input("Ask a travel question...")
        final_input    = user_input or prompt_to_send

        if final_input:
            with st.chat_message("user"):
                st.write(final_input)
            with st.chat_message("assistant"):
                with st.spinner("TravelBot is thinking..."):
                    reply, st.session_state["chat_history"] = chat_with_assistant(
                        final_input, st.session_state["chat_history"]
                    )
                st.write(reply)
            st.session_state["display_messages"].append({"role": "user",      "content": final_input})
            st.session_state["display_messages"].append({"role": "assistant", "content": reply})
            st.rerun()

        if st.session_state["display_messages"]:
            st.markdown("---")
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state["chat_history"]     = []
                st.session_state["display_messages"] = []
                st.rerun()


    # ══════════════════════════════════════════════════════════
    # PAGE 6 — MY PROFILE
    # ══════════════════════════════════════════════════════════
    elif page == "👤 My Profile":

        st.markdown("""
        <div class="hero-banner">
            <h1 class="hero-title">👤 My Profile</h1>
            <p class="hero-subtitle">Manage your account and view saved itineraries</p>
        </div>
        """, unsafe_allow_html=True)

        profile = get_user_profile(user["user_id"])

        # Profile card
        if profile:
            st.markdown(
                '<div class="glass-card">'
                '<div style="display:flex;align-items:center;gap:20px;flex-wrap:wrap;">'
                '<div style="width:70px;height:70px;background:linear-gradient(135deg,#FF6B35,#FFD700);'
                'border-radius:50%;display:flex;align-items:center;justify-content:center;'
                'font-size:2em;flex-shrink:0;">👤</div>'
                '<div>'
                '<div style="font-size:1.4em;font-weight:700;color:#FFD700;">' + profile["name"] + "</div>"
                '<div style="color:rgba(255,255,255,0.6);font-size:0.9em;">📧 ' + profile["email"] + "</div>"
                '<div style="color:rgba(255,255,255,0.4);font-size:0.8em;margin-top:4px;">🗓️ Member since: ' + str(profile["joined"])[:10] + "</div>"
                "</div></div></div>",
                unsafe_allow_html=True
            )

        st.markdown("---")

        # Update name
        st.markdown('<div class="section-header">✏️ Update Profile</div>', unsafe_allow_html=True)
        with st.form("update_profile"):
            new_name = st.text_input("New Display Name", value=user["name"],
                                     placeholder="Enter new name")
            if st.form_submit_button("💾 Save Changes", use_container_width=True):
                if new_name.strip():
                    if update_user_name(user["user_id"], new_name.strip()):
                        st.session_state["user"]["name"] = new_name.strip()
                        st.session_state["name"]         = new_name.strip()
                        st.success("✅ Name updated successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Could not update name.")
                else:
                    st.warning("⚠️ Name cannot be empty.")

        st.markdown("---")

        # Saved itineraries
        st.markdown('<div class="section-header">🗓️ My Saved Itineraries</div>', unsafe_allow_html=True)

        saved = get_user_itineraries(user["user_id"])

        if not saved:
            st.markdown(
                '<div class="glass-card" style="text-align:center;padding:30px;">'
                '<div style="font-size:3em;">🗺️</div>'
                '<div style="color:rgba(255,255,255,0.5);margin-top:10px;">'
                "No saved itineraries yet. Go to Home to plan your first trip!</div>"
                "</div>",
                unsafe_allow_html=True
            )
        else:
            for trip in saved:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(
                        '<div class="dest-card" style="margin:6px 0;">'
                        '<div class="dest-name">📍 ' + trip["destination"] + "</div>"
                        '<div class="dest-detail">⏱️ Duration: ' + str(trip["duration"]) + "</div>"
                        '<div class="dest-detail">🗓️ Saved: ' + str(trip["created_at"])[:16] + "</div>"
                        "</div>",
                        unsafe_allow_html=True
                    )
                with col2:
                    st.markdown("<br><br>", unsafe_allow_html=True)
                    if st.button("🗑️ Delete", key=f"del_{trip['id']}", use_container_width=True):
                        delete_itinerary(trip["id"], user["user_id"])
                        st.success("Deleted!")
                        st.rerun()

        st.markdown("---")

        # Stats
        st.markdown('<div class="section-header">📊 Your Travel Stats</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("🗓️ Trips Planned", len(saved))
        unique_dest = len(set(t["destination"] for t in saved)) if saved else 0
        col2.metric("📍 Destinations Explored", unique_dest)
        col3.metric("🌍 Account Status", "Active ✅")


# ══════════════════════════════════════════════════════════════
# ENTRY POINT — Route to auth or main app
# ══════════════════════════════════════════════════════════════
if not st.session_state["logged_in"]:
    show_auth()
else:
    show_main_app()