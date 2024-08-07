from flask import Flask, request, render_template_string
import pickle

app = Flask(__name__)

# Load the model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

# Define improved HTML template with dropdowns
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>House Rent Prediction</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
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
        .result {
            margin-top: 20px;
            font-size: 18px;
            color: #28a745;
        }
        .error {
            color: #dc3545;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>House Rent Prediction</h1>
        <form action="/predict" method="post">
            <div class="form-group">
                <label for="area">Area (in sq ft):</label>
                <input type="text" id="area" name="area" required>
            </div>

            <div class="form-group">
                <label for="type">Type:</label>
                <select id="type" name="type" required>
                    <option value="1">1 BHK</option>
                    <option value="2">2 BHK</option>
                    <option value="3">3 BHK</option>
                    <option value="4">4 BHK</option>
                    <option value="5">5 BHK</option>
                </select>
            </div>

            <div class="form-group">
                <label for="bathrooms">Bathrooms:</label>
                <input type="text" id="bathrooms" name="bathrooms" required>
            </div>

            <div class="form-group">
                <label for="furnished_type">Furnished Type (0=Unfurnished, 1=Furnished):</label>
                <input type="text" id="furnished_type" name="furnished_type" required>
            </div>

            <div class="form-group">
                <label for="localityclass">Locality Class:</label>
                <input type="text" id="localityclass" name="localityclass" required>
            </div>

            <div class="form-group">
                <label for="city">City:</label>
                <select id="city" name="city" required>
                    <option value="1">Bangalore</option>
                    <!-- Add other cities if needed -->
                </select>
            </div>

            <input type="submit" value="Predict">
        </form>

        {% if prediction_text %}
            <div class="result">{{ prediction_text }}</div>
        {% endif %}
        {% if error_text %}
            <div class="error">{{ error_text }}</div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract features from the form
        area = float(request.form['area'])
        type_ = int(request.form['type'])
        bathrooms = int(request.form['bathrooms'])
        furnished_type = int(request.form['furnished_type'])
        localityclass = int(request.form['localityclass'])
        city = int(request.form['city'])  # Map this to your model's encoding if necessary

        # Prepare the feature vector
        features = [[area, type_, bathrooms, furnished_type, localityclass, city]]

        # Predict
        prediction = model.predict(features)[0]

        prediction_text = f"The house rent prediction is Rs. {round(prediction, 2)} lakhs"
        return render_template_string(HTML_TEMPLATE, prediction_text=prediction_text)
    except Exception as e:
        error_text = f"Error: {str(e)}"
        return render_template_string(HTML_TEMPLATE, error_text=error_text)

if __name__ == "__main__":
    app.run(debug=True)
