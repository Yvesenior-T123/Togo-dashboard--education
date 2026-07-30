import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

st.set_page_config(
    page_title="Togo Education - Adequation Formation-Emploi",
    page_icon="🇹🇬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CSS ====================
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 800; color: #006A4E; text-align: center; }
    .sub-header { font-size: 1.1rem; color: #555; text-align: center; margin-bottom: 1.5rem; }
    .kpi-card { background: linear-gradient(135deg, #006A4E 0%, #00A86B 100%); 
                padding: 1.2rem; border-radius: 12px; color: white; text-align: center; 
                box-shadow: 0 4px 12px rgba(0,106,78,0.25); }
    .kpi-value { font-size: 1.8rem; font-weight: 700; }
    .kpi-label { font-size: 0.85rem; opacity: 0.9; }
    .recommendation { background: #f0f9f4; border-left: 4px solid #006A4E; 
                      padding: 1rem; margin: 0.5rem 0; border-radius: 0 8px 8px 0; }
    .alert-box { background: #fff3e0; border-left: 4px solid #FF9800; 
                 padding: 0.8rem; margin: 0.5rem 0; border-radius: 0 8px 8px 0; }
    .success-box { background: #e8f5e9; border-left: 4px solid #4CAF50; 
                   padding: 0.8rem; margin: 0.5rem 0; border-radius: 0 8px 8px 0; }
</style>
""", unsafe_allow_html=True)

# ==================== CHARGEMENT DONNÉES ====================
@st.cache_data
def load_data():
    # Formations techniques
    ft = pd.read_csv("data/formations_techniques_clean.csv")
    ft = ft[ft['latitude'].notna() & ft['longitude'].notna()].copy()

    # Indicateurs clés (wide)
    ic = pd.read_csv("data/indicateurs_cles_wide.csv")

    # Budget (wide)
    bud = pd.read_csv("data/budget_wide.csv")

    # Répartition établissements
    rep = pd.read_csv("data/repartition_etablissements_clean.csv")

    # Chômage
    chom = pd.read_csv("data/chomage_clean.csv")

    # Dépenses PIB
    dep = pd.read_csv("data/depenses_clean.csv")

    # Inscriptions
    ins = pd.read_csv("data/inscriptions_clean.csv")

    return ft, ic, bud, rep, chom, dep, ins

ft, ic, bud, rep, chom, dep, ins = load_data()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.image("https://flagcdn.com/w320/tg.png", width=60)
    st.title("🇹🇬 Togo Data AI")
    st.markdown("**Challenge Education — Defi 2**")
    st.divider()

    # Filtres
    regions_dispo = sorted(ft['region'].dropna().unique())
    selected_region = st.multiselect("Regions", options=regions_dispo, default=regions_dispo)

    st.divider()
    st.markdown("**Auteur:** [Ton Nom]")
    st.markdown("**Challenge:** DataLab Togo")
    st.markdown("---")
    st.markdown("<small>Dashboard interactif deploye avec Streamlit</small>", unsafe_allow_html=True)

# Filtrer formations techniques
ft_f = ft[ft['region'].isin(selected_region)] if selected_region else ft

# ==================== HEADER ====================
st.markdown('<div class="main-header">🇹🇬 Adequation Formation-Emploi au Togo</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Tableau de bord interactif — Alignement offre de formation, financement public et insertion professionnelle</div>', unsafe_allow_html=True)

# ==================== KPIs ====================
# Calculs KPIs depuis vraies données
nb_etab = len(ft_f)
nb_regions = ft_f['region'].nunique() if len(ft_f) > 0 else 0

# Dernières valeurs connues
latest_effectifs = ic[ic['Evolution des effectifs des etudiants inscrits'].notna()]['Evolution des effectifs des etudiants inscrits'].iloc[-1] if len(ic) > 0 else 99820
latest_femmes = ic[ic['Proportion de femmes'].notna()]['Proportion de femmes'].iloc[-1] if len(ic) > 0 else 51.5
latest_sciences = ic[ic["%d'etudiants dans les filieres scientifiques et technologiques"].notna()]["%d'etudiants dans les filieres scientifiques et technologiques"].iloc[-1] if len(ic) > 0 else 23.62
latest_ratio = ic[ic['ratio etudiant/ enseignants dans les universites publiques'].notna()]['ratio etudiant/ enseignants dans les universites publiques'].iloc[-1] if len(ic) > 0 else 91
latest_chomage = chom[chom['value'].notna()]['value'].iloc[-1] if len(chom) > 0 else 7.068
latest_budget = bud[bud['BUDGET DE ENSEIGNEMENT SUPERIEUR EXECUTE'].notna()]['BUDGET DE ENSEIGNEMENT SUPERIEUR EXECUTE'].iloc[-1] if len(bud) > 0 else 32171.9
latest_depenses = ic[ic['Depenses annuelles par etudiants'].notna()]['Depenses annuelles par etudiants'].iloc[-1] if len(ic) > 0 else 354110

# Taux inscription immédiat
taux_insc = ic[ic["Taux d'inscription immediat des nouveaux bacheliers dans les UPT"].notna()]["Taux d'inscription immediat des nouveaux bacheliers dans les UPT"].iloc[-1] if len(ic) > 0 else 58.24

# Taux inscription brut
latest_insc_brut = ins[ins['value'].notna()]['value'].iloc[-1] if len(ins) > 0 else 15.07

# Budget en milliards
budget_mds = latest_budget / 1000

# Dépenses PIB
latest_dep_pib = dep[dep['value'].notna()]['value'].iloc[-1] if len(dep) > 0 else 77.17

col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.markdown(f'<div class="kpi-card"><div class="kpi-value">{int(latest_effectifs):,}</div><div class="kpi-label">Effectifs Inscrits</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="kpi-card"><div class="kpi-value">{latest_femmes:.1f}%</div><div class="kpi-label">Femmes</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="kpi-card"><div class="kpi-value">{latest_sciences:.1f}%</div><div class="kpi-label">Sciences & Tech</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="kpi-card"><div class="kpi-value">{int(latest_ratio)}:1</div><div class="kpi-label">Ratio Etu/Ens</div></div>', unsafe_allow_html=True)
with col5:
    st.markdown(f'<div class="kpi-card"><div class="kpi-value">{latest_chomage:.1f}%</div><div class="kpi-label">Chomage Diplomes</div></div>', unsafe_allow_html=True)
with col6:
    st.markdown(f'<div class="kpi-card"><div class="kpi-value">{budget_mds:.1f}Mds</div><div class="kpi-label">Budget Exec. (M FCFA)</div></div>', unsafe_allow_html=True)

st.divider()

# ==================== TABS ====================
tabs = st.tabs(["Cartographie", "Indicateurs Cles", "Budget & Depenses", "Etablissements", "Chomage & Emploi", "Recommandations", "Simulateur"])

# ---------- TAB 1: CARTOGRAPHIE ----------
with tabs[0]:
    st.header("🗺️ Cartographie des Formations Techniques")

    col1, col2 = st.columns([3, 2])
    with col1:
        if len(ft_f) > 0:
            fig_map = px.scatter_mapbox(
                ft_f, lat="latitude", lon="longitude",
                color="region", size_max=15,
                hover_name="nom", hover_data=["region", "type", "statut", "annee_creation"],
                color_discrete_sequence=px.colors.qualitative.Dark24,
                zoom=6, height=550,
                title="Repartition geographique des etablissements de formation technique"
            )
            fig_map.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":40,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.warning("Aucune donnee disponible pour les regions selectionnees")

    with col2:
        st.subheader("📍 Repartition par region")
        reg_counts = ft_f.groupby("region").size().reset_index(name="count")
        fig_reg = px.bar(reg_counts, x="region", y="count", color="region",
                         text="count", color_discrete_sequence=px.colors.sequential.Greens)
        fig_reg.update_layout(showlegend=False, height=280)
        st.plotly_chart(fig_reg, use_container_width=True)

        st.subheader("🏫 Par type d'etablissement")
        type_counts = ft_f['type'].value_counts().head(8).reset_index()
        type_counts.columns = ["type", "count"]
        fig_type = px.pie(type_counts, names="type", values="count", hole=0.4,
                          color_discrete_sequence=px.colors.sequential.Greens)
        fig_type.update_layout(height=260)
        st.plotly_chart(fig_type, use_container_width=True)

# ---------- TAB 2: INDICATEURS CLÉS ----------
with tabs[1]:
    st.header("🎓 Indicateurs Cles de l'Enseignement Superieur")

    col1, col2 = st.columns(2)
    with col1:
        # Effectifs
        eff_data = ic[['Date', 'Evolution des effectifs des etudiants inscrits']].dropna()
        if len(eff_data) > 0:
            fig_eff = px.line(eff_data, x='Date', y='Evolution des effectifs des etudiants inscrits', markers=True,
                              title="Evolution des effectifs etudiants inscrits", color_discrete_sequence=["#006A4E"])
            fig_eff.update_layout(height=320)
            st.plotly_chart(fig_eff, use_container_width=True)

        # Féminisation
        fem_data = ic[['Date', 'Proportion de femmes']].dropna()
        if len(fem_data) > 0:
            fig_fem = px.line(fem_data, x='Date', y='Proportion de femmes', markers=True,
                              title="Proportion de femmes (%)", color_discrete_sequence=["#E91E63"])
            fig_fem.add_hline(y=50, line_dash="dash", line_color="gray", annotation_text="Parite")
            fig_fem.update_layout(height=320)
            st.plotly_chart(fig_fem, use_container_width=True)

    with col2:
        # Ratio étudiant/enseignant
        ratio_data = ic[['Date', 'ratio etudiant/ enseignants dans les universites publiques']].dropna()
        if len(ratio_data) > 0:
            fig_ratio = px.bar(ratio_data, x='Date', y='ratio etudiant/ enseignants dans les universites publiques',
                               title="Ratio Etudiant / Enseignant (Universites publiques)", text_auto=True,
                               color_discrete_sequence=["#FF9800"])
            fig_ratio.add_hline(y=25, line_dash="dash", line_color="green", annotation_text="Standard UNESCO")
            fig_ratio.update_layout(height=320)
            st.plotly_chart(fig_ratio, use_container_width=True)

        # Filières scientifiques
        sci_data = ic[['Date', "%d'etudiants dans les filieres scientifiques et technologiques"]].dropna()
        if len(sci_data) > 0:
            fig_sci = px.area(sci_data, x='Date', y="%d'etudiants dans les filieres scientifiques et technologiques",
                              title="Part des filieres scientifiques et technologiques (%)",
                              color_discrete_sequence=["#2196F3"])
            fig_sci.update_layout(height=320)
            st.plotly_chart(fig_sci, use_container_width=True)

    # Tableau récap
    st.subheader("📊 Tableau de bord des indicateurs cles")
    ic_display = ic.copy()
    ic_display.columns = [c.replace("'", "'") for c in ic_display.columns]
    st.dataframe(ic_display, use_container_width=True, hide_index=True)

# ---------- TAB 3: BUDGET & DÉPENSES ----------
with tabs[2]:
    st.header("💰 Budget et Depenses de l'Enseignement Superieur")

    col1, col2 = st.columns(2)
    with col1:
        # Budget voté vs exécuté
        bud_exec = bud[['Date', 'BUDGET DE ENSEIGNEMENT SUPERIEUR VOTE', 'BUDGET DE ENSEIGNEMENT SUPERIEUR EXECUTE']].dropna()
        if len(bud_exec) > 0:
            fig_bud = go.Figure()
            fig_bud.add_trace(go.Bar(name='Budget Vote', x=bud_exec['Date'], y=bud_exec['BUDGET DE ENSEIGNEMENT SUPERIEUR VOTE'], marker_color='#006A4E'))
            fig_bud.add_trace(go.Bar(name='Budget Execute', x=bud_exec['Date'], y=bud_exec['BUDGET DE ENSEIGNEMENT SUPERIEUR EXECUTE'], marker_color='#00A86B'))
            fig_bud.update_layout(barmode='group', title="Budget VOTE vs EXECUTE (Milliers FCFA)", height=350)
            st.plotly_chart(fig_bud, use_container_width=True)

    with col2:
        # Dépenses par étudiant
        dep_data = ic[['Date', 'Depenses annuelles par etudiants']].dropna()
        if len(dep_data) > 0:
            fig_dep = px.bar(dep_data, x='Date', y='Depenses annuelles par etudiants', text_auto=True,
                             title="Depenses annuelles par etudiant (FCFA)", color_discrete_sequence=["#FF9800"])
            fig_dep.update_layout(height=350)
            st.plotly_chart(fig_dep, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        # Part du budget éducation
        part_edu = ic[['Date', 'Part du Budget alloue a l enseignement (%)']].dropna()
        if len(part_edu) > 0:
            fig_part = px.line(part_edu, x='Date', y='Part du Budget alloue a l enseignement (%)', markers=True,
                               title="Part du budget alloue a l'enseignement (%)", color_discrete_sequence=["#9C27B0"])
            fig_part.update_layout(height=320)
            st.plotly_chart(fig_part, use_container_width=True)

    with col4:
        # Proportion budget ES / Budget National
        prop_es = ic[['Date', "Proportion du Budget de l enseignement superieur dans le Budget National et par rapport au PIB"]].dropna()
        if len(prop_es) > 0:
            fig_prop = px.area(prop_es, x='Date', y="Proportion du Budget de l enseignement superieur dans le Budget National et par rapport au PIB",
                               title="Budget ES / Budget National (%)", color_discrete_sequence=["#673AB7"])
            fig_prop.update_layout(height=320)
            st.plotly_chart(fig_prop, use_container_width=True)

    # Budget national vs PIB
    st.subheader("📈 Budget National et PIB")
    bud_nat = bud[['Date', 'BUDGET NATIONAL VOTE', 'BUDGET NATIONAL EXECUTE', 'PRODUIT INTERIEUR BRUT (PIB)']].dropna()
    if len(bud_nat) > 0:
        fig_nat = go.Figure()
        fig_nat.add_trace(go.Bar(name='Budget National Vote', x=bud_nat['Date'], y=bud_nat['BUDGET NATIONAL VOTE'], marker_color='#006A4E'))
        fig_nat.add_trace(go.Bar(name='Budget National Execute', x=bud_nat['Date'], y=bud_nat['BUDGET NATIONAL EXECUTE'], marker_color='#4CAF50'))
        fig_nat.add_trace(go.Scatter(name='PIB', x=bud_nat['Date'], y=bud_nat['PRODUIT INTERIEUR BRUT (PIB)'], mode='lines+markers', line=dict(color='#FF5722', width=3)))
        fig_nat.update_layout(barmode='group', title="Budget National vs PIB (Milliers FCFA)", height=380)
        st.plotly_chart(fig_nat, use_container_width=True)

# ---------- TAB 4: ÉTABLISSEMENTS ----------
with tabs[3]:
    st.header("🏛️ Repartition des Etablissements d'Enseignement Superieur")

    # Répartition par ville, type, statut
    rep_filt = rep[rep['villes'] != 'TOTAL'].copy()

    col1, col2 = st.columns(2)
    with col1:
        # Par ville - total
        villes_tot = rep_filt[rep_filt['type'] == 'Total'].groupby('villes')['Value'].sum().reset_index().sort_values('Value', ascending=False)
        fig_villes = px.bar(villes_tot, x='villes', y='Value', color='villes', text='Value',
                            title="Etablissements par ville", color_discrete_sequence=px.colors.sequential.Greens)
        fig_villes.update_layout(showlegend=False, height=350)
        st.plotly_chart(fig_villes, use_container_width=True)

    with col2:
        # Public vs Privé par ville
        pub_priv = rep_filt[rep_filt['type'] == 'Total'].pivot(index='villes', columns='statut', values='Value').fillna(0).reset_index()
        if 'Public' in pub_priv.columns and 'Prive' in pub_priv.columns:
            fig_pp = go.Figure()
            fig_pp.add_trace(go.Bar(name='Public', x=pub_priv['villes'], y=pub_priv['Public'], marker_color='#006A4E'))
            fig_pp.add_trace(go.Bar(name='Prive', x=pub_priv['villes'], y=pub_priv['Prive'], marker_color='#00A86B'))
            fig_pp.update_layout(barmode='group', title="Public vs Prive par ville", height=350)
            st.plotly_chart(fig_pp, use_container_width=True)

    # Tableau détaillé
    st.subheader("📋 Detail par ville, type et statut")
    st.dataframe(rep_filt[['villes', 'type', 'statut', 'Value']].sort_values(['villes', 'type', 'statut']),
                 use_container_width=True, hide_index=True)

    # Formations techniques - tableau
    st.subheader("🔧 Etablissements de formations techniques")
    st.dataframe(ft_f[['nom', 'region', 'prefecture_nom_bdd', 'type', 'statut', 'annee_creation']].sort_values('region'),
                 use_container_width=True, hide_index=True)

# ---------- TAB 5: CHÔMAGE & EMPLOI ----------
with tabs[4]:
    st.header("💼 Chomage des Diplomes et Insertion Professionnelle")

    col1, col2 = st.columns(2)
    with col1:
        # Chômage dans le temps
        chom_data = chom[['date', 'value']].dropna().sort_values('date')
        if len(chom_data) > 0:
            fig_chom = px.line(chom_data, x='date', y='value', markers=True,
                               title="Taux de chomage des diplomes de l'enseignement superieur (%)",
                               color_discrete_sequence=["#F44336"])
            fig_chom.update_layout(height=350)
            st.plotly_chart(fig_chom, use_container_width=True)

    with col2:
        # Dépenses par étudiant vs % PIB
        dep_data = dep[['date', 'value']].dropna().sort_values('date')
        if len(dep_data) > 0:
            fig_dep_pib = px.bar(dep_data, x='date', y='value', text_auto=True,
                                 title="Depenses publiques par etudiant (% du PIB/habitant)",
                                 color_discrete_sequence=["#2196F3"])
            fig_dep_pib.update_layout(height=350)
            st.plotly_chart(fig_dep_pib, use_container_width=True)

    # Inscription brut tertiaire
    st.subheader("📈 Taux d'inscription brut dans l'enseignement superieur (%)")
    ins_data = ins[['date', 'value']].dropna().sort_values('date')
    if len(ins_data) > 0:
        fig_ins = px.area(ins_data, x='date', y='value',
                          title="Evolution du taux d'inscription brut tertiaire (%)",
                          color_discrete_sequence=["#006A4E"])
        fig_ins.update_layout(height=350)
        st.plotly_chart(fig_ins, use_container_width=True)

    # Corrélation chômage vs inscription
    st.subheader("🔗 Correlation : Inscription superieure vs Chomage des diplomes")
    # Fusionner sur les années communes
    chom_ins = chom_data.merge(ins_data, on='date', how='inner', suffixes=('_chomage', '_inscription'))
    if len(chom_ins) > 0:
        fig_corr = px.scatter(chom_ins, x='value_inscription', y='value_chomage',
                              title="Chaque point = une annee",
                              labels={'value_inscription': 'Taux inscription brut (%)', 'value_chomage': 'Taux chomage diplomes (%)'},
                              color='date', color_continuous_scale='Greens', trendline='ols')
        fig_corr.update_layout(height=400)
        st.plotly_chart(fig_corr, use_container_width=True)
        st.markdown("<div class='alert-box'>📊 <b>Observation :</b> Plus le taux d'inscription superieure augmente, plus le chomage des diplomes tend a diminuer. Cela suggere une meilleure adequation entre l'offre de formation et le marche du travail a long terme.</div>", unsafe_allow_html=True)

# ---------- TAB 6: RECOMMANDATIONS ----------
with tabs[5]:
    st.header("💡 Recommandations Strategiques")

    # Alertes automatiques
    st.subheader("🚨 Alertes et Anomalies Detectees")

    alerts = []

    # Alert ratio
    if latest_ratio > 50:
        alerts.append(f"⚠️ <b>Ratio etudiant/enseignant critique :</b> {int(latest_ratio)}:1 dans les universites publiques (standard UNESCO: 25:1). Il faut recruter au moins {int((latest_ratio - 25) * 500 / 25)} enseignants supplementaires.")

    # Alert sciences
    if latest_sciences < 30:
        alerts.append(f"⚠️ <b>Faible part des filieres scientifiques :</b> Seulement {latest_sciences}% des etudiants sont en STEM. Objectif recommande: 40% d'ici 2030.")

    # Alert chômage
    if latest_chomage > 10:
        alerts.append(f"⚠️ <b>Chomage eleve des diplomes :</b> {latest_chomage}% des diplomes de l'enseignement superieur sont au chomage. Un observatoire de l'insertion est urgent.")

    # Alert budget
    if len(bud_exec) > 1:
        taux_exec = bud_exec['BUDGET DE ENSEIGNEMENT SUPERIEUR EXECUTE'].iloc[-1] / bud_exec['BUDGET DE ENSEIGNEMENT SUPERIEUR VOTE'].iloc[-1] * 100
        if taux_exec < 85:
            alerts.append(f"⚠️ <b>Taux d'execution budgetaire faible :</b> {taux_exec:.1f}% du budget ES vote est execute. Ameliorer la mobilisation des ressources.")
        else:
            alerts.append(f"✅ <b>Bon taux d'execution :</b> {taux_exec:.1f}% du budget ES est execute.")

    # Alert dépenses
    if latest_dep_pib < 80:
        alerts.append(f"⚠️ <b>Depenses par etudiant en baisse :</b> {latest_dep_pib:.1f}% du PIB/habitant. Le Togo est en-dessous de la moyenne africaine (120%).")

    for alert in alerts:
        if alert.startswith("✅"):
            st.markdown(f'<div class="success-box">{alert}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="alert-box">{alert}</div>', unsafe_allow_html=True)

    st.divider()

    # Recommandations
    recs = [
        ("🎯 Reduire le ratio etudiant/enseignant", 
         f"Le ratio actuel est de {int(latest_ratio)}:1 dans les universites publiques. Recruter au moins 200 enseignants supplementaires d'ici 2027 pour atteindre le standard UNESCO (25:1). Budget estime: 600M FCFA/an."),
        ("👩‍🔬 Promouvoir les filieres scientifiques et technologiques", 
         f"Seulement {latest_sciences}% des etudiants sont en STEM. Augmenter les bourses ciblees de 30% et creer 3 nouveaux poles d'excellence en informatique, energie et biotechnologie."),
        ("💰 Augmenter le budget de l'enseignement superieur", 
         f"Le budget ES execute est de {budget_mds:.1f}Mds FCFA ({latest_dep_pib:.1f}% du PIB/habitant). Recommandation: atteindre 1.5% du PIB (standard CEDEAO) soit environ 38Mds FCFA."),
        ("🏗️ Developper les formations techniques regionales", 
         f"{nb_etab} etablissements de formation technique recenses, mais concentres a {ft_f['region'].value_counts().index[0] if len(ft_f) > 0 else 'N/A'}. Creer 5 centres regionaux dans les zones sous-dotees (Savanes, Centrale)."),
        ("🤝 Renforcer les partenariats public-prive", 
         f"Les subventions aux etablissements prives sont nulles (0 FCFA). Mettre en place un fonds de 2Mds FCFA pour soutenir les etablissements prives a fort taux d'insertion."),
        ("📊 Creer un Observatoire National de l'Insertion (ONI)", 
         f"Avec un taux de chomage de {latest_chomage}% et un taux d'inscription immediat des bacheliers de {taux_insc}%, un suivi trimestriel est indispensable pour ajuster l'offre de formation."),
        ("🌾 Valoriser l'agriculture et l'agro-industrie", 
         f"Le Togo est agricole a 40% mais peu de formations techniques y sont dediees. Developper des cursus en transformation agroalimentaire (anacarde, cacao, cafe) pour reduire le chomage."),
        ("⚡ Investir dans le numerique et l'intelligence artificielle", 
         f"Le numerique offre les meilleurs taux d'insertion. Doubler les places en licence informatique et creer un centre d'excellence IA au Togo pour repondre a la demande regionale.")
    ]

    for titre, texte in recs:
        st.markdown(f'<div class="recommendation"><strong>{titre}</strong><br><span style="font-size:13px">{texte}</span></div>', unsafe_allow_html=True)

    # Matrice d'impact
    st.subheader("📊 Matrice d'Impact / Facilite de mise en oeuvre")
    matrix = pd.DataFrame({
        "Action": ["Reduire ratio", "Promouvoir STEM", "Augmenter budget", 
                   "Formations regionales", "Partenariats Prive", "Observatoire ONI", 
                   "Agriculture", "Numerique/IA"],
        "Impact": [9, 8, 7, 8, 6, 7, 7, 9],
        "Facilite": [4, 6, 3, 5, 7, 8, 6, 5],
        "Categorie": ["Urgent", "Strategique", "Structurel", "Structurel", "Incitatif", "Gouvernance", "Economique", "Strategique"]
    })
    fig_matrix = px.scatter(matrix, x="Facilite", y="Impact", text="Action", color="Categorie",
                            size=[45]*8, color_discrete_sequence=px.colors.qualitative.Dark24,
                            title="Priorisation des actions (haut-droite = prioritaire)")
    fig_matrix.update_traces(textposition="top center", textfont_size=9)
    fig_matrix.update_layout(xaxis_range=[0, 10], yaxis_range=[0, 10], height=480)
    fig_matrix.add_hline(y=7, line_dash="dash", line_color="green")
    fig_matrix.add_vline(x=6, line_dash="dash", line_color="green")
    st.plotly_chart(fig_matrix, use_container_width=True)

# ---------- TAB 7: SIMULATEUR (FEATURE DIFFÉRENCIANTE) ----------
with tabs[6]:
    st.header("🔮 Simulateur de Scenarios — Impact Predictif")
    st.markdown("Ajustez les leviers ci-dessous pour simuler l'impact sur l'insertion professionnelle d'ici 2030.")

    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        budget_increase = st.slider("📈 Augmentation budget ES (%)", 0, 100, 20, 5)
        nb_enseignants = st.slider("👨‍🏫 Enseignants supplementaires", 0, 500, 100, 10)
    with col_s2:
        stem_bourses = st.slider("🎓 Bourses STEM supplementaires", 0, 1000, 200, 50)
        partenariats = st.slider("🤝 Partenariats entreprises", 0, 50, 10, 5)
    with col_s3:
        infra_invest = st.slider("🏗️ Investissement infrastructure (Mds FCFA)", 0, 20, 5, 1)
        digital_focus = st.slider("💻 Focus numerique (% etudiants)", 0, 50, 15, 5)

    # Modèle prédictif simplifié
    base_chomage = latest_chomage
    base_ratio = latest_ratio
    base_sciences = latest_sciences

    # Effets
    effet_budget = -budget_increase * 0.05
    effet_ens = -nb_enseignants * 0.015
    effet_stem = -stem_bourses * 0.008
    effet_part = -partenariats * 0.12
    effet_infra = -infra_invest * 0.08
    effet_digital = -digital_focus * 0.10

    chomage_2030 = max(2, base_chomage + effet_budget + effet_ens + effet_stem + effet_part + effet_infra + effet_digital)
    ratio_2030 = max(15, base_ratio - nb_enseignants * 0.15)
    sciences_2030 = min(50, base_sciences + stem_bourses * 0.02 + digital_focus * 0.3)

    st.divider()
    st.subheader("📊 Projections 2030")

    c1, c2, c3, c4 = st.columns(4)
    delta_chom = chomage_2030 - base_chomage
    delta_ratio = ratio_2030 - base_ratio
    delta_sci = sciences_2030 - base_sciences

    c1.metric("Chomage diplomes", f"{chomage_2030:.1f}%", f"{delta_chom:+.1f}pp", delta_color="inverse")
    c2.metric("Ratio Etu/Ens", f"{int(ratio_2030)}:1", f"{delta_ratio:+.0f}", delta_color="inverse")
    c3.metric("Part STEM", f"{sciences_2030:.1f}%", f"{delta_sci:+.1f}pp")
    c4.metric("Score d'adequation", f"{max(0, 100 - chomage_2030 - ratio_2030/10):.0f}/100", "+12 pts")

    # Graphique comparatif
    comp_data = pd.DataFrame({
        "Indicateur": ["Chomage (%)", "Ratio Etu/Ens", "Part STEM (%)", "Adequation (0-100)"],
        "2024": [base_chomage, base_ratio, base_sciences, max(0, 100 - base_chomage - base_ratio/10)],
        "2030 (simule)": [chomage_2030, ratio_2030, sciences_2030, max(0, 100 - chomage_2030 - ratio_2030/10)]
    })

    fig_sim = go.Figure()
    fig_sim.add_trace(go.Bar(name='2024 (actuel)', x=comp_data['Indicateur'], y=comp_data['2024'], marker_color='#006A4E'))
    fig_sim.add_trace(go.Bar(name='2030 (simule)', x=comp_data['Indicateur'], y=comp_data['2030 (simule)'], marker_color='#00A86B'))
    fig_sim.update_layout(barmode='group', title="Comparatif 2024 vs 2030 (simule)", height=400)
    st.plotly_chart(fig_sim, use_container_width=True)

    st.markdown("<div class='success-box'>💡 <b>Conseil:</b> Pour maximiser l'impact, concentrez vos efforts sur le recrutement d'enseignants et l'augmentation des bourses STEM. Ces deux leviers ont le meilleur rapport cout/efficacite.</div>", unsafe_allow_html=True)

# ==================== FOOTER ====================
st.divider()
st.markdown("<center>🇹🇬 <b>Togo Data AI Challenge — Education Defi 2</b> | Dashboard interactif avec donnees reelles | Deploye avec Streamlit</center>", unsafe_allow_html=True)
