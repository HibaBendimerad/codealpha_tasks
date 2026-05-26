from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import uuid
import re
from database import create_database

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("bus_pass.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    """Home page — show all available routes"""
    conn = get_db()
    routes = conn.execute("SELECT * FROM routes WHERE available_seats > 0").fetchall()
    conn.close()
    return render_template("index.html", routes=routes)

@app.route("/book/<int:route_id>")
def book(route_id):
    """Booking page for a specific route"""
    conn = get_db()
    route = conn.execute("SELECT * FROM routes WHERE id = ?", (route_id,)).fetchone()
    conn.close()
    if not route:
        return "Route not found!", 404
    return render_template("booking.html", route=route)

@app.route("/confirm", methods=["POST"])
def confirm():
    """Process booking and generate ticket"""
    name  = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    route_id = request.form.get("route_id")

    # Validate inputs
    if not name or not email or not route_id:
        return "All fields are required!", 400
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "Invalid email address!", 400

    conn = get_db()
    route = conn.execute("SELECT * FROM routes WHERE id = ?", (route_id,)).fetchone()

    if not route or route["available_seats"] <= 0:
        conn.close()
        return "No seats available!", 400

    # Generate unique ticket number
    ticket_number = "BP-" + str(uuid.uuid4()).upper()[:12]
    seat_number   = 41 - route["available_seats"]

    # Save ticket
    conn.execute("""
        INSERT INTO tickets (ticket_number, passenger_name, passenger_email, route_id, seat_number)
        VALUES (?, ?, ?, ?, ?)
    """, (ticket_number, name, email, route_id, seat_number))

    # Update available seats
    conn.execute("""
        UPDATE routes SET available_seats = available_seats - 1 WHERE id = ?
    """, (route_id,))

    conn.commit()

    ticket = conn.execute("""
        SELECT t.*, r.origin, r.destination, r.departure_time, r.arrival_time, r.price
        FROM tickets t JOIN routes r ON t.route_id = r.id
        WHERE t.ticket_number = ?
    """, (ticket_number,)).fetchone()
    conn.close()

    return render_template("confirm.html", ticket=ticket)

@app.route("/tickets")
def tickets():
    """Display all booked tickets"""
    conn = get_db()
    all_tickets = conn.execute("""
        SELECT t.*, r.origin, r.destination, r.departure_time, r.arrival_time, r.price
        FROM tickets t JOIN routes r ON t.route_id = r.id
        ORDER BY t.booking_date DESC
    """).fetchall()
    conn.close()
    return render_template("tickets.html", tickets=all_tickets)

if __name__ == "__main__":
    create_database()
    print("🚌 Bus Pass System running at http://127.0.0.1:5000")
    app.run(debug=True)