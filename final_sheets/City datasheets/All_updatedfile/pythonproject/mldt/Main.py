from flask import Flask, request, render_template_string, redirect, url_for
import pickle

app = Flask(__name__)

# Load the model
with open('modelrf.pkl', 'rb') as file:
    model = pickle.load(file)

# Define the HTML templates
HTML_TEMPLATE_FORM = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>House Rent Prediction</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
    <style>
        body {
            background-color: #f8f9fa;
            text-align: center;
            padding-top: 50px;
        }
        .container {
            max-width: 600px;
            margin: auto;
            background: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #343a40;
            margin-bottom: 20px;
        }
        label {
            font-weight: bold;
        }
        select, input[type="text"] {
            width: 100%;
            padding: 8px;
            margin-bottom: 15px;
            border-radius: 4px;
            border: 1px solid #ced4da;
        }
        input[type="submit"] {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>House Rent Prediction</h1>
        <form action="/predict" method="post">
            <div class="form-group">
                <label for="area">Area (in sq ft):</label>
                <input type="text" id="area" name="area" value="{{ area }}" required>
            </div>
            <div class="form-group">
                <label for="type">Type:</label>
                <select id="type" name="type" required>
                    <option value="1" {% if type_ == 1 %}selected{% endif %}>1 BHK</option>
                    <option value="2" {% if type_ == 2 %}selected{% endif %}>2 BHK</option>
                    <option value="3" {% if type_ == 3 %}selected{% endif %}>3 BHK</option>
                    <option value="4" {% if type_ == 4 %}selected{% endif %}>4 BHK</option>
                    <option value="5" {% if type_ == 5 %}selected{% endif %}>5 BHK</option>
                </select>
            </div>
            <div class="form-group">
                <label for="bathrooms">Bathrooms:</label>
                <select id="bathrooms" name="bathrooms" required>
                    <option value="1" {% if bathrooms == 1 %}selected{% endif %}>1</option>
                    <option value="2" {% if bathrooms == 2 %}selected{% endif %}>2</option>
                    <option value="3" {% if bathrooms == 3 %}selected{% endif %}>3</option>
                    <option value="4" {% if bathrooms == 4 %}selected{% endif %}>4</option>
                    <option value="5" {% if bathrooms == 5 %}selected{% endif %}>5</option>
                </select>
            </div>
            <div class="form-group">
                <label for="furnished_type">Furnished Type:</label>
                <select id="furnished_type" name="furnished_type" required>
                    <option value="0" {% if furnished_type == 0 %}selected{% endif %}>Furnished</option>
                    <option value="1" {% if furnished_type == 1 %}selected{% endif %}>Semi-Furnished</option>
                    <option value="2" {% if furnished_type == 2 %}selected{% endif %}>Unfurnished</option>
                </select>
            </div>
            <div class="form-group">
                <label for="localityclass">Locality Class:</label>
                <select id="localityclass" name="localityclass" required>
                    <option value="0" {% if localityclass == 0 %}selected{% endif %}>Primetown</option>
                    <option value="1" {% if localityclass == 1 %}selected{% endif %}>Uptown</option>
                    <option value="2" {% if localityclass == 2 %}selected{% endif %}>Suburb</option>
                </select>
            </div>
            <div class="form-group">
                <label for="city">City:</label>
                <select id="city" name="city" required>
                    <option value="0" {% if city == 0 %}selected{% endif %}>Ahmedabad</option>
                    <option value="1" {% if city == 1 %}selected{% endif %}>Bangalore</option>
                    <option value="2" {% if city == 2 %}selected{% endif %}>Chennai</option>
                    <option value="3" {% if city == 3 %}selected{% endif %}>Delhi</option>
                    <option value="4" {% if city == 4 %}selected{% endif %}>Gurgaon</option>
                    <option value="5" {% if city == 5 %}selected{% endif %}>Hyderabad</option>
                    <option value="6" {% if city == 6 %}selected{% endif %}>Kolkata</option>
                    <option value="7" {% if city == 7 %}selected{% endif %}>Mumbai</option>
                    <option value="8" {% if city == 8 %}selected{% endif %}>Noida</option>
                    <option value="9" {% if city == 9 %}selected{% endif %}>Pune</option>
                </select>
            </div>
            <input type="submit" value="Predict">
        </form>
    </div>
</body>
</html>
'''

HTML_TEMPLATE_RESULT = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prediction Result</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
    <style>
        body {
            background-color: #e9ecef;
            text-align: center;
            padding-top: 50px;
        }
        .container {
            max-width: 600px;
            margin: auto;
            background: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #343a40;
            margin-bottom: 20px;
        }
        .result {
            font-size: 24px;
            color: #28a745;
            margin-bottom: 20px;
        }
        .btn {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            text-decoration: none;
        }
        .btn:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Prediction Result</h1>
        <div class="result">{{ prediction_text }}</div>
        <a href="/" class="btn">Back to Prediction Form</a>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE_FORM, area='', type_=1, bathrooms=1, furnished_type=0, localityclass=0, city=0)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract features from the form
        area = float(request.form['area'])
        type_ = int(request.form['type'])
        bathrooms = int(request.form['bathrooms'])
        furnished_type = int(request.form['furnished_type'])
        localityclass = int(request.form['localityclass'])
        city = int(request.form['city'])

        # Validate inputs
        if area <= 0 or bathrooms <= 0:
            raise ValueError("Invalid input values for area or bathrooms.")

        # Prepare the feature vector
        features = [[area, type_, bathrooms, furnished_type, localityclass, city]]

        # Predict
        prediction = model.predict(features)[0]

        # Convert the prediction to thousands and round to the nearest integer
        prediction_in_thousands = round(prediction)

        prediction_text = f"The house rent prediction is Rs. {prediction_in_thousands} thousands."
        return render_template_string(HTML_TEMPLATE_RESULT, prediction_text=prediction_text)
    except Exception as e:
        return render_template_string(HTML_TEMPLATE_RESULT, prediction_text=f"Error: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)

