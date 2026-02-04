import json
import os
from datetime import datetime
import streamlit as st

PARTIES = [
    "SPD",
    "CDU",
    "GRUENE",
    "FDP",
    "AfD",
    "FREIE_WAEHLER",
    "LINKE",
]

TIPPS_FILE = "tipps.json"

# ⬇️ Abgabeschluss hier anpassen!
DEADLINE = datetime(2026, 3, 12, 18, 0)


def load_tips():
    if os.path.exists(TIPPS_FILE):
        with open(TIPPS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_tips(tips):
    with open(TIPPS_FILE, "w", encoding="utf-8") as f:
        json.dump(tips, f, indent=2, ensure_ascii=False)


def calculate_score(tips, results):
    score = 0
    for party in PARTIES:
        diff = abs(tips[party] - results[party])
        if diff == 0:
            score += 3
        elif diff <= 1.0:
            score += 1
    return score


st.title("🎯 Tippspiel – Landtagswahl Rheinland-Pfalz")

now = datetime.now()
locked = now >= DEADLINE

st.markdown(
    f"**Abgabeschluss:** {DEADLINE.strftime('%d.%m.%Y %H:%M')} Uhr  \n"
    f"**Status:** {'🔒 geschlossen' if locked else '🟢 offen'}"
)

st.divider()

st.header("📝 Tipp abgeben")

if locked:
    st.warning("Die Tippabgabe ist geschlossen.")
else:
    name = st.text_input("Dein Name")

    tips = {}
    for party in PARTIES:
        tips[party] = st.number_input(
            party,
            min_value=0.0,
            max_value=100.0,
            step=0.1,
            format="%.1f",
        )

    if st.button("Tipp speichern"):
        if not name.strip():
            st.error("Bitte einen Namen eingeben.")
        else:
            all_tips = load_tips()
            if name in all_tips:
                st.error("Dieser Name existiert bereits.")
            else:
                all_tips[name] = tips
                save_tips(all_tips)
                st.success("Tipp gespeichert ✅")

st.divider()
st.header("📊 Auswertung")

with st.expander("Endergebnisse eingeben"):
    results = {}
    for party in PARTIES:
        results[party] = st.number_input(
            f"{party} Ergebnis",
            min_value=0.0,
            max_value=100.0,
            step=0.1,
            format="%.1f",
            key=f"res_{party}",
        )

    if st.button("Auswertung berechnen"):
        all_tips = load_tips()

        if not all_tips:
            st.warning("Noch keine Tipps vorhanden.")
        else:
            scores = []
            for name, tips in all_tips.items():
                scores.append((name, calculate_score(tips, results)))

            scores.sort(key=lambda x: x[1], reverse=True)

            st.subheader("🏆 Rangliste")
            for i, (name, score) in enumerate(scores, start=1):
                st.write(f"**{i}. {name}** – {score} Punkte")
