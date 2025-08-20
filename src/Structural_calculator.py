import math

class StructuralCalculator:
    def __init__(self):
        # Constantes matériaux (en MPa)
        self.concrete_strength = 25  # Résistance béton C25/30
        self.steel_yield_strength = 500  # Résistance acier HA500
        
        # Charges standards (en kN/m²)
        self.dead_load = 2.5  # Charge permanente
        self.live_load = 1.5  # Charge d'exploitation (résidentiel)
    
    def calculate_slab_thickness(self, span):
        """Calcule l'épaisseur minimale d'une dalle selon les règles BAEL"""
        # Formule simplifiée: épaisseur ≥ portée/30 pour dalle continue
        min_thickness = span / 30
        return max(0.12, min_thickness)  # Épaisseur minimale de 12cm
    
    def calculate_beam_dimensions(self, span, load):
        """Calcule les dimensions approximatives d'une poutre"""
        # Formule simplifiée: h ≈ portée/10 à portée/15
        height = span / 12
        width = height / 2
        
        return {
            'hauteur': round(height, 2),
            'largeur': round(width, 2),
            'portee': span
        }
    
    def calculate_foundation_size(self, total_load, soil_bearing_capacity=200):
        """Calcule la dimension des fondations superficielles"""
        # Surface nécessaire = charge totale / capacité portante du sol
        area = total_load / soil_bearing_capacity
        side = math.sqrt(area)
        
        return {
            'surface': round(area, 2),
            'cote': round(side, 2),
            'profondeur': round(0.5 + side/10, 2)  # Profondeur minimale
        }
    
    def calculate_total_load(self, surface, etages):
        """Calcule la charge totale sur les fondations"""
        load_per_floor = surface * (self.dead_load + self.live_load)
        return load_per_floor * etages
    
    def generate_structural_report(self, params):
        """Génère un rapport structurel complet"""
        surface = params.get('surface', 100)
        etages = params.get('etages', 1)
        portee_type = params.get('portee_type', 5)  # Portée typique en mètres
        
        # Calculs
        total_load = self.calculate_total_load(surface, etages)
        slab_thickness = self.calculate_slab_thickness(portee_type)
        beam_dims = self.calculate_beam_dimensions(portee_type, total_load)
        foundation_size = self.calculate_foundation_size(total_load)
        
        # Rapport
        report = {
            'charges': {
                'charge_permanente': self.dead_load,
                'charge_exploitation': self.live_load,
                'charge_totale_etage': surface * (self.dead_load + self.live_load),
                'charge_totale_batiment': total_load
            },
            'dalles': {
                'epaisseur_minimale': slab_thickness,
                'recommendation': f"Dalle de {slab_thickness*100:.0f}cm d'épaisseur minimum"
            },
            'poutres': beam_dims,
            'fondations': foundation_size,
            'conformite': {
                'eurocode': "Calculs simplifiés basés sur l'Eurocode",
                'bael': "Calculs simplifiés basés sur le BAEL",
                'notes': "Ces calculs sont indicatifs et doivent être validés par un ingénieur structure"
            }
        }
        
        return report

# Fonction de test
def test_structural_calculator():
    calculator = StructuralCalculator()
    params = {
        'surface': 120,
        'etages': 2,
        'portee_type': 6
    }
    report = calculator.generate_structural_report(params)
    
    print("Rapport de calculs structurels:")
    for section, content in report.items():
        print(f"\n{section.upper()}:")
        if isinstance(content, dict):
            for key, value in content.items():
                print(f"  {key}: {value}")
        else:
            print(f"  {content}")

if __name__ == "__main__":
    test_structural_calculator()
