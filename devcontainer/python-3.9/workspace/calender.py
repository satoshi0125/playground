#!/usr/local/bin/python3

print('hello, world!')


from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import calendar

app = Flask(__name__)

def get_calendar_data(year, month):
    cal = calendar.monthcalendar(year, month)
    today = datetime.now().date()
    first_day = datetime(year, month, 1).date()
    
    data = []
    cycle = ['A', 'B', 'C']
    cycle_index = 0
    
    for week in cal:
        week_data = []
        for day in week:
            if day == 0:
                week_data.append({'day': '', 'status': ''})
            else:
                current_date = first_day.replace(day=day)
                delta = (current_date - first_day).days
                status = cycle[(delta + cycle_index) % 3]
                week_data.append({
                    'day': day,
                    'status': status,
                    'is_today': current_date == today
                })
        data.append(week_data)
    
    return data

@app.route('/')
def index():
    today = datetime.now()
    return render_template('index.html', year=today.year, month=today.month)

@app.route('/get_calendar')
def get_calendar():
    year = int(request.args.get('year'))
    month = int(request.args.get('month'))
    data = get_calendar_data(year, month)
    return jsonify({
        'calendar': data,
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month]
    })

if __name__ == '__main__':
    app.run(debug=True)