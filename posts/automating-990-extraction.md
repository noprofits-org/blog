---
title: DRAFT - Automating IRS Form 990 Data Extraction - A Programmatic Approach to Nonprofit Data Analysis 
date: 2025-04-03
tags: nonprofit transparency, IRS Form 990, data extraction, computational methods, API development
description: A programmatic approach to automating the extraction and analysis of IRS Form 990 data for targeted nonprofit organizations using advanced computational techniques and API development.
draft: true
---

## Introduction

The Internal Revenue Service (IRS) Form 990 provides a wealth of information about tax-exempt organizations in the United States. However, accessing and analyzing this data has historically been challenging due to the complexities of the IRS data repository structure.[@williams2023; @ottinger2022] Building upon previous work towards mapping the structure of the IRS Form 990 data repository, the current aim is to further advance programmatic methods to efficiently probe and analyze specific organizations within the Form 990 dataset.[Anthropic2025Claude]

The availability of Form 990 data in electronic format has increased significantly since the introduction of e-filing requirements for tax-exempt organizations.[@blackwood2013] Despite this progress, challenges persist in terms of data accessibility, quality, and usability for research purposes.[@noveck2013] Existing approaches to Form 990 data analysis often rely on manual extraction methods or limited subsets of the available data, hindering the ability to conduct comprehensive, longitudinal studies of the nonprofit sector.[@borenstein2018]

To address these limitations, we propose a programmatic approach to automate the extraction and analysis of Form 990 data for targeted organizations. By leveraging advanced computational techniques and focusing on specific Employer Identification Numbers (EINs) of interest, this study aims to demonstrate the feasibility and benefits of a more efficient, scalable, and reproducible method for nonprofit data discovery.

## Experimental

```python
import boto3
import logging
import xml.etree.ElementTree as ET
from typing import List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

S3_BUCKET = "irs-form-990"
TARGET_EINS = [
    "13-6213516",  # American Civil Liberties Union Foundation
    "53-0196605",  # American National Red Cross
    "13-1635294",  # United Way Worldwide
    "13-1644147",  # Planned Parenthood Federation of America
    "53-0242652",  # Nature Conservancy
]

def get_form990_filings(ein: str, start_year: int, end_year: int) -> List[str]:
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(S3_BUCKET)
    
    filings = []
    
    for year in range(start_year, end_year + 1):
        prefix = f"{year}/{ein}"
        objects = bucket.objects.filter(Prefix=prefix)
        
        for obj in objects:
            if obj.key.endswith(".xml"):
                filings.append(obj.key)
    
    return filings

def parse_form990_xml(xml_content: str) -> dict:
    root = ET.fromstring(xml_content)
    
    data = {
        "ein": root.find("EIN").text,
        "organization_name": root.find("BusinessName/BusinessNameLine1").text,
        "tax_year": root.find("TaxYear").text,
        "total_revenue": root.find("TotalRevenueAmt").text,
        "total_expenses": root.find("TotalExpensesAmt").text,
        "net_assets": root.find("NetAssetsOrFundBalancesEOYAmt").text,
    }
    
    return data

def main():
    for ein in TARGET_EINS:
        logger.info(f"Retrieving Form 990 filings for EIN: {ein}")
        
        filings = get_form990_filings(ein, 2019, 2025)
        
        for filing in filings:
            logger.info(f"Parsing Form 990 XML: {filing}")
            
            obj = s3.Object(S3_BUCKET, filing)
            xml_content = obj.get()["Body"].read().decode("utf-8")
            
            data = parse_form990_xml(xml_content)
            logger.info(f"Extracted data: {data}")

if __name__ == "__main__":
    main()
```

The experimental process involves the following steps:

1. Import necessary Python libraries: `boto3` for interacting with AWS S3, `logging` for logging, `xml.etree.ElementTree` for parsing XML, and `typing` for type hinting.

2. Configure logging to output log messages to the console with the `INFO` level.

3. Define constants for the S3 bucket name (`S3_BUCKET`) and the list of target EINs (`TARGET_EINS`).

4. Implement the `get_form990_filings` function to retrieve Form 990 XML filings for a given EIN within a specified year range from the S3 bucket. The function returns a list of S3 object keys representing the XML filings.

5. Implement the `parse_form990_xml` function to parse the XML content of a Form 990 filing and extract relevant data fields such as EIN, organization name, tax year, total revenue, total expenses, and net assets. The function returns a dictionary containing the extracted data.

6. In the `main` function, iterate over the target EINs and perform the following steps for each EIN:
   - Retrieve Form 990 filings for the EIN within the specified year range using the `get_form990_filings` function.
   - For each retrieved filing, read the XML content from the S3 object.
   - Parse the XML content using the `parse_form990_xml` function to extract relevant data.
   - Log the extracted data for each filing.

7. Run the `main` function when the script is executed.

Note: The provided code assumes the necessary AWS credentials are configured in the environment where the script is run, allowing access to the S3 bucket.