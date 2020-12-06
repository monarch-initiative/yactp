import argparse
import datetime
from SPARQLWrapper import SPARQLWrapper, JSON





parser = argparse.ArgumentParser(prog="meshSparql.py",
                                usage='%(prog)s -m <MeSH id>',
                                description='Download MeSH terms that descend from a given MeSH ID')

# Add the arguments
parser.add_argument('-m',
                    '--mesh',
                    type=str,
                    default='D009369',
                    help='MeSH ID (default, D009369=Neoplasms)')

# Execute the parse_args() method
args = parser.parse_args()

meshid = args.mesh


query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX meshv: <http://id.nlm.nih.gov/mesh/vocab#>
    PREFIX mesh: <http://id.nlm.nih.gov/mesh/>
    PREFIX mesh2015: <http://id.nlm.nih.gov/mesh/2015/>
    PREFIX mesh2016: <http://id.nlm.nih.gov/mesh/2016/>
    PREFIX mesh2017: <http://id.nlm.nih.gov/mesh/2017/>

    SELECT DISTINCT ?descriptor ?label
    FROM <http://id.nlm.nih.gov/mesh>

    WHERE {
        mesh:%s meshv:treeNumber ?treeNum .
        ?childTreeNum meshv:parentTreeNumber+ ?treeNum .
        ?descriptor meshv:treeNumber ?childTreeNum .
        ?descriptor rdfs:label ?label .
    }

ORDER BY ?label
""" % meshid



sparql = SPARQLWrapper("https://id.nlm.nih.gov/mesh/sparql")
sparql.setQuery(query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()



def extract_MeSH_id(mesh_uri):
    """
    mesh_uri is something like http://id.nlm.nih.gov/mesh/D008258
    return the id, e.g., D008258
    """
    if not mesh_uri.startswith("http://id.nlm.nih.gov/mesh/"):
        raise ValueError("Malformed MeSH URI: '%s'" % mesh_uri)
    mesh = mesh_uri[27:]
    print("GOT ", mesh)
    return mesh



now = datetime.date.today().strftime("%m_%d_%Y") 
outname = "mesh_%s_%s.tsv" % (meshid, now)

fh = open(outname, 'wt')
c = 0


for result in results["results"]["bindings"]:
    label = result["label"]["value"]
    mesh_id = extract_MeSH_id(result['descriptor']['value'])
    fh.write("%s\t%s\n" % (mesh_id, label))
    c += 1
fh.close()
print("[INFO] We got %d MeSH entries that descend from Neoplasm" % c)