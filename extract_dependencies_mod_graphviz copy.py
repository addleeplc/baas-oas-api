import json
import networkx as nx
from pyvis.network import Network

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def extract_and_modify_dependencies(services, target_services):
    modified_dependencies = {}
    for service in services:
        service_name = service['name']
        if service_name in target_services:
            dependencies = []
            for version in service.get('versions', []):
                for dependency in version.get('dependencies', []):
                    dependency_name = dependency['name']
                    dependencies.append(dependency_name)
            modified_dependencies[service_name] = sorted(set(dependencies))
    return modified_dependencies

def generate_dag(dependencies):
    G = nx.DiGraph()
    for service, deps in dependencies.items():
        for dep in deps:
            G.add_edge(service, dep)
    return G

def visualize_dag(G, output_file):
    net = Network(height='750px', width='100%', bgcolor='#222222', font_color='white')
    net.from_nx(G)
    net.show_buttons(filter_=['physics'])
    net.show(output_file)

def main():
    # Load the target services
    target_services_data = load_json('al_baas-services.json')
    target_services = target_services_data.get('services', [])

    # Load the services inventory
    services_inventory = load_json('al_shamrock-service-inventory.json')
    services = services_inventory.get('services', [])

    # Extract and modify dependencies
    modified_dependencies = extract_and_modify_dependencies(services, target_services)

    # Save the final modified dependencies array to a new JSON file
    save_json(modified_dependencies, 'al_baas-modified-dependencies.json')

    # Generate and visualize the DAG
    dag = generate_dag(modified_dependencies)
    visualize_dag(dag, 'service_dependencies.html')

if __name__ == '__main__':
    main()