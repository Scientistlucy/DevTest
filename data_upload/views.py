# Create your views here.
import pandas as pd
from django.shortcuts import render
from .forms import UploadFileForm
from django.contrib import messages  # Import messages for alerts

def handle_uploaded_file(f):
    # This function will handle both Excel and CSV files
    if f.name.endswith('.xlsx'):
        df = pd.read_excel(f)
    elif f.name.endswith('.csv'):
        df = pd.read_csv(f)
    else:
        return None, 'file_type'  # Return 'file_type' error for unsupported file types

    # Check if necessary columns exist
    required_columns = ['Cust State', 'Cust Pin', 'DPD']
    if not all(column in df.columns for column in required_columns):
        return None, 'missing_columns'  # Return 'missing_columns' error if columns are missing

    # Create a summary report
    summary = df.groupby('Cust State').agg({'DPD': 'sum'}).reset_index()
    return summary, None  # Return the summary with no error

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            summary, error_type = handle_uploaded_file(request.FILES['file'])
            
            if summary is not None:
                # Add a success message
                messages.success(request, 'You have successfully uploaded the file.')
                # Add logic to handle the summary if needed
            else:
                if error_type == 'file_type':
                    # Add an error message for unsupported file types
                    messages.error(request, 'Invalid file type. Please upload an Excel (.xlsx) or CSV (.csv) file.')
                elif error_type == 'missing_columns':
                    # Add an error message for missing required columns
                    messages.error(request, 'Uploaded file must contain "Cust State," "Cust Pin," and "DPD" columns.')
    else:
        form = UploadFileForm()
    
    return render(request, 'data_upload/upload.html', {'form': form})
