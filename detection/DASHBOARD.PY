

from flask import Flask, render_template_string, request, redirect, send_file
import sqlite3
import csv
import io
from datetime import datetime, timedelta


from detection.database.activity_database import (
    get_daily_goal,
    set_daily_goal
)
app = Flask(__name__)


HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="5">
    <title>Digital Procrastination Detector</title>

<head>

    <title>Digital Procrastination Detector</title>

    <meta http-equiv="refresh" content="10">

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>

        body {
            font-family: Arial, sans-serif;
            background: #f4f6f8;
            margin: 0;
            padding: 30px;
        }

        h1 {
            text-align: center;
            margin-bottom: 10px;
        }

        .date {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }

        .cards,
        .time-section,
        .report-section {
            display: flex;
            gap: 20px;
            justify-content: center;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }

        .card,
        .time-card,
        .report-card {
            background: white;
            padding: 25px;
            width: 220px;
            text-align: center;
            border-radius: 12px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }

        .card h2,
        .time-card h2,
        .report-card h2 {
            font-size: 30px;
            margin: 10px;
        }

        .productive {
            border-top: 5px solid green;
        }

        .distraction {
            border-top: 5px solid red;
        }

        .neutral {
            border-top: 5px solid orange;
        }

        .percentage {
            background: white;
            padding: 25px;
            text-align: center;
            border-radius: 12px;
            margin: 30px auto;
            max-width: 600px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }

        .percentage h2 {
            font-size: 45px;
            margin: 10px;
        }

        /* SMART ALERT */

        .smart-alert {
            max-width: 900px;
            margin: 0 auto 30px auto;
            padding: 25px;
            text-align: center;
            border-radius: 12px;
            font-weight: bold;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }

        .smart-alert h2 {
            margin-top: 0;
        }

        .smart-warning {
            background: #fff4cc;
            color: #8a6500;
            border: 2px solid #e0b400;
        }

        .smart-danger {
            background: #ffe5cc;
            color: #a63d00;
            border: 2px solid #ff7b00;
        }

        .smart-critical {
            background: #ffdede;
            color: #a00000;
            border: 2px solid red;
        }

        .smart-success {
            background: #e0ffe8;
            color: #087a25;
            border: 2px solid green;
        }

        .goal-section {
            background: white;
            padding: 30px;
            margin: 30px auto;
            max-width: 900px;
            border-radius: 12px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            text-align: center;
        }

        .progress-container {
            width: 90%;
            height: 30px;
            background: #ddd;
            border-radius: 20px;
            margin: 20px auto;
            overflow: hidden;
        }

        .progress-bar {
            height: 100%;
            width: {{ goal_percentage }}%;
            background: green;
            border-radius: 20px;
        }

        .goal-form {
            margin-top: 25px;
        }

        .goal-form input {
            padding: 10px;
            width: 120px;
            border: 1px solid #ccc;
            border-radius: 6px;
        }

        .goal-form button {
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            background: #222;
            color: white;
            cursor: pointer;
        }

        .goal-achieved {
            color: green;
            font-size: 22px;
            font-weight: bold;
        }

        .section {
            background: white;
            padding: 25px;
            margin: 30px auto;
            max-width: 1100px;
            border-radius: 12px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }

        .chart-box {
            max-width: 750px;
        }

        .table-container {
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th {
            background: #222;
            color: white;
            padding: 12px;
        }

        td {
            padding: 12px;
            border-bottom: 1px solid #ddd;
            text-align: center;
        }

        .PRODUCTIVE {
            color: green;
            font-weight: bold;
        }

        .DISTRACTION {
            color: red;
            font-weight: bold;
        }

        .NEUTRAL {
            color: orange;
            font-weight: bold;
        }

    </style>

</head>


<body>


<h1>Digital Procrastination Detector</h1>

<div class="date">
    Daily Productivity Report — {{ today }}
</div>


<!-- SMART PROCRASTINATION ALERT -->

{% if alert_level == "warning" %}

<div class="smart-alert smart-warning">

    <h2>⚠️ PROCRASTINATION WARNING</h2>

    <p>
        You have spent
        <strong>{{ distraction_time }}</strong>
        on distracting activities.
    </p>

    <p>
        Consider returning to your productive task.
    </p>

</div>


{% elif alert_level == "danger" %}

<div class="smart-alert smart-danger">

    <h2>🟠 HIGH DISTRACTION</h2>

    <p>
        You have spent
        <strong>{{ distraction_time }}</strong>
        on distracting activities.
    </p>

    <p>
        Your distraction time is increasing.
        It's a good time to get back to work.
    </p>

</div>


{% elif alert_level == "critical" %}

<div class="smart-alert smart-critical">

    <h2>🚨 CRITICAL PROCRASTINATION ALERT</h2>

    <p>
        You have spent
        <strong>{{ distraction_time }}</strong>
        on distracting activities.
    </p>

    <p>
        Please return to your productive task.
    </p>

</div>


{% else %}

<div class="smart-alert smart-success">

    <h2>✅ PRODUCTIVITY LOOKS GOOD</h2>

    <p>
        No significant distraction detected.
    </p>

</div>

{% endif %}


<!-- ACTIVITY COUNTS -->

<div class="cards">

    <div class="card productive">

        <h3>PRODUCTIVE</h3>

        <h2>{{ productive }}</h2>

        <p>Activities Today</p>

    </div>


    <div class="card distraction">

        <h3>DISTRACTION</h3>

        <h2>{{ distraction }}</h2>

        <p>Activities Today</p>

    </div>


    <div class="card neutral">

        <h3>NEUTRAL</h3>

        <h2>{{ neutral }}</h2>

        <p>Activities Today</p>

    </div>

</div>


<!-- TIME SUMMARY -->

<div class="time-section">

    <div class="time-card productive">

        <h3>🟢 Productive Time</h3>

        <h2>{{ productive_time }}</h2>

        <p>Today</p>

    </div>


    <div class="time-card distraction">

        <h3>🔴 Distraction Time</h3>

        <h2>{{ distraction_time }}</h2>

        <p>Today</p>

    </div>


    <div class="time-card neutral">

        <h3>🟠 Neutral Time</h3>

        <h2>{{ neutral_time }}</h2>

        <p>Today</p>

    </div>

</div>


<!-- PRODUCTIVITY SCORE -->

<div class="percentage">

    <h3>Productivity Score</h3>

    <h2>{{ productivity }}%</h2>

    <p>
        Based on actual tracked time
    </p>

</div>


<!-- DAILY GOAL -->

<div class="goal-section">

    <h2>🎯 Daily Productivity Goal</h2>

    <p>
        Goal:
        <strong>{{ goal_time }}</strong>
        of productive work
    </p>


    <div class="progress-container">

        <div class="progress-bar"></div>

    </div>


    <h2>{{ goal_percentage }}%</h2>


    <p>
        {{ productive_time }}
        completed out of
        {{ goal_time }}
    </p>


    {% if goal_achieved %}

        <p class="goal-achieved">
            🎉 Goal Achieved!
            <br>
            Excellent work!
        </p>

    {% else %}

        <p>
            ⏳ {{ remaining_goal }}
            remaining to reach today's goal.
        </p>

    {% endif %}


    <form
        class="goal-form"
        method="POST"
        action="/set-goal"
    >

        <label>
            Set goal in minutes:
        </label>

        <input
            type="number"
            name="minutes"
            min="1"
            max="1440"
            value="{{ goal_minutes }}"
            required
        >

        <button type="submit">
            Update Goal
        </button>

    </form>

</div>


<!-- DAILY REPORT -->

<div class="section">

    <h2>📊 Daily Productivity Report</h2>

    <div class="report-section">

        <div class="report-card">

            <h3>Total Tracked Time</h3>

            <h2>{{ total_time }}</h2>

        </div>


        <div class="report-card">

            <h3>Productivity Score</h3>

            <h2>{{ productivity }}%</h2>

        </div>


        <div class="report-card">

            <h3>Distraction Sessions</h3>

            <h2>{{ distraction_sessions }}</h2>

        </div>


        <div class="report-card">

            <h3>Most Used Application</h3>

            <h2>{{ most_used }}</h2>

        </div>

    </div>

</div>


<!-- TODAY CHART -->

<div class="section chart-box">

    <h2>Today's Time Distribution</h2>

    <canvas id="timeChart"></canvas>

</div>


<!-- 7 DAY CHART -->

<div class="section chart-box">

    <h2>📈 7-Day Productivity Trend</h2>

    <canvas id="weeklyChart"></canvas>

</div>


<!-- 7 DAY SUMMARY -->

<div class="section">

    <h2>📅 7-Day Summary</h2>

    <div class="table-container">

        <table>

            <tr>

                <th>Date</th>
                <th>Productive Time</th>
                <th>Distraction Time</th>
                <th>Neutral Time</th>
                <th>Productivity</th>

            </tr>


            {% for day in weekly_data %}

            <tr>

                <td>{{ day.date }}</td>

                <td>{{ day.productive_time }}</td>

                <td>{{ day.distraction_time }}</td>

                <td>{{ day.neutral_time }}</td>

                <td>
                    <strong>
                        {{ day.productivity }}%
                    </strong>
                </td>

            </tr>

            {% endfor %}

        </table>

    </div>

</div>


<!-- APPLICATION ANALYSIS -->

<div class="section">

    <h2>Application-wise Time Analysis</h2>

    <div class="table-container">

        <table>

            <tr>

                <th>Application / Window</th>
                <th>Category</th>
                <th>Total Time</th>

            </tr>


            {% for application in applications %}

            <tr>

                <td>{{ application[0] }}</td>

                <td class="{{ application[1] }}">
                    {{ application[1] }}
                </td>

                <td>
                    {{ format_duration(application[2]) }}
                </td>

            </tr>

            {% endfor %}

        </table>

    </div>

</div>


<!-- ACTIVITY HISTORY -->

<div class="section">

    <h2>Activity History</h2>

    <div class="table-container">

        <table>

            <tr>

                <th>ID</th>
                <th>Time</th>
                <th>Window</th>
                <th>Category</th>
                <th>Duration</th>

            </tr>


            {% for row in rows %}

            <tr>

                <td>{{ row[0] }}</td>

                <td>{{ row[1] }}</td>

                <td>{{ row[2] }}</td>

                <td class="{{ row[3] }}">
                    {{ row[3] }}
                </td>

                <td>
                    {{ format_duration(row[4]) }}
                </td>

            </tr>

            {% endfor %}

        </table>

    </div>

</div>


<script>

const productive =
    {{ productive_seconds }};

const distraction =
    {{ distraction_seconds }};

const neutral =
    {{ neutral_seconds }};


const timeCtx =
    document.getElementById("timeChart");


new Chart(timeCtx, {

    type: "doughnut",

    data: {

        labels: [
            "Productive",
            "Distraction",
            "Neutral"
        ],

        datasets: [{

            data: [
                productive,
                distraction,
                neutral
            ]

        }]

    },

    options: {

        responsive: true,

        plugins: {

            legend: {
                position: "bottom"
            }

        }

    }

});


const weeklyLabels =
    {{ weekly_labels | safe }};

const weeklyProductivity =
    {{ weekly_productivity | safe }};


const weeklyCtx =
    document.getElementById("weeklyChart");


new Chart(weeklyCtx, {

    type: "line",

    data: {

        labels: weeklyLabels,

        datasets: [{

            label: "Productivity %",

            data: weeklyProductivity,

            tension: 0.3,

            fill: false

        }]

    },

    options: {

        responsive: true,

        scales: {

            y: {

                beginAtZero: true,

                max: 100

            }

        }

    }

});

</script>

<!-- EXPORT REPORT -->
<div class="section" style="text-align:center; margin:30px 0 50px 0;">
    <h2>📥 Download Productivity Report</h2>
    <p>Download all your tracked activity as a CSV file.</p>
    <a href="/export" style="display:inline-block; padding:15px 30px; background:#007bff; color:white; text-decoration:none; border-radius:10px; font-size:18px; font-weight:bold;">📥 Export Report</a>
</div>

</body>

</html>
"""


def format_duration(seconds):

    seconds = int(seconds or 0)

    hours = seconds // 3600

    minutes = (seconds % 3600) // 60

    remaining_seconds = seconds % 60

    if hours > 0:

        return f"{hours}h {minutes}m {remaining_seconds}s"

    elif minutes > 0:

        return f"{minutes}m {remaining_seconds}s"

    else:

        return f"{remaining_seconds}s"


def get_daily_seconds(cursor, date_string, category):

    cursor.execute("""
        SELECT COALESCE(SUM(duration), 0)
        FROM activity_log
        WHERE category = ?
        AND timestamp LIKE ?
    """, (
        category,
        date_string + "%"
    ))

    result = cursor.fetchone()[0]

    return int(result or 0)


@app.route("/")
def dashboard():

    connection = sqlite3.connect("productivity.db")

    cursor = connection.cursor()

    today = datetime.now()

    today_db = today.strftime("%Y-%m-%d")

    today_display = today.strftime("%d %B %Y")


    # Activity history

    cursor.execute("""
        SELECT
            id,
            timestamp,
            window_title,
            category,
            duration
        FROM activity_log
        WHERE timestamp LIKE ?
        ORDER BY id DESC
    """, (today_db + "%",))

    rows = cursor.fetchall()


    # Counts

    cursor.execute("""
        SELECT COUNT(*)
        FROM activity_log
        WHERE category = 'PRODUCTIVE'
        AND timestamp LIKE ?
    """, (today_db + "%",))

    productive = cursor.fetchone()[0]


    cursor.execute("""
        SELECT COUNT(*)
        FROM activity_log
        WHERE category = 'DISTRACTION'
        AND timestamp LIKE ?
    """, (today_db + "%",))

    distraction = cursor.fetchone()[0]


    cursor.execute("""
        SELECT COUNT(*)
        FROM activity_log
        WHERE category = 'NEUTRAL'
        AND timestamp LIKE ?
    """, (today_db + "%",))

    neutral = cursor.fetchone()[0]


    # Time

    productive_seconds = get_daily_seconds(
        cursor,
        today_db,
        "PRODUCTIVE"
    )

    distraction_seconds = get_daily_seconds(
        cursor,
        today_db,
        "DISTRACTION"
    )

    neutral_seconds = get_daily_seconds(
        cursor,
        today_db,
        "NEUTRAL"
    )


    total_seconds = (
        productive_seconds
        + distraction_seconds
        + neutral_seconds
    )


    if total_seconds > 0:

        productivity = round(
            (productive_seconds / total_seconds) * 100,
            1
        )

    else:

        productivity = 0


    # Most used application

    cursor.execute("""
        SELECT
            window_title,
            SUM(duration)
        FROM activity_log
        WHERE timestamp LIKE ?
        GROUP BY window_title
        ORDER BY SUM(duration) DESC
        LIMIT 1
    """, (today_db + "%",))

    most_used_result = cursor.fetchone()


    if most_used_result:

        most_used = most_used_result[0]

        if len(most_used) > 30:
            most_used = most_used[:30] + "..."

    else:

        most_used = "None"


    # Application analysis

    cursor.execute("""
        SELECT
            window_title,
            category,
            SUM(duration)
        FROM activity_log
        WHERE timestamp LIKE ?
        GROUP BY window_title, category
        ORDER BY SUM(duration) DESC
    """, (today_db + "%",))

    applications = cursor.fetchall()


    # 7-day data

    weekly_data = []

    weekly_labels = []

    weekly_productivity = []


    for days_ago in range(6, -1, -1):

        date_value = today - timedelta(
            days=days_ago
        )

        date_string = date_value.strftime(
            "%Y-%m-%d"
        )

        display_date = date_value.strftime(
            "%d %b"
        )


        day_productive = get_daily_seconds(
            cursor,
            date_string,
            "PRODUCTIVE"
        )

        day_distraction = get_daily_seconds(
            cursor,
            date_string,
            "DISTRACTION"
        )

        day_neutral = get_daily_seconds(
            cursor,
            date_string,
            "NEUTRAL"
        )


        day_total = (
            day_productive
            + day_distraction
            + day_neutral
        )


        if day_total > 0:

            day_productivity = round(
                (day_productive / day_total) * 100,
                1
            )

        else:

            day_productivity = 0


        weekly_labels.append(display_date)

        weekly_productivity.append(
            day_productivity
        )


        weekly_data.append({

            "date": display_date,

            "productive_time":
                format_duration(day_productive),

            "distraction_time":
                format_duration(day_distraction),

            "neutral_time":
                format_duration(day_neutral),

            "productivity":
                day_productivity

        })


    # Persistent goal

    goal_seconds = get_daily_goal()


    if goal_seconds <= 0:
        goal_seconds = 7200


    goal_percentage = round(
        (productive_seconds / goal_seconds) * 100,
        1
    )


    if goal_percentage > 100:
        goal_percentage = 100


    goal_achieved = (
        productive_seconds >= goal_seconds
    )


    remaining_seconds = max(
        goal_seconds - productive_seconds,
        0
    )


    remaining_goal = format_duration(
        remaining_seconds
    )


    goal_time = format_duration(
        goal_seconds
    )


    goal_minutes = goal_seconds // 60


    # ---------------------------------------
    # SMART PROCRASTINATION LEVEL
    # ---------------------------------------

    if distraction_seconds >= 300:

        alert_level = "critical"

    elif distraction_seconds >= 180:

        alert_level = "danger"

    elif distraction_seconds >= 60:

        alert_level = "warning"

    else:

        alert_level = "safe"


    connection.close()


    return render_template_string(

        HTML,

        today=today_display,

        rows=rows,

        applications=applications,

        productive=productive,

        distraction=distraction,

        neutral=neutral,

        productive_seconds=productive_seconds,

        distraction_seconds=distraction_seconds,

        neutral_seconds=neutral_seconds,

        productive_time=format_duration(
            productive_seconds
        ),

        distraction_time=format_duration(
            distraction_seconds
        ),

        neutral_time=format_duration(
            neutral_seconds
        ),

        total_time=format_duration(
            total_seconds
        ),

        productivity=productivity,

        distraction_sessions=distraction,

        most_used=most_used,

        weekly_data=weekly_data,

        weekly_labels=weekly_labels,

        weekly_productivity=weekly_productivity,

        goal_percentage=goal_percentage,

        goal_achieved=goal_achieved,

        remaining_goal=remaining_goal,

        goal_time=goal_time,

        goal_minutes=goal_minutes,

        alert_level=alert_level,

        format_duration=format_duration

    )


@app.route("/set-goal", methods=["POST"])
def update_goal():

    minutes = request.form.get(
        "minutes",
        "120"
    )

    try:

        minutes = int(minutes)

        if minutes < 1:
            minutes = 1

        if minutes > 1440:
            minutes = 1440

    except ValueError:

        minutes = 120


    set_daily_goal(minutes)

    return redirect("/")


@app.route("/export")
def export_report():

    connection = sqlite3.connect("productivity.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            timestamp,
            window_title,
            category,
            duration
        FROM activity_log
        ORDER BY timestamp DESC
    """)

    rows = cursor.fetchall()
    connection.close()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "ID",
        "Timestamp",
        "Window",
        "Category",
        "Duration (seconds)"
    ])

    for row in rows:
        writer.writerow(row)

    csv_data = output.getvalue().encode("utf-8")
    output.close()

    return send_file(
        io.BytesIO(csv_data),
        mimetype="text/csv",
        as_attachment=True,
        download_name="productivity_report.csv"
    )


if __name__ == "__main__":

    app.run(debug=True)
