from flask import Flask, jsonify, request, render_template
from flasgger import Swagger
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import os
from flask import Flask, render_template


base_dir = os.path.abspath(os.path.dirname(__file__))

# 2. Pega o caminho da pasta raiz (meu_atelier) subindo um nível
root_dir = os.path.dirname(base_dir)
template_path = os.path.join(root_dir, 'meu_front', 'templates')
static_path = os.path.join(root_dir, 'meu_front', 'static')

app = Flask(__name__,
            template_folder=template_path,
            static_folder=static_path)


# 3. Define os caminhos exatos para as pastas que estão em meu_front
template_path = os.path.join(root_dir, 'meu_front', 'templates')
static_path = os.path.join(root_dir, 'meu_front', 'static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# INICIALIZAÇÃO DAS EXTENSÕES (O db deve vir antes do Model)
db = SQLAlchemy(app)
CORS(app)
swagger = Swagger(app)



class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_material = db.Column(db.String(100), nullable=False, unique=True)
    data_cadastro = db.Column(db.Date, nullable=False)
    quantidade_em_estoque = db.Column(db.Integer, nullable=False)
    valor_material = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    """
    Página Principal
    ---
    responses:
      200:
        description: Retorna o index.html
    """
    return render_template('index.html')

@app.route('/cadastrar_material', methods=['POST'])
def cadastrar_material():
    """
    Cadastrar Material
    ---
    tags:
      - Materiais
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: MaterialInput
          required:
            - nome_material
            - data_cadastro
            - quantidade_em_estoque
            - valor_material
          properties:
            nome_material:
              type: string
            data_cadastro:
              type: string
              format: date
            quantidade_em_estoque:
              type: integer
            valor_material:
              type: number
    responses:
      201:
        description: Cadastrado com sucesso
      400:
        description: Erro nos dados
    """
    try:
        data = request.get_json()
        
        # Converte string de data para objeto date do Python
        data_formatada = datetime.strptime(data['data_cadastro'], '%Y-%m-%d').date()

        novo = Material(
            nome_material=data['nome_material'], 
            data_cadastro=data_formatada,
            quantidade_em_estoque=int(data['quantidade_em_estoque']),
            valor_material=float(data['valor_material'])
        )
        db.session.add(novo)
        db.session.commit()
        return jsonify({'message': 'Material cadastrado com sucesso!'}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Erro: Material já existe.'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro interno: {str(e)}'}), 500

@app.route('/buscar_materiais', methods=['GET'])
def buscar_materiais():
    """
    Listar Materiais
    ---
    tags:
      - Materiais
    responses:
      200:
        description: Lista de materiais cadastrados
    """
    try:
        materiais = Material.query.all()
        # IMPORTANTE: .strftime('%Y-%m-%d') evita erro de serialização no JSON
        resultado = [{
            'id': m.id,
            'nome_material': m.nome_material,
            'data_cadastro': m.data_cadastro.strftime('%Y-%m-%d'),
            'quantidade_em_estoque': m.quantidade_em_estoque,
            'valor_material': f"{m.valor_material:.2f}"
        } for m in materiais]
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/deletar_material/<int:id>', methods=['DELETE'])
def deletar_material(id):
    """
    Deletar Material
    ---
    tags:
      - Materiais
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Deletado com sucesso
    """
    material = Material.query.get(id)
    if material:
        db.session.delete(material)
        db.session.commit()
        return jsonify({'message': 'Deletado com sucesso.'}), 200
    return jsonify({'message': 'Não encontrado.'}), 404

if __name__ == '__main__':
    app.run(debug=True)