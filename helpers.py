


def save_html_content(html_content, filename):
    import os

    # Ensure the mock_data directory exists
    os.makedirs("mock_data", exist_ok=True)
    
    # Save the HTML content to a file
    filepath = os.path.join("mock_data", filename)
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(html_content)
    print(f"Saved HTML content to {filepath}")

def saveMockData(results):
    # Save the HTML content of each result to a file
    for i, result in enumerate(results):
        if result.success:
            filename = f"business_{i}.html"
            save_html_content(result.cleaned_html, filename)
        else:
            print(f"Failed to save result {i}: {result.error_message}")


def saveToJson(results):
    import json
    # Save results to a JSON file
    with open("crawl_results.json", "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4)
    print("Results saved to crawl_results.json")

def save_results_to_json(new_results, filename="crawl_results.json"):
    import json
    import os

    # Check if the file exists
    if os.path.exists(filename):
        # Load existing data
        with open(filename, "r", encoding="utf-8") as file:
            existing_data = json.load(file)
    else:
        # Initialize an empty list if the file does not exist
        existing_data = []

    # Create a set of existing URLs for quick lookup
    existing_urls = {entry["url"] for entry in existing_data}

    # Counters for tracking updates
    new_entries_count = 0
    new_emails_count = 0

    # Add only new results (avoid duplicates)
    for result in new_results:
        if result["url"] not in existing_urls:
            # Add new website entry
            existing_data.append(result)
            new_entries_count += 1
        else:
            # Update existing entry with new emails
            for existing_entry in existing_data:
                if existing_entry["url"] == result["url"]:
                    # Find new emails that are not already in the existing entry
                    existing_emails = set(existing_entry.get("emails", []))
                    new_emails = set(result.get("emails", [])) - existing_emails
                    if new_emails:
                        existing_entry["emails"].extend(new_emails)
                        new_emails_count += len(new_emails)

    # Save the updated data back to the file
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, indent=4)

    # Print a summary of the updates
    print(f"Results saved to {filename}")
    print(f"New website entries added: {new_entries_count}")
    print(f"New emails added to existing websites: {new_emails_count}")
    print(f"Total websites in the file: {len(existing_data)}")

def saveToCsv(results):
    import csv
    # Save results to a CSV file
    with open("crawl_results.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(["URL", "Emails", "Error"])

        # Write each entry
        for entry in results:
            emails = ", ".join(entry["emails"])  # Join emails into a single string
            error = entry.get("error", "")  # Get the error if it exists
            writer.writerow([entry["url"], emails, error])

    print("Results saved to crawl_results.csv")

