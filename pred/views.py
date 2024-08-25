from django.shortcuts import render
from joblib import load
import pandas as pd

# Load the model
model = load('./place_model/placement_model.pkl')

# Create your views here
def form(request):
    result = ''
    if request.method == 'POST':
        # Extract data from the request
        try:
            Age = int(request.POST.get('age', 0))
            Gender = request.POST.get('gender')
            Stream = request.POST.get('stream')
            internship = request.POST.get('internship')
            hist_of_backlog = request.POST.get('history_of_backlogs')
            CGPA = float(request.POST.get('cgpa', 0))
            
            # Encode categorical features
            Internships = 1 if internship == 'Yes' else 0
            HistoryOfBacklogs = 1 if hist_of_backlog == 'Yes' else 0
            
            # Prepare input data
            input_data = pd.DataFrame({
                'Age': [Age],
                'Gender': [Gender],
                'Stream': [Stream],
                'Internships': [Internships],
                'CGPA': [CGPA],
                'HistoryOfBacklogs': [HistoryOfBacklogs]
            })
            
            # Debug: print input data to check format
            print("Input Data:", input_data)
            
            # Make prediction
            try:
                prediction = model.predict(input_data)[0]
                print("Prediction:", prediction)
                if prediction == 1:
                    result = 'Placed'
                else:
                    result = 'Not Placed'
            except Exception as e:
                result = f'Prediction Error: {e}'
        
        except Exception as e:
            result = f'Error: {e}'

    return render(request, 'form.html', {'result': result})
