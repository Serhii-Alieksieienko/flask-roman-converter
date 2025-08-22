# main.py
import os
from flask import Flask, render_template, request, jsonify
import converter  # Замість calendar_main

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home_page():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    try:
        # Отримуємо тип конвертації (за замовчуванням to_roman)
        conversion_type = request.form.get("type", "to_roman")
        
        if conversion_type == "to_roman":
            # Конвертуємо число в римське
            number = int(request.form["number"])
            roman = converter.number_to_roman(number)
            return render_template("convert.html", 
                                 input_value=number,
                                 result=roman,
                                 conversion_type="Number to Roman")
        else:
            # Якщо у вас немає функції roman_to_number, 
            # тимчасово можна просто показати повідомлення
            return render_template("convert.html", 
                                 error="Roman to Number conversion not yet implemented")
            
    except ValueError as e:
        return render_template("convert.html", error=str(e))
    except Exception as e:
        return render_template("convert.html", 
                             error="An unexpected error occurred. Please try again.")

# Додайте простий API endpoint для live preview (опціонально)
@app.route("/api/convert", methods=["POST"])
def api_convert():
    try:
        data = request.get_json()
        conversion_type = data.get("type", "to_roman")
        
        if conversion_type == "to_roman":
            number = int(data["value"])
            result = converter.number_to_roman(number)
        else:
            # Тимчасово повертаємо помилку
            return jsonify({"success": False, "error": "Not implemented"}), 501
            
        return jsonify({"success": True, "result": result})
        
    except (ValueError, KeyError) as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))