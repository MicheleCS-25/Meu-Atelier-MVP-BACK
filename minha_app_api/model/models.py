from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Material(db.Model):
    # ID como chave primária
    id = db.Column(db.Integer, primary_key=True)

    # Detalhes do Material
    nome_material = db.Column(db.String(100), unique=True, nullable=False)
    data_cadastro = db.Column(db.String(10), nullable=False) # Armazenada como string (YYYY-MM-DD)
    quantidade_em_estoque = db.Column(db.Integer, nullable=False)
    valor_material = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f'<Material {self.nome_material}>'