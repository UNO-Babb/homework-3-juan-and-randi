from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Variables globales
current_player = 1
player_money = {1: 1000, 2: 1000}
events = []
clicked_tiles = set()
tile_events = {}

# Función para cargar eventos desde el archivo
def load_events():
    with open('events.txt', 'r') as file:
        return [line.strip() for line in file]

# Función para reiniciar todo
def reset_game():
    global current_player, player_money, clicked_tiles, tile_events, events
    current_player = 1
    player_money = {1: 1000, 2: 1000}
    clicked_tiles = set()
    events = load_events()
    random.shuffle(events)
    tile_events = {i+1: events[i] for i in range(min(25, len(events)))}

# Inicia el juego al cargar
reset_game()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_tile/<int:tile_id>')
def add_tile(tile_id):
    global current_player

    if tile_id in clicked_tiles:
        return jsonify(
            message="Already clicked!",
            color="gray",
            player=current_player,
            money=player_money[current_player],
            next_player=current_player,
            game_over=False
        )

    clicked_tiles.add(tile_id)
    color = 'green' if current_player == 1 else 'blue'
    event = tile_events.get(tile_id, "Free space, No event")

    # Obtener monto
    amount = 0
    for word in event.split():
        try:
            if '+/-' in word:
                amount = random.choice([200, -200])
            elif word.startswith('+') or word.startswith('-'):
                amount = int(word.replace(',', ''))
        except:
            continue

    display_player = current_player
    player_money[display_player] += amount
    message = f"Player {display_player}: {event}"

    game_over = player_money[display_player] >= 5000
    current_money = player_money[display_player]
    next_player = 2 if current_player == 1 else 1
    current_player = next_player

    return jsonify(
        color=color,
        message=message,
        player=display_player,
        money=current_money,
        next_player=next_player,
        player1_money=player_money[1],
        player2_money=player_money[2],
        game_over=game_over
    )

@app.route('/reset', methods=['POST'])
def reset():
    reset_game()
    return jsonify(status="reset",
                   player1_money=player_money[1],
                   player2_money=player_money[2],
                   current_player=current_player)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)






