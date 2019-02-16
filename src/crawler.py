import requests
import json
import time

def main():
    """ Retrieves and parses information from Global Giving's API
        and writes it to a json file """
    # Specifying API to return JSON
    headers = {"Accept": "application/json"}

    # JSON files to write to
    projects_json = open("projects.json", "w")

    # Initial setup
    next_project_id = 2
    has_next = True
    projects = []
    error_count = 0

    while has_next:
        # Requesting projects from Global Giving API
        try:
            r = requests.get(
                "https://api.globalgiving.org/api/public/projectservice/all/projects/"
                + "?api_key=72ef6e29-cb2b-4613-9cc6-69a88a8d3f3b&next_project_id="
                + str(next_project_id),
                headers=headers,
            )

            projects = r.json()["projects"]
        
        except:
            error_count += 1
            if error_count >= 3:
                next_project_id += 1
                error_count = 0
            continue

        # Grabbing next projects
        has_next = projects["hasNext"]
        if has_next:
            next_project_id = projects["nextProjectId"]

        # Recording projects
        projects += [
            parse_project_info(project) for project in projects["project"]
        ]

        time.sleep(0.5)

    # Writing projects to JSON file
    json.dump(
        {"projects": projects},
        projects_json,
        sort_keys=True,
        indent=2,
        ensure_ascii=False,
    )


def get_project_key(project, keys):
    """ Helper method to find project properties
    Finds properties in given keys, if not, returns ''

    Args: 
        project: projects json returned by Global Giving's API
        keys: keys to iterate through project to find desired value

    Return:
        Object found in project key(s)
    """
    try:
        result = project
        for key in keys:
            result = results.get(key)
        return result
    except:
        return ""


def parse_project_info(project):
    """ Helper method to parse projects and filter relevant data 

    Args:
        project: projects json returned by Global Giving's API

    Return: 
        Dictionary of filtered parameters from project json
    """
    name = get_project_key(project, ["organization", "name"])
    url = get_project_key(project, ["organization", "url"])
    main_theme = get_project_key(project, ["themeName"])
    sub_themes = get_project_key(project, ["organization", "themes", "theme"])
    country = get_project_key(project, ["country"])
    
    return {"name": name, "url": url, "mainTheme": main_theme, "subThemes": sub_themes, "country": country}

if __name__ == "__main__":
    main()
