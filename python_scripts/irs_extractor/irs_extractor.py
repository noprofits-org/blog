#!/usr/bin/env python3
"""
Script to download IRS Form 990 XML filings for specified EINs from the IRS AWS S3 repository.

This script scrapes the IRS download page for index files, streams them to filter for the given EINs,
and downloads the corresponding XML filings, saving them locally.
"""

import requests
import pandas as pd
import time
import logging
import csv
import zipfile
import io
from io import StringIO
from pathlib import Path
from typing import List, Optional, Dict
from bs4 import BeautifulSoup

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("irs_download.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Constants
BASE_URL = "https://apps.irs.gov/pub/epostcard/990"  # Updated base URL for XML files
DOWNLOAD_PAGE = "https://www.irs.gov/charities-non-profits/form-990-series-downloads"
EINS = ["13-6213516", "53-0196605", "13-1635294", "13-1644147", "53-0242652"]
EINS_SET = {int(ein.replace("-", "")) for ein in EINS}  # Convert to integers for matching
YEARS = range(2023, 2026)  # Adjust years as needed (e.g., 2023-2025)
DOWNLOAD_DIR = Path("filings")
RATE_LIMIT = 0.5  # Seconds between requests to avoid throttling

def setup_directories():
    """Create directories for storing downloaded filings."""
    DOWNLOAD_DIR.mkdir(exist_ok=True)
    for ein in EINS:
        (DOWNLOAD_DIR / ein).mkdir(exist_ok=True)

def download_file(url: str, dest_path: Path) -> bool:
    """Download a file from a URL and save it to the destination path."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        logger.info(f"Successfully downloaded {url} to {dest_path}")
        return True
    except requests.RequestException as e:
        logger.error(f"Failed to download {url}: {e}")
        return False

def get_index_urls(year: int) -> List[str]:
    """
    Scrape the IRS download page to find all index file URLs for a given year.
    Returns a list of URLs for the index files (CSVs and ZIPs).
    """
    try:
        response = requests.get(DOWNLOAD_PAGE)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find all links on the page that match the pattern for index files
        index_urls = []
        for link in soup.find_all("a", href=True):
            href = link["href"]
            # Look for URLs that contain the year and end with .csv or .zip
            if str(year) in href and (href.endswith(".csv") or href.endswith(".zip")):
                # Ensure the URL is absolute
                if not href.startswith("http"):
                    href = f"https://www.irs.gov{href}" if href.startswith("/") else f"https://www.irs.gov/{href}"
                index_urls.append(href)
        
        if not index_urls:
            logger.warning(f"No index files found for year {year}")
        else:
            logger.info(f"Found {len(index_urls)} index files for year {year}: {index_urls}")
        return index_urls
    except requests.RequestException as e:
        logger.error(f"Failed to scrape index URLs for year {year}: {e}")
        return []

def list_zip_contents(zip_path: Path) -> List[str]:
    """List the contents of a ZIP file and return the list of file names."""
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            contents = zip_ref.namelist()
            logger.info(f"Contents of ZIP {zip_path}: {contents}")
            return contents
    except Exception as e:
        logger.error(f"Failed to list contents of ZIP {zip_path}: {e}")
        return []

def extract_csv_from_zip(zip_path: Path) -> Optional[StringIO]:
    """
    Extract the CSV file from a ZIP archive and return its contents as a StringIO object.
    Looks for any CSV file in the ZIP.
    """
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            # Find any CSV file in the ZIP
            csv_file = [f for f in zip_ref.namelist() if f.endswith(".csv")]
            if not csv_file:
                logger.error(f"No CSV file found in ZIP: {zip_path}")
                return None
            if len(csv_file) > 1:
                logger.warning(f"Multiple CSV files found in ZIP: {zip_path}, using the first one: {csv_file[0]}")
            
            # Extract the CSV content
            with zip_ref.open(csv_file[0]) as f:
                content = f.read().decode("utf-8")
                return StringIO(content)
    except Exception as e:
        logger.error(f"Failed to extract CSV from ZIP {zip_path}: {e}")
        return None

def stream_index(url: str, year: int, batch_id: str) -> List[Dict]:
    """
    Stream the index CSV file from the given URL and filter for the target EINs.
    Handles both direct CSVs and ZIP files containing CSVs.
    Returns a list of dictionaries containing the relevant rows.
    """
    relevant_rows = []
    temp_path = DOWNLOAD_DIR / f"index_{year}_{batch_id}.tmp"
    
    # Download the file
    if not download_file(url, temp_path):
        return []
    
    try:
        # Check if the file is a ZIP
        if url.endswith(".zip"):
            # List the contents of the ZIP file for debugging
            list_zip_contents(temp_path)
            
            csv_stream = extract_csv_from_zip(temp_path)
            if csv_stream is None:
                return []
        else:
            # Assume it's a CSV
            with open(temp_path, "r", encoding="utf-8") as f:
                csv_stream = StringIO(f.read())
        
        # Parse the CSV
        csv_stream.seek(0)
        reader = csv.DictReader(csv_stream)
        
        # Check if the index file contains a URL column
        fieldnames = reader.fieldnames
        logger.info(f"Index file columns: {fieldnames}")
        url_column = None
        for col in fieldnames:
            if col.lower() in ["url", "file_location", "xml_url"]:
                url_column = col
                logger.info(f"Found URL column: {url_column}")
                break
        
        for row in reader:
            try:
                ein = int(row["EIN"])
                if ein in EINS_SET:
                    # If there's a URL column, add it to the row
                    if url_column:
                        row["XML_URL"] = row[url_column]
                    relevant_rows.append(row)
                    logger.info(f"Found filing for EIN {ein} in year {year}, batch {batch_id}")
            except (KeyError, ValueError) as e:
                logger.warning(f"Skipping row due to error: {e}")
                continue
        
        logger.info(f"Found {len(relevant_rows)} relevant filings in year {year}, batch {batch_id}")
        return relevant_rows
    except Exception as e:
        logger.error(f"Failed to process index file from {url}: {e}")
        return []
    finally:
        # Clean up the temporary file
        temp_path.unlink(missing_ok=True)
        # Only close csv_stream if it exists
        if "csv_stream" in locals() and csv_stream is not None:
            csv_stream.close()

def download_filings_for_ein(ein: str, filings: List[Dict], year: int, batch_id: str):
    """Download all XML filings for a given EIN in a specific year and batch."""
    for filing in filings:
        try:
            object_id = filing["OBJECT_ID"]
            
            # Check if the filing has a specific XML URL
            if "XML_URL" in filing:
                xml_url = filing["XML_URL"]
            else:
                # Fallback to constructing the URL
                xml_url = f"{BASE_URL}/{year}/{object_id}_public.xml"
            
            dest_path = DOWNLOAD_DIR / ein / f"{year}_{object_id}.xml"
            
            if dest_path.exists():
                logger.info(f"XML for EIN {ein}, year {year}, object_id {object_id} already exists, skipping")
                continue
            
            logger.info(f"Downloading XML for EIN {ein}, year {year}, object_id {object_id} from {xml_url}")
            time.sleep(RATE_LIMIT)  # Respect rate limit
            download_file(xml_url, dest_path)
        except KeyError as e:
            logger.error(f"Missing OBJECT_ID in filing: {e}")
            continue

def main():
    """Main function to download IRS Form 990 filings for specified EINs."""
    logger.info("Starting IRS Form 990 data download")
    
    # Setup directories
    setup_directories()
    
    # Process each year
    for year in YEARS:
        logger.info(f"Processing year {year}")
        
        # Get all index file URLs for the year
        index_urls = get_index_urls(year)
        if not index_urls:
            logger.warning(f"Skipping year {year} due to no index files found")
            continue
        
        # Process each index file
        for idx, url in enumerate(index_urls):
            batch_id = f"batch_{idx+1:03d}"  # e.g., batch_001, batch_002
            logger.info(f"Processing batch {batch_id} for year {year} from {url}")
            
            # Stream the index file and filter for target EINs
            relevant_filings = stream_index(url, year, batch_id)
            if not relevant_filings:
                logger.warning(f"No relevant filings found in batch {batch_id} for year {year}")
                continue
            
            # Group filings by EIN
            filings_by_ein = {}
            for filing in relevant_filings:
                ein = filing["EIN"]
                if ein not in filings_by_ein:
                    filings_by_ein[ein] = []
                filings_by_ein[ein].append(filing)
            
            # Download filings for each EIN
            for ein in EINS:
                ein_int = str(int(ein.replace("-", "")))
                if ein_int in filings_by_ein:
                    download_filings_for_ein(ein, filings_by_ein[ein_int], year, batch_id)
    
    logger.info("Download complete. Check the 'filings' directory for XML files.")

if __name__ == "__main__":
    main()