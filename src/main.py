from .utils import logging, search_websites, load_jsonl_to_list, dump_list_to_jsonl, list_to_dataframe
from .config import OUTPUT_DIR
import os, json

def main():
    keywords = load_jsonl_to_list("src/keywords.jsonl")
    logging.debug(json.dumps(keywords[0], indent=4))

    for item in keywords:
        logging.debug(item["CWE_ID"])
        websites = search_websites(item["Keywords"])
        logging.debug(len(websites))
        websites = list(set(websites))
        logging.debug(len(websites))
        item["websites"] = websites

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = f"{OUTPUT_DIR}/websites.jsonl"
    dump_list_to_jsonl(keywords, output_file)
    logging.info(f"Websites have been written to {output_file}")

    for item in keywords:
        item.pop("Keywords", None)

    dataframe = list_to_dataframe(keywords)
    dataframe.to_csv(f"{OUTPUT_DIR}/websites.csv", index=False)
    logging.info(f"Dataframe has been saved to {OUTPUT_DIR}/websites.csv")

if __name__ == "__main__":
    main()