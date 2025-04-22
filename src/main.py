from .utils import logging, search_websites, load_csv_to_dataframe
from .config import OUTPUT_DIR
import os
import pandas as pd

def main():
    keywords = load_csv_to_dataframe("src/packages.csv")
    results = []

    for _, item in keywords.iterrows():
        logging.debug(item["CVE-ID"])
        search_query = [f"{item['Package']} {item['Snapshot']} documentation"]
        websites = search_websites(search_query)
        logging.debug(len(websites))
        websites = list(set(websites))
        results.append({
            "CVE-ID": item["CVE-ID"],
            "Package": item["Package"],
            "Snapshot": item["Snapshot"],
            "Websites": websites
        })

    # Convert results to a DataFrame
    results_df = pd.DataFrame(results)

    # Write to CSV
    output_path = os.path.join(OUTPUT_DIR, "packages-documents.csv")
    results_df.to_csv(output_path, index=False)
    logging.info(f"Results written to {output_path}")

if __name__ == "__main__":
    main()