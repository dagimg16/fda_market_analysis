import requests
import pandas as pd

def fetch_approvals(limit=500):
    try:
        url = f"https://api.fda.gov/drug/drugsfda.json?limit={limit}" 
        response= requests.get(url)
        data = response.json()

        records= []

        try:
            for result in data['results']:
                sponsor = result.get('sponsor_name')
                product = result.get('products', [])
                if product:
                    drug_name = product[0]['brand_name']
                else:
                    drug_name = None
                for app in result.get('submissions', []):
                    record = {
                        'company': sponsor,
                        'drug_name': drug_name,
                        'submission_type': app.get('submission_type'),
                        'submission_number': app.get('submission_number'),
                        'submission_status': app.get('submission_status'),
                        'submission_status_date': app.get('submission_status_date'),
                        'submission_class_code': app.get('submission_class_code', None)
                    }
                    records.append(record)
        except:
            print("Error while extracting data from JSON file")    
        return pd.DataFrame(records)
    except:
        print("API data retrieval failed")

#Run and save to CSV
df = fetch_approvals(500)        
df.to_csv("historical_approvals.csv", index=False)


