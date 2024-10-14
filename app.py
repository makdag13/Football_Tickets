from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database initialization function
def init_db():
    conn = sqlite3.connect('ticket_system.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )
    ''')

    # Matches table
    c.execute('''
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team1 TEXT NOT NULL,
        team2 TEXT NOT NULL,
        match_date TEXT NOT NULL
    )
    ''')

    # Tickets table
    c.execute('''
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        match_id INTEGER NOT NULL,
        seat_number INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (match_id) REFERENCES matches(id)
    )
    ''')

    conn.commit()
    conn.close()

# Call the function to initialize the database
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buy_ticket', methods=['GET', 'POST'])
def buy_ticket():
    if request.method == 'POST':
        seat_number = request.form['seat_number']
        # Add ticket to the database
        conn = sqlite3.connect('ticket_system.db')
        c = conn.cursor()
        c.execute('INSERT INTO tickets (user_id, match_id, seat_number) VALUES (?, ?, ?)', (1, 1, seat_number))
        conn.commit()
        conn.close()
        return redirect('/confirmation')

    # Show available seats
    total_seats = range(1, 51)  # Assuming 50 seats are available
    return render_template('buy_ticket.html', available_seats=total_seats)

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

if __name__ == '__main__':
    app.run(debug=True)
