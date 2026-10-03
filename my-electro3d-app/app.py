from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)

# Direct route to serve the Google Verification HTML file
@app.route("/google7aa978d49123db61.html")
def google_verify():
    return send_from_directory("templates", "google7aa978d49123db61.html")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/microcontrollers")
def microcontrollers():
    return render_template("microcontrollers.html")

@app.route("/switches")
def switches():
    return render_template("switches.html")

@app.route("/circuits")
def circuits():
    return render_template("circuits.html")

# Complete Simulation Backend API
@app.route("/api/simulate-circuit", methods=["POST"])
def simulate_circuit():
    data = request.json or {}
    circuit_id = data.get("circuit_id")
    state = data.get("state", False)
    
    # Safely convert numeric input values
    try:
        val = float(data.get("value", 0))
    except (ValueError, TypeError):
        val = 0.0

    # 1. Relay Circuit Logic
    if circuit_id == "relay":
        return jsonify({
            "status": "ON 💡" if state else "OFF 🔌",
            "voltage_ac": "230V AC Connected" if state else "0V AC (Isolated)",
            "output_msg": "Relay coil energized! AC Light Bulb is ON." if state else "Relay contact open. AC Load is powered off."
        })
    
    # 2. SSR Circuit Logic
    elif circuit_id == "ssr":
        firing_pct = int(val)
        return jsonify({
            "triac_state": f"CONDUCTING ({firing_pct}%) 🔥" if firing_pct > 0 else "IDLE / OFF 💤",
            "output_msg": f"Solid State Relay firing at {firing_pct}% power. Zero mechanical noise." if firing_pct > 0 else "SSR Control input LOW. Load OFF."
        })

    # 3. Sonar Distance Logic
    elif circuit_id == "sonar":
        dist_cm = max(2, min(400, int(val)))
        time_us = int(dist_cm * 58.8)
        alarm = dist_cm < 20
        return jsonify({
            "distance_cm": dist_cm,
            "flight_time_us": f"{time_us} µs",
            "alarm_active": alarm,
            "output_msg": f"Sonic reflection at {dist_cm} cm! " + ("🚨 ALARM TRIGGERED (Object < 20cm)!" if alarm else "Clear path ahead.")
        })

    # 4. PIR Motion Logic
    elif circuit_id == "pir":
        return jsonify({
            "status": "MOTION DETECTED 🚨" if state else "NO MOTION 👁️",
            "output_msg": "IR signature movement detected! Security Siren & Alarm LED ACTIVE." if state else "Infrared spectrum steady. Zone clear."
        })

    # 5. MOSFET PWM Logic
    elif circuit_id == "mosfet":
        duty_pct = int((val / 255.0) * 100)
        rpm = int((val / 255.0) * 3000)
        return jsonify({
            "duty_cycle": f"{duty_pct}%",
            "motor_rpm": f"{rpm} RPM",
            "output_msg": f"MOSFET PWM set to {int(val)}/255. DC Motor rotating at {rpm} RPM." if val > 0 else "MOSFET Gate OFF. Motor stopped."
        })

    # 6. Servo Motor Logic
    elif circuit_id == "servo":
        angle = int(val)
        pulse = 1000 + int((angle / 180.0) * 1000)
        return jsonify({
            "angle": f"{angle}°",
            "pulse_width": f"{pulse} µs",
            "output_msg": f"Servo horn rotated to {angle} degrees position."
        })

    # 7. LDR Light Sensor Logic
    elif circuit_id == "ldr":
        lux = int(val)
        is_dark = lux < 300
        return jsonify({
            "raw_adc": int((lux / 1000.0) * 1023),
            "lux_level": f"{lux} Lux",
            "light_state": "DARK / NIGHT 🌙" if is_dark else "DAYLIGHT ☀️",
            "output_msg": "Low light level detected! Street light relay ACTIVATED." if is_dark else "Daylight sufficient. Street light turned OFF."
        })

    return jsonify({"output_msg": "Simulation updated."})

if __name__ == "__main__":
    app.run(port=8080, debug=False)
