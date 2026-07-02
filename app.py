from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

comandas_db = []
contador_id = 1 
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/comandas")
def comandas():
    return render_template("comandas.html")

@app.route("/api/comandas", methods=["GET"])
def get_comandas():
    return jsonify(comandas_db)

@app.route("/api/comandas", methods=["POST"])
def add_comanda():
    global contador_id
    data = request.get_json()
    
    quantidade = int(data['quantidade'])
    valor = float(data['valor'])
    total = quantidade * valor
    
    nova_comanda = {
        "id": contador_id,
        "cliente": data['cliente'],
        "mesa": data['mesa'],
        "pedido": data['pedido'],
        "quantidade": quantidade,
        "valor": valor,
        "total": total
    }
    
    comandas_db.append(nova_comanda)
    contador_id += 1
    
    return jsonify(nova_comanda), 201

@app.route("/api/comandas/<int:id>", methods=["PUT"])
def update_comanda(id):
    global comandas_db
    data = request.get_json()
    
    for comanda in comandas_db:
        if comanda['id'] == id:
            quantidade = int(data['quantidade'])
            valor = float(data['valor'])
            
            comanda['cliente'] = data['cliente']
            comanda['mesa'] = data['mesa']
            comanda['pedido'] = data['pedido']
            comanda['quantidade'] = quantidade
            comanda['valor'] = valor
            comanda['total'] = quantidade * valor # Reclacula o total
            return jsonify(comanda), 200
            
    return jsonify({"mensagem": "Comanda não encontrada"}), 404

@app.route("/api/comandas/<int:id>", methods=["DELETE"])
def delete_comanda(id):
    global comandas_db
    comandas_db = [c for c in comandas_db if c['id'] != id]
    return jsonify({"mensagem": "Comanda removida com sucesso"}), 200

if __name__ == "__main__":
    app.run(debug=True)