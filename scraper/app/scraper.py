from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

def handle_multiple_search_results(driver: webdriver.Chrome):
    result = []
    multiple_search_result_table = driver.find_element(By.CSS_SELECTOR, "div#search-results table")
    rows = multiple_search_result_table.find_elements(By.XPATH, ".//tbody//tr")
    
    for index in range(0, len(rows)):
        row = rows[index]
        columns = row.find_elements(By.XPATH, ".//td")
        json_object = {
            "name": columns[0].text,
            "document_number": columns[1].text,
            "status": columns[2].text
        }
        result.append(json_object)
    return result

def handle_single_search_result(single_search_result: WebElement) -> list[dict]:
    result = []
    data_dict = {}
    data_dict.update(get_filing_information(single_search_result))
    data_dict.update(get_corporation_name(single_search_result))
    data_dict.update(get_detail_sections(single_search_result))
    result.append(data_dict)
    # print(result)
    return result

def get_filing_information(single_search_result: WebElement):
    filing_information = single_search_result.find_element(By.XPATH, ".//div[@class='detailSection filingInformation']")
    data_element = filing_information.find_element(By.CSS_SELECTOR, "span div")
    labels = data_element.find_elements(By.TAG_NAME, 'label')
    spans = data_element.find_elements(By.TAG_NAME, 'span')
    data_dict = {}
    for label, span in zip(labels, spans):
        data_dict[get_label(label.text)] = span.text
    return data_dict

def get_label(label_text):
    if label_text == "FEI/EIN Number":
        return "fei_number"
    return label_text.replace(" ", "_").replace("/", "_").lower()

def get_corporation_name(single_search_result: WebElement):
    corporation_name = single_search_result.find_element(By.XPATH, ".//div[@class='detailSection corporationName']")
    p_tags = corporation_name.find_elements(By.TAG_NAME, "p")
    data_dict = {}
    data_dict["name"] = p_tags[1].text
    return data_dict

def get_detail_sections(single_search_result: WebElement):
    detail_sections = single_search_result.find_elements(By.XPATH, ".//div[@class='detailSection']")
    data_dict = {}
    for section in detail_sections:
        span_tag = section.find_element(By.TAG_NAME, "span")
        data_dict.update(handle_sections(span_tag.text, section))
    return data_dict

def handle_sections(section_name: str, section: WebElement):
    data_dict = {}
    if(section_name == "Principal Address"):
        data_dict.update(handle_address_section(section))
    elif(section_name == "Mailing Address"):
        data_dict.update(handle_mailing_address_section(section))
    elif(section_name == "Registered Agent Name & Address"):
        data_dict.update(handle_registered_agent_section(section))
    elif(section_name == "Officer/Director Detail"):
        data_dict.update(handle_officer_director_detail_section(section))
    elif(section_name == "Document Images"):
        data_dict.update(handle_document_images_section(section))
    elif(section_name == "Annual Reports"):
        data_dict.update(handle_annual_reports_section(section))
    return data_dict

def handle_address_section(section: WebElement):
    span_tags = section.find_elements(By.TAG_NAME, "span")
    data_dict = {}
    if(len(span_tags) == 1):
        data_dict["principal_address"] = "None"
        return
    data_dict["principal_address"] = " ".join(span_tags[1].text.strip().split("\n"))
    return data_dict

def handle_mailing_address_section(section: WebElement):
    span_tags = section.find_elements(By.TAG_NAME, "span")
    data_dict = {}
    if(len(span_tags) == 1):
        data_dict["mailing_address"] = "None"
        return
    data_dict["mailing_address"] = " ".join(span_tags[1].text.strip().split("\n"))
    return data_dict

def handle_registered_agent_section(section: WebElement):
    data_dict = {}
    span_tags = section.find_elements(By.TAG_NAME, "span")
    if(len(span_tags) == 1):
        data_dict["registered_agent"] = "None"
        return
    # print(span_tags.text)
    data_dict["registered_agent"] = span_tags[1].text
    if(len(span_tags) > 2):
        data_dict["registered_agent_address"] = " ".join(span_tags[2].text.strip().split("\n"))
    else:
        data_dict["registered_agent_address"] = "None"
    return data_dict

def handle_officer_director_detail_section(section: WebElement):
    try:
        officer_sections = section.find_elements(By.XPATH, "//span[contains(text(), 'Title')]")
    except NoSuchElementException as e:
        print(f"Error: Officer sections not found. {e}")
    data_dict = {}
    officers = []
    for officer_section in officer_sections:
        try:
            title = officer_section.text.split()[-1]
            name = officer_section.find_element(By.XPATH, "preceding-sibling::br").text
            address_div = officer_section.find_element(By.XPATH, "following-sibling::span//div")
            address = " ".join(address_div.text.strip().split("\n"))
            
            officers.append({
                "title": title,
                "name": name,
                "address": address
            })
        except NoSuchElementException as e:
            print(f"Error: Officer section not found. {e}")
        except Exception as e:
            print(f"Unexpected error while processing officer: {e}")
    data_dict["officers"] = officers
    return data_dict

def handle_document_images_section(section: WebElement):   
    data_dict= {}
    document_images = []
    try:
        rows = section.find_elements(By.XPATH, ".//table//tr[td]")
        for row in rows:
            link_div = row.find_element(By.TAG_NAME, "td")
            link = link_div.find_element(By.TAG_NAME, "a").get_attribute("href")
            title = link_div.find_element(By.TAG_NAME, "a").text
            document_images.append({
                "link": link,
                "title": title
            })
    except NoSuchElementException as e:
        print(f"Error: Elements not found. {e}")
    except Exception as e:
        print(f"Unexpected error while processing document images: {e}")
    
    data_dict["document_images"] = document_images
    return data_dict

def handle_annual_reports_section(section: WebElement): 
    data_dict = {}
    reports = []
    try:
        rows = section.find_elements(By.XPATH, ".//table//tr[td]")
        rows.pop(0)
        for row in rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) == 2:
                year = columns[0].text.strip() 
                filed_date = columns[1].text.strip() 
                reports.append({
                    "report_year": year,
                    "filed_date": filed_date
                })
    except NoSuchElementException as e:
        print(f"Error: Elements not found. {e}")

    data_dict["annual_reports"] = reports
    return data_dict
