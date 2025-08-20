import ezdxf
from ezdxf import units
import numpy as np
from .plan_generator import PlanGenerator

class Model3DGenerator(PlanGenerator):
    def __init__(self):
        super().__init__()
        self.height = 3.0  # Hauteur par défaut d'un étage en mètres
    
    def set_floor_height(self, height):
        """Définit la hauteur d'un étage"""
        self.height = height
    
    def generate_3d_walls(self, length, width, floors=1, wall_thickness=0.2):
        """Génère un modèle 3D des murs"""
        self.create_new_document()
        
        # Hauteur totale du bâtiment
        total_height = floors * self.height
        
        # Points de base pour les murs extérieurs
        outer_points = [
            (0, 0, 0),
            (length, 0, 0),
            (length, width, 0),
            (0, width, 0),
            (0, 0, 0)
        ]
        
        # Points pour les murs intérieurs (simplifiés)
        inner_points = [
            (wall_thickness, wall_thickness, 0),
            (length - wall_thickness, wall_thickness, 0),
            (length - wall_thickness, width - wall_thickness, 0),
            (wall_thickness, width - wall_thickness, 0),
            (wall_thickness, wall_thickness, 0)
        ]
        
        # Création des murs extérieurs
        for i in range(4):
            start = outer_points[i]
            end = outer_points[i+1]
            self.add_3d_wall(start, end, total_height, wall_thickness)
        
        return self.doc
    
    def add_3d_wall(self, start_point, end_point, height, thickness):
        """Ajoute un mur en 3D entre deux points"""
        # Conversion en points 3D
        start_3d = (start_point[0], start_point[1], 0)
        end_3d = (end_point[0], end_point[1], 0)
        
        # Création d'une face 3D pour le mur
        points = [
            start_3d,
            end_3d,
            (end_3d[0], end_3d[1], height),
            (start_3d[0], start_3d[1], height)
        ]
        
        # Ajout de la face au modèle 3D
        self.msp.add_3dface(points)
    
    def export_3d_model(self, filename, format='dxf'):
        """Exporte le modèle 3D"""
        if format == 'dxf':
            self.save_dxf(filename)
        else:
            # Pour d'autres formats, nous pourrions utiliser pywavefront ou similar
            print(f"Format {format} non supporté pour le moment")
    
    def generate_simple_building(self, params):
        """Génère un bâtiment simple basé sur les paramètres"""
        length = params.get('longueur', 10)
        width = params.get('largeur', 8)
        floors = params.get('etages', 1)
        wall_thickness = params.get('epaisseur_mur', 0.2)
        
        return self.generate_3d_walls(length, width, floors, wall_thickness)

# Fonction utilitaire pour tests
def test_3d_generator():
    generator = Model3DGenerator()
    params = {
        'longueur': 12,
        'largeur': 10,
        'etages': 2,
        'epaisseur_mur': 0.25
    }
    model = generator.generate_simple_building(params)
    generator.export_3d_model("test_3d_model.dxf")
    return model

if __name__ == "__main__":
    test_3d_generator()
