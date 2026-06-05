import streamlit as st
import httpx
import os
import pandas as pd
import time

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_KEY = os.getenv("API_KEY", "")

st.set_page_config(page_title="DevOps Monitor", layout="wide", page_icon="🚀")

# Injection du CSS Custom pour un design Premium (Glassmorphism & Gradients)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.title-gradient {
    background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
    font-size: 3.5rem;
    margin-bottom: 0.2rem;
    letter-spacing: -1px;
}

.subtitle {
    color: #a0aec0;
    font-size: 1.2rem;
    margin-bottom: 2rem;
    font-weight: 400;
}

.metric-card {
    background: rgba(17, 25, 40, 0.75);
    backdrop-filter: blur(16px) saturate(180%);
    -webkit-backdrop-filter: blur(16px) saturate(180%);
    border: 1px solid rgba(255, 255, 255, 0.125);
    border-radius: 20px;
    padding: 30px 20px;
    text-align: center;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    margin-bottom: 20px;
}

.metric-card:hover {
    transform: translateY(-10px) scale(1.03);
    box-shadow: 0 20px 50px 0 rgba(0, 210, 255, 0.2);
    border: 1px solid rgba(0, 210, 255, 0.5);
}

.metric-icon {
    font-size: 2.5rem;
    margin-bottom: 15px;
}

.metric-value {
    font-size: 3.8rem;
    font-weight: 800;
    margin: 5px 0;
    color: #ffffff;
    text-shadow: 0 2px 15px rgba(255,255,255,0.2);
    line-height: 1;
}

.metric-label {
    font-size: 1.1rem;
    color: #cbd5e1;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: 600;
    margin-top: 10px;
}

.server-card {
    background: rgba(30, 41, 59, 0.7);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
    border-left: 5px solid #3b82f6;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.server-card:hover {
    transform: translateX(8px);
    background: rgba(30, 41, 59, 0.9);
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.server-name {
    font-size: 1.3rem;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 5px;
}

.server-host {
    color: #94a3b8;
    font-size: 0.95rem;
    font-weight: 500;
}

.status-badge {
    padding: 8px 16px;
    border-radius: 30px;
    font-size: 0.85rem;
    font-weight: 800;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.status-up { background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.4); }
.status-down { background: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.4); }
.status-degraded { background: rgba(245, 158, 11, 0.15); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.4); }

.stButton>button {
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title-gradient">DevOps Monitor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Real-time infrastructure intelligence by <b>Darkbd11</b></div>', unsafe_allow_html=True)

st.markdown("---")

tab1, tab2 = st.tabs(["🚀 MÉTRIQUES SYSTÈME", "🖥️ PARC SERVEURS"])

if 'metrics_history' not in st.session_state:
    st.session_state['metrics_history'] = pd.DataFrame(columns=['cpu_percent', 'memory_percent', 'disk_percent'])

with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    metric_placeholder = st.empty()
    st.markdown("<br>", unsafe_allow_html=True)
    chart_placeholder = st.empty()
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Bouton d'activation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        start_monitor = st.button("🔴 ACTIVER LE FLUX EN TEMPS RÉEL", use_container_width=True)

    if start_monitor:
        while True:
            try:
                response = httpx.get(f"{API_BASE_URL}/metrics", timeout=2.0)
                if response.status_code == 200:
                    data = response.json()
                    
                    with metric_placeholder.container():
                        c1, c2, c3 = st.columns(3)
                        c1.markdown(f'''
                            <div class="metric-card">
                                <div class="metric-icon">⚡</div>
                                <div class="metric-value">{data["cpu_percent"]}%</div>
                                <div class="metric-label">Processeur (CPU)</div>
                            </div>
                        ''', unsafe_allow_html=True)
                        
                        c2.markdown(f'''
                            <div class="metric-card">
                                <div class="metric-icon">🧠</div>
                                <div class="metric-value">{data["memory_percent"]}%</div>
                                <div class="metric-label">Mémoire (RAM)</div>
                            </div>
                        ''', unsafe_allow_html=True)
                        
                        c3.markdown(f'''
                            <div class="metric-card">
                                <div class="metric-icon">💾</div>
                                <div class="metric-value">{data["disk_percent"]}%</div>
                                <div class="metric-label">Stockage (Disque)</div>
                            </div>
                        ''', unsafe_allow_html=True)
                    
                    new_row = pd.DataFrame([data])
                    st.session_state['metrics_history'] = pd.concat([st.session_state['metrics_history'], new_row], ignore_index=True).tail(60)
                    
                    # Graphique stylisé
                    chart_placeholder.line_chart(
                        st.session_state['metrics_history'], 
                        color=["#00d2ff", "#3a7bd5", "#10b981"],
                        height=400
                    )
                    
            except httpx.RequestError:
                st.error("🔌 Connexion à l'API perdue. L'API est-elle lancée ?")
                break
                
            time.sleep(1)

with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    col_list, col_gap, col_form = st.columns([5, 1, 4])
    
    with col_list:
        st.markdown("### 📡 Serveurs Connectés")
        def fetch_servers():
            try:
                r = httpx.get(f"{API_BASE_URL}/servers")
                return r.json() if r.status_code == 200 else []
            except:
                return []

        servers = fetch_servers()
        
        if servers:
            for s in servers:
                status_class = "status-up" if s["status"] == "UP" else "status-degraded" if s["status"] == "DEGRADED" else "status-down"
                st.markdown(f'''
                    <div class="server-card">
                        <div>
                            <div class="server-name">{s["name"]}</div>
                            <div class="server-host">🌐 {s["host"]}:{s["port"]}</div>
                        </div>
                        <div class="status-badge {status_class}">{s["status"]}</div>
                    </div>
                ''', unsafe_allow_html=True)
        else:
            st.info("🕸️ Aucun serveur n'est actuellement surveillé.")

    with col_form:
        st.markdown("### ➕ Déployer un Nœud")
        with st.form("add_server_form", clear_on_submit=True):
            name = st.text_input("Identifiant du Serveur", placeholder="ex: Prod-DB-01")
            host = st.text_input("Adresse / IP", placeholder="ex: 192.168.1.50")
            port = st.number_input("Port cible", min_value=1, max_value=65535, value=8000)
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("🚀 INITIALISER LE TRACKING", use_container_width=True)
            
            if submitted:
                payload = {"name": name, "host": host, "port": port}
                headers = {"X-API-Key": API_KEY}
                try:
                    res = httpx.post(f"{API_BASE_URL}/servers", json=payload, headers=headers)
                    if res.status_code == 201:
                        st.success("✅ Serveur synchronisé avec succès !")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"❌ Rejet de l'API : {res.status_code}")
                except Exception as e:
                    st.error(f"⚠️ Échec réseau : {e}")
