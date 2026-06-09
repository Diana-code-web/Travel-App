def load_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        min-height: 100vh;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.1) !important;
        min-width: 240px !important;
    }

    section[data-testid="stSidebar"] > div {
        background: transparent !important;
    }

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] .stRadio > div {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }

    section[data-testid="stSidebar"] .stRadio label {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
        padding: 10px 15px !important;
        margin: 2px 0 !important;
        display: block !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        color: white !important;
    }

    section[data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255,165,0,0.2) !important;
        border-color: #FFA500 !important;
    }

    section[data-testid="stSidebar"] .stSelectbox > div > div {
        background: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 10px !important;
        color: white !important;
    }

    .hero-banner {
        background: linear-gradient(135deg, #FF6B35, #F7931E, #FFD700);
        border-radius: 20px;
        padding: 40px 30px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(255,107,53,0.4);
        position: relative;
        overflow: hidden;
    }

    .hero-banner::before {
        content: '';
        position: absolute;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
        animation: shimmer 4s infinite linear;
    }

    @keyframes shimmer {
        0%   { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .hero-title {
        font-size: 2.5em; font-weight: 700; color: white;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.3);
        margin: 0; position: relative; z-index: 1;
    }

    .hero-subtitle {
        font-size: 1.05em; color: rgba(255,255,255,0.92);
        margin-top: 10px; position: relative; z-index: 1;
    }

    .glass-card {
        background: rgba(255,255,255,0.07);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.13);
        border-radius: 16px; padding: 25px; margin: 15px 0;
        transition: all 0.3s ease;
    }

    .glass-card:hover {
        background: rgba(255,255,255,0.10);
        border-color: rgba(255,165,0,0.4);
        box-shadow: 0 8px 28px rgba(0,0,0,0.25);
    }

    .section-header {
        background: linear-gradient(90deg, rgba(255,165,0,0.18), transparent);
        border-left: 4px solid #FFA500;
        border-radius: 0 10px 10px 0;
        padding: 11px 18px; margin: 20px 0 14px 0;
        color: #FFD700 !important; font-size: 1.1em; font-weight: 600;
    }

    .dest-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.09) 0%, rgba(255,255,255,0.04) 100%);
        border: 1px solid rgba(255,255,255,0.13);
        border-radius: 16px; padding: 20px; margin: 12px 0;
        transition: all 0.3s ease; position: relative; overflow: hidden;
    }

    .dest-card::after {
        content: ''; position: absolute; top: 0; left: 0;
        width: 4px; height: 100%;
        background: linear-gradient(180deg, #FF6B35, #FFD700);
        border-radius: 4px 0 0 4px;
    }

    .dest-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(0,0,0,0.28);
        border-color: rgba(255,165,0,0.45);
    }

    .dest-name   { font-size: 1.25em; font-weight: 700; color: #FFD700; margin-bottom: 8px; }
    .dest-detail { color: rgba(255,255,255,0.78); font-size: 0.88em; margin: 4px 0; }
    .dest-badge  {
        display: inline-block;
        background: linear-gradient(90deg, #FF6B35, #FFD700);
        color: white; font-size: 0.72em; font-weight: 600;
        padding: 3px 11px; border-radius: 20px; margin: 3px 2px;
    }

    .metric-card {
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.13);
        border-radius: 14px; padding: 16px; text-align: center; transition: all 0.3s ease;
    }

    .metric-card:hover { background: rgba(255,165,0,0.13); border-color: #FFA500; transform: translateY(-2px); }
    .metric-value { font-size: 1.6em; font-weight: 700; color: #FFD700; }
    .metric-label { font-size: 0.78em; color: rgba(255,255,255,0.55); margin-top: 4px; }

    .day-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 14px; padding: 20px; margin: 10px 0;
    }

    .day-title {
        font-size: 1.05em; font-weight: 600; color: #FFD700;
        margin-bottom: 14px; padding-bottom: 10px;
        border-bottom: 1px solid rgba(255,255,255,0.09);
    }

    .time-block {
        background: rgba(255,255,255,0.04);
        border-radius: 10px; padding: 12px; margin: 8px 0; border-left: 3px solid;
    }

    .time-block.morning   { border-left-color: #FF9800; }
    .time-block.afternoon { border-left-color: #2196F3; }
    .time-block.evening   { border-left-color: #9C27B0; }

    .time-label { font-size: 0.78em; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }
    .morning   .time-label { color: #FF9800; }
    .afternoon .time-label { color: #64B5F6; }
    .evening   .time-label { color: #CE93D8; }
    .time-content { color: rgba(255,255,255,0.82); font-size: 0.88em; }

    .weather-card {
        background: linear-gradient(135deg, rgba(33,150,243,0.18), rgba(0,188,212,0.13));
        border: 1px solid rgba(33,150,243,0.28);
        border-radius: 20px; padding: 30px; text-align: center; margin: 15px 0;
    }

    .weather-temp  { font-size: 3.8em; font-weight: 700; color: white; line-height: 1; }
    .weather-desc  { font-size: 1.15em; color: rgba(255,255,255,0.78); margin-top: 8px; text-transform: capitalize; }
    .weather-city  { font-size: 1.4em; font-weight: 600; color: #64B5F6; margin-bottom: 14px; }

    .weather-pill {
        display: inline-block;
        background: rgba(255,255,255,0.09); border: 1px solid rgba(255,255,255,0.18);
        border-radius: 20px; padding: 7px 16px; margin: 5px 3px;
        font-size: 0.88em; color: white;
    }

    .advice-success {
        background: linear-gradient(90deg, rgba(76,175,80,0.18), rgba(76,175,80,0.04));
        border: 1px solid rgba(76,175,80,0.38); border-radius: 12px;
        padding: 13px 17px; margin: 8px 0; color: #A5D6A7;
    }

    .advice-warning {
        background: linear-gradient(90deg, rgba(255,152,0,0.18), rgba(255,152,0,0.04));
        border: 1px solid rgba(255,152,0,0.38); border-radius: 12px;
        padding: 13px 17px; margin: 8px 0; color: #FFCC80;
    }

    .advice-danger {
        background: linear-gradient(90deg, rgba(244,67,54,0.18), rgba(244,67,54,0.04));
        border: 1px solid rgba(244,67,54,0.38); border-radius: 12px;
        padding: 13px 17px; margin: 8px 0; color: #EF9A9A;
    }

    .budget-item {
        background: rgba(255,255,255,0.04); border-radius: 10px;
        padding: 12px 16px; margin: 7px 0;
        display: flex; justify-content: space-between; align-items: center;
        border: 1px solid rgba(255,255,255,0.07); transition: all 0.3s ease;
    }

    .budget-item:hover { background: rgba(255,165,0,0.09); border-color: rgba(255,165,0,0.28); }
    .budget-item-name  { color: rgba(255,255,255,0.82); font-size: 0.93em; }
    .budget-item-cost  { color: #FFD700; font-weight: 600; font-size: 0.93em; }

    .rate-table-row {
        display: flex; justify-content: space-between; align-items: center;
        padding: 11px 16px; margin: 5px 0;
        background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.07);
        border-radius: 10px; transition: all 0.2s ease;
    }

    .rate-table-row:hover { background: rgba(255,165,0,0.09); border-color: rgba(255,165,0,0.28); }

    .converter-result {
        background: linear-gradient(135deg, rgba(255,107,53,0.15), rgba(255,215,0,0.1));
        border: 1px solid rgba(255,165,0,0.35);
        border-radius: 16px; padding: 28px; text-align: center; margin-top: 18px;
    }

    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.18) !important;
        border-radius: 10px !important; color: white !important; padding: 10px 14px !important;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #FFA500 !important; box-shadow: 0 0 0 2px rgba(255,165,0,0.18) !important;
    }

    .stSelectbox > div > div {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.18) !important;
        border-radius: 10px !important; color: white !important;
    }

    .stMultiSelect > div > div {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.18) !important; border-radius: 10px !important;
    }

    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #FF6B35, #FFD700) !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #FF6B35, #F7931E) !important;
        color: white !important; border: none !important; border-radius: 12px !important;
        padding: 12px 24px !important; font-weight: 600 !important;
        transition: all 0.3s ease !important; box-shadow: 0 4px 15px rgba(255,107,53,0.35) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255,107,53,0.55) !important;
        background: linear-gradient(135deg, #FF8C00, #FFD700) !important;
    }

    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stText { color: white !important; }
    hr { border-color: rgba(255,255,255,0.09) !important; margin: 18px 0 !important; }

    [data-testid="stChatMessage"] {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.09) !important;
        border-radius: 14px !important; margin: 8px 0 !important; padding: 12px !important;
    }

    [data-testid="stChatInput"] textarea {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.18) !important;
        border-radius: 12px !important; color: white !important;
    }

    .stSuccess { background: rgba(76,175,80,0.13)  !important; border: 1px solid rgba(76,175,80,0.38)  !important; border-radius: 12px !important; }
    .stInfo    { background: rgba(33,150,243,0.13) !important; border: 1px solid rgba(33,150,243,0.38) !important; border-radius: 12px !important; }
    .stWarning { background: rgba(255,152,0,0.13)  !important; border: 1px solid rgba(255,152,0,0.38)  !important; border-radius: 12px !important; }
    .stError   { background: rgba(244,67,54,0.13)  !important; border: 1px solid rgba(244,67,54,0.38)  !important; border-radius: 12px !important; }

    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.11) !important;
        border-radius: 14px !important; padding: 15px !important;
    }

    [data-testid="stMetricValue"] { color: #FFD700 !important; font-weight: 700 !important; }
    [data-testid="stMetricLabel"] { color: rgba(255,255,255,0.55) !important; }
    .stCaption { color: rgba(255,255,255,0.45) !important; font-size: 0.8em !important; }

    .stLinkButton > a {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.18) !important;
        border-radius: 10px !important; color: white !important; transition: all 0.3s ease !important;
    }

    .stLinkButton > a:hover { background: rgba(255,165,0,0.18) !important; border-color: #FFA500 !important; }

    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: rgba(255,255,255,0.04); }
    ::-webkit-scrollbar-thumb { background: linear-gradient(#FF6B35, #FFD700); border-radius: 3px; }

    .sidebar-logo { text-align: center; padding: 20px 10px 10px 10px; }
    .sidebar-logo .logo-icon  { font-size: 2.8em; display: block; margin-bottom: 7px; }
    .sidebar-logo .logo-title { font-size: 1.25em; font-weight: 700; color: #FFD700 !important; display: block; }
    .sidebar-logo .logo-sub   { font-size: 0.78em; color: rgba(255,255,255,0.45) !important; }

    .step-badge {
        display: inline-flex; align-items: center; justify-content: center;
        width: 30px; height: 30px;
        background: linear-gradient(135deg, #FF6B35, #FFD700);
        border-radius: 50%; font-weight: 700; font-size: 0.88em;
        color: white; margin-right: 10px; flex-shrink: 0;
    }

    .step-header { display: flex; align-items: center; margin: 20px 0 14px 0; }
    .step-title  { font-size: 1.15em; font-weight: 600; color: white; }

    .app-footer {
        text-align: center; padding: 18px;
        color: rgba(255,255,255,0.28) !important; font-size: 0.77em; margin-top: 30px;
    }
    </style>
    """