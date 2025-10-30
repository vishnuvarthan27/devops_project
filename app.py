from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

buses = [
    {"id": 1, "route": "Chennai → Bangalore", "time": "08:00 AM", "fare": 550},
    {"id": 2, "route": "Coimbatore → Madurai", "time": "09:30 AM", "fare": 450},
    {"id": 3, "route": "Trichy → Chennai", "time": "06:00 PM", "fare": 600},
]

bookings = []

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>🚌 Bus Ticket Booking</title>
    <style>
        body { font-family: Arial; background-color: #f2f2f2; margin: 40px; }
        h1, h2 { color: #333; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; background: white; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: center; }
        th { background-color: #007BFF; color: white; }
        tr:hover { background-color: #f1f1f1; }
        form { margin-top: 20px; background: white; padding: 21px; border-radius: 8px; }
        input, select, button { padding: 10px; margin: 5px; }
        button { background-color: #007BFF; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background-color: #0056b3; }
        .container { max-width: 800px; margin: auto; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚌 Welcome to Smart Bus Ticket Booking System</h1>
        <h2>Available Buses</h2>
        <table>
            <tr><th>ID</th><th>Route</th><th>Departure</th><th>Fare (₹)</th></tr>
            {% for bus in buses %}
            <tr>
                <td>{{ bus.id }}</td>
                <td>{{ bus.route }}</td>
                <td>{{ bus.time }}</td>
                <td>{{ bus.fare }}</td>
            </tr>
            {% endfor %}
        </table>

        <h2>Book Your Ticket</h2>
        <form method="POST" action="/">
            <label>Name:</label><br>
            <input type="text" name="name" required><br>
            <label>Bus ID:</label><br>
            <select name="bus_id">
                {% for bus in buses %}
                <option value="{{ bus.id }}">{{ bus.route }}</option>
                {% endfor %}
            </select><br>
            <label>Seats:</label><br>
            <input type="number" name="seats" min="1" required><br>
            <button type="submit">Book Ticket</button>
        </form>

        <h2>🎟 Your Bookings</h2>
        <table>
            <tr><th>Name</th><th>Bus Route</th><th>Seats</th><th>Total Fare (₹)</th></tr>
            {% for b in bookings %}
            <tr>
                <td>{{ b['name'] }}</td>
                <td>{{ b['route'] }}</td>
                <td>{{ b['seats'] }}</td>
                <td>{{ b['total'] }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        bus_id = int(request.form.get("bus_id"))
        seats = int(request.form.get("seats"))

        bus = next((b for b in buses if b["id"] == bus_id), None)
        if bus:
            total = seats * bus["fare"]
            bookings.append({
                "name": name,
                "route": bus["route"],
                "seats": seats,
                "total": total
            })
        return redirect(url_for("index"))

    return render_template_string(html_template, buses=buses, bookings=bookings)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
