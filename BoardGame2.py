from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Game state
player_turn = 1
money = {1: 1000, 2: 1000}
tiles_clicked = set()
tile_event = {}
all_events = []

# Load events from file
def load_events():
    events = []
    with open('events.txt', 'r') as f:
        for line in f:
            events.append(line.strip())
    return events

# Reset the whole game
def start_new_game():
    global player_turn, money, tiles_clicked, tile_event, all_events
    player_turn = 1
    money = {1: 1000, 2: 1000}
    tiles_clicked = set()
    all_events = load_events()
    random.shuffle(all_events)
    tile_event = {}
    for i in range(min(25, len(all_events))):
        tile_event[i + 1] = all_events[i]

# Start game when app loads
start_new_game()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_tile/<int:tile_id>')
def handle_tile(tile_id):
    global player_turn

    if tile_id in tiles_clicked:
        return jsonify(
            message="Tile already used.",
            color="gray",
            player=player_turn,
            money=money[player_turn],
            next_player=player_turn,
            game_over=False
        )

    tiles_clicked.add(tile_id)
    color = 'green' if player_turn == 1 else 'blue'

    event = tile_event.get(tile_id, "No event")
    change = 0

    # Try to find money change in the event text
    words = event.split()
    for word in words:
        if '+/-' in word:
            change = random.choice([200, -200])
        elif word.startswith('+') or word.startswith('-'):
            try:
                change = int(word.replace(',', ''))
            except:
                pass

    money[player_turn] += change
    msg = "Player " + str(player_turn) + ": " + event

    win = money[player_turn] >= 5000
    current_money = money[player_turn]

    next_turn = 2 if player_turn == 1 else 1
    player_turn = next_turn

    return jsonify(
        color=color,
        message=msg,
        player=player_turn,
        money=current_money,
        next_player=next_turn,
        player1_money=money[1],
        player2_money=money[2],
        game_over=win
    )

@app.route('/reset', methods=['POST'])
def reset():
    start_new_game()
    return jsonify(
        status="reset",
        player1_money=money[1],
        player2_money=money[2],
        current_player=player_turn
    )



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
