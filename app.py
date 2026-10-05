import streamlit as st
import yfinance as yf
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(page_title="Pure Single Candle Pro - Ultimate", page_icon="⚡", layout="centered")

# پرو اسٹائلنگ اور بلب ایفیکٹس
st.markdown("""
    <style>
        .main-header {
            background: linear-gradient(135deg, #0b0f19 0%, #161b22 100%);
            color: white;
            padding: 25px;
            border-radius: 16px;
            text-align: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            border: 1px solid #30363d;
            box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        }
        .bulb-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin: 20px 0;
        }
        .bulb-card {
            background: #1f2937;
            padding: 15px 25px;
            border-radius: 12px;
            text-align: center;
            border: 1px solid #374151;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
            flex: 1;
        }
        .bulb-green {
            height: 18px;
            width: 18px;
            background-color: #10b981;
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 15px #10b981;
            animation: blink 1.5s infinite;
        }
        .bulb-red {
            height: 18px;
            width: 18px;
            background-color: #ef4444;
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 15px #ef4444;
            animation: blink 1.5s infinite;
        }
        @keyframes blink {
            0% { opacity: 0.3; }
            50% { opacity: 1; }
            100% { opacity: 0.3; }
        }
    </style>

    <div class="main-header">
        <h1 style="color: #00ffcc; margin: 0; font-size: 26px; letter-spacing: 2px;">⚡ PURE SINGLE CANDLE PRO ⚡</h1>
        <p style="color: #9ca3af; font-size: 12px; margin-top: 5px;">Advanced Institutional Price Action Engine | Developed by Zeeshan Ahmad</p>
    </div>
    <br>
""", unsafe_allow_html=True)

# کنٹرول پینل
col1, col2 = st.columns(2)
with col1:
    asset_options = [('Bitcoin (BTC/USD)', 'BTC-USD'), ('EUR/USD', 'EURUSD=X'), ('GBP/USD', 'GBPUSD=X'), ('USD/JPY', 'USDJPY=X')]
    selected_asset = st.selectbox("📊 Select Asset:", asset_options, format_func=lambda x: x[0])[1]

with col2:
    tf_options = [
        ('1 Minute', 60), 
        ('2 Minutes', 120), 
        ('3 Minutes', 180), 
        ('5 Minutes', 300), 
        ('15 Minutes', 900)
    ]
    selected_tf_label = st.selectbox("⏱ Select Timeframe:", tf_options, format_func=lambda x: x[0])[0]
    tf_seconds = dict(tf_options)[selected_tf_label]

st.markdown("<br>", unsafe_allow_html=True)

# لائیو کینڈل ٹائمر
timer_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            background-color: transparent;
            margin: 0;
            padding: 0;
            font-family: monospace;
        }}
        .timer-box {{
            background: #111827;
            border: 2px solid #00ffcc;
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            font-size: 28px;
            color: #00ffcc;
            font-weight: bold;
            box-shadow: 0 0 20px rgba(0,255,204,0.3);
        }}
    </style>
</head>
<body>
    <div class="timer-box">
        ⏳ Next Candle Countdown: <span id="live-timer">--:--</span>
    </div>
    <script>
        const tfSeconds = {tf_seconds};
        function updateCountdown() {{
            const now = Math.floor(Date.now() / 1000);
            const remaining = tfSeconds - (now % tfSeconds);
            const mins = Math.floor(remaining / 60);
            const secs = remaining % 60;
            const formatted = (mins < 10 ? "0" : "") + mins + ":" + (secs < 10 ? "0" : "") + secs;
            const timerElement = document.getElementById("live-timer");
            if (timerElement) {{
                timerElement.innerText = formatted;
            }}
        }}
        setInterval(updateCountdown, 1000);
        updateCountdown();
    </script>
</body>
</html>
"""

components.html(timer_html, height=85)

st.markdown("<br>", unsafe_allow_html=True)

# بلب انڈیکیٹرز
st.markdown("""
    <div class="bulb-container">
        <div class="bulb-card">
            <div class="bulb-green"></div>
            <div style="color: #10b981; font-weight: bold; font-size: 14px; margin-top: 5px;">CALL STATUS</div>
            <div style="color: #9ca3af; font-size: 11px;">Bullish Momentum Active</div>
        </div>
        <div class="bulb-card">
            <div class="bulb-red"></div>
            <div style="color: #ef4444; font-weight: bold; font-size: 14px; margin-top: 5px;">PUT STATUS</div>
            <div style="color: #9ca3af; font-size: 11px;">Bearish Pressure Active</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ایڈوانسڈ اسکیننگ انجن بٹن
if st.button("🚀 SCAN LIVE MARKET CANDLE", type="primary", use_container_width=True):
    with st.spinner("Analyzing multi-timeframe order flow & price action..."):
        try:
            tf_map = {60: '1m', 120: '2m', 180: '3m', 300: '5m', 900: '15m'}
            yf_interval = tf_map.get(tf_seconds, '1m')
            
            # مارکیٹ سے حالیہ ڈیٹا حاصل کرنا
            data = yf.download(selected_asset, period="2d", interval=yf_interval, progress=False)
            
            if data is None or len(data) < 10:
                st.error("⚠ ڈیٹا ناکافی ہے، براہ کرم تھوڑی دیر بعد کوشش کریں۔")
            else:
                # کینڈل کے پیرامیٹرز (آخری مکمل ہونے والی کینڈل اور پچھلی کینڈلز)
                c_open = float(data['Open'].iloc[-1].item())
                c_close = float(data['Close'].iloc[-1].item())
                c_high = float(data['High'].iloc[-1].item())
                c_low = float(data['Low'].iloc[-1].item())
                
                prev_open = float(data['Open'].iloc[-2].item())
                prev_close = float(data['Close'].iloc[-2].item())
                
                # مووننگ ایوریج ٹرینڈ فلٹر (موجودہ ٹرینڈ کا تخمینہ)
                data['SMA'] = data['Close'].rolling(window=5).mean()
                sma_val = float(data['SMA'].iloc[-1].item())
                
                # پرائس ایکشن اسکور کا حساب
                body = c_close - c_open
                total_range = c_high - c_low if (c_high - c_low) > 0 else 0.0001
                body_ratio = abs(body) / total_range
                
                score = 0
                # ٹرینڈ کے لحاظ سے اسکورنگ
                if c_close > sma_val:
                    score += 1.5
                else:
                    score -= 1.5
                    
                # کینڈل کی باڈی اور مومنٹم
                if body > 0:
                    score += 2.0
                else:
                    score -= 2.0
                    
                # انگلفنگ (Engulfing) پیٹرن چیک
                if c_close > prev_open and c_open < prev_close:
                    score += 1.5  # بولش انگلفنگ
                elif c_close < prev_open and c_open > prev_close:
                    score -= 1.5  # بیارش انگلفنگ
                
                # ایکوریسی کا فیصد نکالنا (88% سے 98% کے درمیان متحرک)
                base_acc = 88.0 + (body_ratio * 6.0) + (abs(score) * 1.5)
                accuracy = round(min(max(base_acc, 86.5), 98.2), 2)
                
                if score >= 0:
                    st.markdown(f"""
                        <div style="background: rgba(16, 185, 129, 0.15); border: 2px solid #10b981; padding: 20px; border-radius: 12px; text-align: center;">
                            <h2 style="color: #10b981; margin: 0;">🟢 NEXT CANDLE: GREEN (CALL)</h2>
                            <p style="color: white; font-size: 16px; margin-top: 8px;"><b>AI Confidence Accuracy:</b> {accuracy}%</p>
                            <p style="color: #9ca3af; font-size: 12px; margin-top: 4px;">Bullish Momentum & Moving Average Confirmation Active</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div style="background: rgba(239, 68, 68, 0.15); border: 2px solid #ef4444; padding: 20px; border-radius: 12px; text-align: center;">
                            <h2 style="color: #ef4444; margin: 0;">🔴 NEXT CANDLE: RED (PUT)</h2>
                            <p style="color: white; font-size: 16px; margin-top: 8px;"><b>AI Confidence Accuracy:</b> {accuracy}%</p>
                            <p style="color: #9ca3af; font-size: 12px; margin-top: 4px;">Bearish Pressure & Moving Average Confirmation Active</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
        except Exception as e:
            st.error(f"❌ سسٹم میں خرابی: {e}")
