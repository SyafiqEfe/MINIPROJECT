from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    player_choice = None
    computer_choice = None
    choices = ["Batu", "Kertas", "Gunting"]

    if request.method == 'POST':
        player_choice = int(request.form.get('choice'))
        computer_choice = random.randint(0, 2)

        if player_choice == computer_choice:
            result = "Seri!"
        elif (player_choice == 0 and computer_choice == 2) or \
             (player_choice == 1 and computer_choice == 0) or \
             (player_choice == 2 and computer_choice == 1):
            result = "Kamu Menang!"
        else:
            result = "Kamu Kalah!"

    return render_template('index.html', result=result, 
                           player_choice=player_choice, 
                           computer_choice=computer_choice, 
                           choices=choices)

if __name__ == '__main__':
    app.run(debug=True)
