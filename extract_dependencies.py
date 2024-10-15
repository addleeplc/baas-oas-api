import json

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def extract_dependencies(services):
    dependencies = []
    for service in services:
        for version in service.get('versions', []):
            for dependency in version.get('dependencies', []):
                dependencies.append(dependency['name'])
    return dependencies

def main():
    # Load the services inventory
    services_inventory = load_json('al_shamrock-service-inventory.json')
    services = services_inventory.get('services', [])

    # Extract dependencies
    baas_dependencies = extract_dependencies(services)

    # Sort and remove duplicates
    baas_dependencies = sorted(set(baas_dependencies))

    # Save the final dependencies array to a new JSON file
    save_json({'baas-dependencies': baas_dependencies}, 'al_baas-dependencies.json')

if __name__ == '__main__':
    main()