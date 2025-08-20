import streamlit as st
import sys
import os
import json
import tempfile
from datetime import datetime

# Ajouter le chemin src pour importer nos modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import des modules (avec gestion d'erreurs pour Colab)
try:
    from plan_generator import PlanGenerator
    from model3d_generator import Model3DGenerator
    from structural_calculator import StructuralCalculator
except ImportError:
    st.error("Impossible d'importer les modules. Vérifiez la structure de votre projet.")

# Configuration de la page
st.set_page_config(
    page_title="Générateur de Dossiers de Génie Civil",
    page_icon="🏗️",
    layout="wide"
)

# Titre de l'application
st.title("🏗️ Générateur de Dossiers de Génie Civil")
st.markdown("""
Cette application permet de générer automatiquement des dossiers techniques de génie civil à partir d'une description textuelle.
""")

# Sidebar pour les paramètres
st.sidebar.header("Paramètres")

# Champ de description
description = st.text_area(
    "Description du projet",
    height=100,
    placeholder="Ex: Maison individuelle de 120m² avec 2 étages, murs en béton de 20cm, fondations semelles continues"
)

# Paramètres avancés
with st.sidebar.expander("Paramètres avancés"):
    resistance_beton = st.slider("Résistance du béton (MPa)", 20, 40, 25)
    resistance_acier = st.slider("Résistance de l'acier (MPa)", 400, 600, 500)
    portee_type = st.slider("Portée type (m)", 4, 10, 6)

# Bouton de génération
if st.button("Générer le dossier technique"):
    if description:
        with st.spinner("Extraction des paramètres..."):
            # Extraction des paramètres (version simplifiée pour l'interface)
            params = extract_params(description)
            params['resistance_beton'] = resistance_beton
            params['resistance_acier'] = resistance_acier
            params['portee_type'] = portee_type
            
        st.success("Paramètres extraits avec succès!")
        
        # Affichage des paramètres
        st.subheader("Paramètres extraits")
        st.json(params)
        
        # Génération du plan 2D
        with st.spinner("Génération du plan 2D..."):
            plan_generator = PlanGenerator()
            plan = plan_generator.generate_simple_rectangular_plan(
                params['longueur'], 
                params['largeur'], 
                params.get('epaisseur_mur', 0.2)
            )
            plan_generator.save_dxf("plan_2d.dxf")
        
        # Génération du modèle 3D
        with st.spinner("Génération du modèle 3D..."):
            model3d_generator = Model3DGenerator()
            model3d = model3d_generator.generate_simple_building(params)
            model3d_generator.save_dxf("modele_3d.dxf")
        
        # Calculs structurels
        with st.spinner("Calculs structurels..."):
            structural_calculator = StructuralCalculator()
            # Mise à jour des résistances des matériaux
            structural_calculator.concrete_strength = resistance_beton
            structural_calculator.steel_yield_strength = resistance_acier
            
            structural_report = structural_calculator.generate_structural_report(params)
        
        # Génération de la documentation
        with st.spinner("Génération de la documentation..."):
            generate_technical_documentation(description, params, structural_report)
        
        st.success("Dossier technique généré avec succès!")
        
        # Téléchargement des fichiers
        st.subheader("Téléchargement des fichiers")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            with open("plan_2d.dxf", "rb") as file:
                st.download_button(
                    label="Télécharger le plan 2D",
                    data=file,
                    file_name="plan_2d.dxf",
                    mime="application/dxf"
                )
        
        with col2:
            with open("modele_3d.dxf", "rb") as file:
                st.download_button(
                    label="Télécharger le modèle 3D",
                    data=file,
                    file_name="modele_3d.dxf",
                    mime="application/dxf"
                )
        
        with col3:
            with open("dossier_technique.json", "rb") as file:
                st.download_button(
                    label="Télécharger le rapport JSON",
                    data=file,
                    file_name="dossier_technique.json",
                    mime="application/json"
                )
        
        with col4:
            if os.path.exists("dossier_technique.pdf"):
                with open("dossier_technique.pdf", "rb") as file:
                    st.download_button(
                        label="Télécharger le rapport PDF",
                        data=file,
                        file_name="dossier_technique.pdf",
                        mime="application/pdf"
                    )
    else:
        st.error("Veuillez entrer une description.")

# Fonction d'extraction simplifiée pour l'interface
def extract_params(description):
    import re
    params = {
        'longueur': 10,
        'largeur': 8,
        'etages': 1,
        'epaisseur_mur': 0.2,
        'surface': 80
    }
    
    # Extraction de la surface
    surface_match = re.search(r'(\d+)\s*m²', description)
    if surface_match:
        surface = int(surface_match.group(1))
        params['surface'] = surface
        # Estimation des dimensions à partir de la surface
        params['longueur'] = round((surface * 1.2) ** 0.5, 1)
        params['largeur'] = round(surface / params['longueur'], 1)
    
    # Extraction du nombre d'étages
    etages_match = re.search(r'(\d+)\s*étages?', description)
    if etages_match:
        params['etages'] = int(etages_match.group(1))
    
    # Extraction de l'épaisseur des murs
    mur_match = re.search(r'(\d+)\s*cm', description)
    if mur_match:
        params['epaisseur_mur'] = int(mur_match.group(1)) / 100
    
    return params

# Fonction de génération de documentation
def generate_technical_documentation(description, params, structural_report):
    import json
    from fpdf import FPDF
    
    # Génération du JSON
    doc = {
        'projet': 'Dossier technique généré automatiquement',
        'date': datetime.now().isoformat(),
        'description_originale': description,
        'paramètres_extraits': params,
        'calculs_structurels': structural_report,
        'notes': 'Document généré automatiquement - Validation par un ingénieur recommandée'
    }
    
    with open('dossier_technique.json', 'w', encoding='utf-8') as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
    
    # Génération du PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Titre
    pdf.cell(200, 10, txt="DOSSIER TECHNIQUE", ln=True, align='C')
    pdf.ln(10)
    
    # Informations de base
    pdf.multi_cell(0, 10, f"Date: {doc['date']}")
    pdf.multi_cell(0, 10, f"Description: {doc['description_originale']}")
    pdf.ln(5)
    
    # Paramètres extraits
    pdf.multi_cell(0, 10, "Paramètres extraits:")
    for key, value in doc['paramètres_extraits'].items():
        pdf.multi_cell(0, 10, f"  {key}: {value}")
    
    pdf.ln(5)
    
    # Calculs structurels
    pdf.multi_cell(0, 10, "Calculs structurels:")
    for section, content in structural_report.items():
        if isinstance(content, dict):
            pdf.multi_cell(0, 10, f"{section}:")
            for key, value in content.items():
                pdf.multi_cell(0, 10, f"  {key}: {value}")
        else:
            pdf.multi_cell(0, 10, f"{section}: {content}")
        pdf.ln(2)
    
    pdf.output("dossier_technique.pdf")

if __name__ == "__main__":
    # Pour lancer l'application en local: streamlit run app.py
    pass
