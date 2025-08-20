import ezdxf
from ezdxf import units
import math

class PlanGenerator:
    def __init__(self):
        self.doc = None
        self.msp = None
        
    def create_new_document(self):
        """Crée un nouveau document DXF"""
        self.doc = ezdxf.new('R2010')
        self.doc.units = units.M
        self.msp = self.doc.modelspace()
        return self.doc
    
    def add_wall(self, start_point, end_point, thickness=0.2):
        """Ajoute un mur entre deux points avec une épaisseur donnée"""
        # Calcul de la direction du mur
        dx = end_point[0] - start_point[0]
        dy = end_point[1] - start_point[1]
        length = math.sqrt(dx**2 + dy**2)
        
        if length == 0:
            return
            
        # Normalisation
        dx, dy = dx/length, dy/length
        
        # Points pour le mur avec épaisseur
        perp_dx, perp_dy = -dy, dx  # Vecteur perpendiculaire
        
        # Points extérieurs du mur
        p1 = (start_point[0] + perp_dx * thickness/2, start_point[1] + perp_dy * thickness/2)
        p2 = (end_point[0] + perp_dx * thickness/2, end_point[1] + perp_dy * thickness/2)
        p3 = (end_point[0] - perp_dx * thickness/2, end_point[1] - perp_dy * thickness/2)
        p4 = (start_point[0] - perp_dx * thickness/2, start_point[1] - perp_dy * thickness/2)
        
        # Création du polygone du mur
        self.msp.add_lwpolyline([p1, p2, p3, p4, p1])
        
        return (p1, p2, p3, p4)
    
    def generate_simple_rectangular_plan(self, length, width, wall_thickness=0.2):
        """Génère un plan rectangulaire simple"""
        self.create_new_document()
        
        # Points du rectangle
        points = [
            (0, 0),
            (length, 0),
            (length, width),
            (0, width),
            (0, 0)
        ]
        
        # Ajout des murs
        for i in range(4):
            start = points[i]
            end = points[i+1]
            self.add_wall(start, end, wall_thickness)
        
        # Ajout des cotations
        self.add_dimensions(length, width)
        
        return self.doc
    
    def add_dimensions(self, length, width):
        """Ajoute des cotations au plan"""
        # Cotation horizontale
        self.msp.add_linear_dim(
            base=(0, -2),
            p1=(0, 0),
            p2=(length, 0),
            dimstyle="EZDXF"
        )
        
        # Cotation verticale
        self.msp.add_linear_dim(
            base=(-2, 0),
            p1=(0, 0),
            p2=(0, width),
            dimstyle="EZDXF"
        )
    
    def save_dxf(self, filename):
        """Sauvegarde le document DXF"""
        if self.doc:
            self.doc.saveas(filename)
            print(f"Plan sauvegardé sous {filename}")
        else:
            print("Aucun document à sauvegarder")

# Fonction utilitaire pour tests
def test_generator():
    generator = PlanGenerator()
    plan = generator.generate_simple_rectangular_plan(10, 8, 0.2)
    generator.save_dxf("test_plan.dxf")
    return plan

if __name__ == "__main__":
    test_generator()
