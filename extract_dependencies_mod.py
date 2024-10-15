# import json
# import networkx as nx
# from pyvis.network import Network

# def load_json(file_path):
#     with open(file_path, 'r') as file:
#         return json.load(file)

# def save_json(data, file_path):
#     with open(file_path, 'w') as file:
#         json.dump(data, file, indent=4)

# def extract_and_modify_dependencies(services, public_services):
#     modified_dependencies = {}
#     for service in services:
#         service_name = service['name']
#         if service_name in public_services:
#             dependencies = []
#             for version in service.get('versions', []):
#                 for dependency in version.get('dependencies', []):
#                     dependency_name = dependency['name']
#                     dependencies.append(dependency_name)
#             modified_dependencies[service_name] = sorted(set(dependencies))
#     return modified_dependencies

# def generate_dag(dependencies):
#     G = nx.DiGraph()
#     for service, deps in dependencies.items():
#         for dep in deps:
#             G.add_edge(service, dep)
#     return G

# def visualize_dag(G, output_file):
#     net = Network(height='1080px', width='100%', bgcolor='#222222', font_color='white')
#     net.from_nx(G)
#     # Customize nodes and edges
#     for node in net.nodes:
#         node['color'] = 'lightblue' if 'service' in node['id'] else 'orange'
#         node['size'] = 20 if 'service' in node['id'] else 10
    
#     for edge in net.edges:
#         edge['color'] = 'gray'
#         edge['arrows'] = 'orange'
#     net.show_buttons(filter_=['physics'])
#     # net.show(output_file)
    
#     # Write the HTML content to a file
#     html_content = net.generate_html()
#     with open(output_file, 'w') as f:
#         f.write(html_content)

# def main():
#     # Load the target services
#     public_services_data = load_json('al_baas-services.json')
#     public_services = public_services_data.get('services', [])

#     # Load the services inventory
#     services_inventory = load_json('al_shamrock-service-inventory.json')
#     services = services_inventory.get('services', [])

#     # Extract and modify dependencies
#     modified_dependencies = extract_and_modify_dependencies(services, public_services)

#     # Save the final modified dependencies array to a new JSON file
#     save_json(modified_dependencies, 'al_baas-modified-dependencies.json')

#     # Generate and visualize the DAG
#     dag = generate_dag(modified_dependencies)
#     visualize_dag(dag, 'service_dependencies.html')

# if __name__ == '__main__':
#     main()

# revision 

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

def visualize_dag(G, target_services, output_file):
    net = Network(height='1200px', width='100%', bgcolor='#222222', font_color='white')
    net.from_nx(G)
    
    # Set default physics options
    physics_options = {
        "physics": {
            "enabled": True,
            "forceAtlas2Based": {
                "theta": 0.1,
                "gravitationalConstant": -272,
                "centralGravity": 0.05,
                "springLength": 80,
                "springConstant": 0.34,
                "damping": 0.19,
                "avoidOverlap": 1
            },
            "minVelocity": 0.75,
            "solver": "forceAtlas2Based",
            "timestep": 0.32
        },
        "configure": {
            "enabled": True,
            "filter": "physics",
            "collapsed": True
        }
    }
    net.set_options(json.dumps(physics_options))
    
    # Customize nodes and edges
    for node in net.nodes:
        if node['id'] in target_services:
            node['color'] = 'lightblue'
            node['size'] = 20
            node['font']['color'] = 'white'
        else:
            node['color'] = 'orange'
            node['size'] = 10
            node['font']['color'] = 'lightblue'
    
    for edge in net.edges:
        if edge['from'] in target_services and edge['to'] in target_services:
            edge['color'] = 'lightblue'
            edge['width'] = 3
        else:
            edge['color'] = 'gray'
    
    # Write the HTML content to a file
    html_content = net.generate_html()
    with open(output_file, 'w') as f:
        f.write(html_content)

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
    visualize_dag(dag, target_services, 'service_dependencies.html')

if __name__ == '__main__':
    main()