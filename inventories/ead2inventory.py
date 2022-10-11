import json

import rdflib
from rdflib import Graph, URIRef, Literal, RDF, SDO
from rdflib.resource import Resource

from typing import Union


def main(infile: str, outfile: str, brediusdata: str):
    """
    Convert a json with EAD data into an RDF file in `schema.org`.
    
    This is done recursively until the last level. If persons are 
    mentioned in the file, then they are added as `schema:Person` 
    instances with a `schema:about`/`schema:subjectOf` relation to 
    the `schema:ArchiveComponent`. 


    Example:
    ```turtle

    <https://rkd.nl/explore/archives/file/110432054> a schema:ArchiveComponent ;
        schema:about <https://rkd.nl/explore/artists/33498>,
            <https://rkd.nl/explore/artists/33499>,
            <https://rkd.nl/explore/artists/33500>,
            <https://rkd.nl/explore/artists/33501>,
            <https://rkd.nl/explore/artists/495214> ;
        schema:hasPart <https://data.rkd.nl/excerpts/780007>,
            <https://data.rkd.nl/excerpts/780008>,
            ...
        schema:identifier "0380.220" ;
        schema:isPartOf <https://rkd.nl/explore/archives/file/110432027> ;
        schema:name "Grebber, De (familie)"@nl .
    ```

    Args:
        infile (str): The input file path in csv.
        outfile (str): the output file path in trig.
    """

    with open(infile) as f:
        data = json.load(f)

    g = Graph(identifier="https://data.goldenagents.org/datasets/bredius/")

    brediuscollection = Resource(g, URIRef("https://data.rkd.nl/collections/380"))
    brediuscollection.add(RDF.type, SDO.ArchiveComponent)
    brediuscollection.add(RDF.type, SDO.Collection)
    brediuscollection.add(SDO.name, Literal("Archief Abraham Bredius", lang="nl"))
    brediuscollection.add(SDO.temporalCoverage, Literal("1616/1940"))
    brediuscollection.add(SDO.size, Literal("7.5M"))
    brediuscollection.add(SDO.holdingArchive, URIRef("https://rkd.nl/"))
    brediuscollection.add(SDO.creator, URIRef("https://rkd.nl/explore/artists/338895"))
    brediuscollection.add(SDO.identifier, Literal("NL-HaRKD.0380"))
    brediuscollection.add(
        SDO.url, URIRef("https://rkd.nl/explore/archives/details/NL-HaRKD-0380")
    )

    org = Resource(g, URIRef("https://rkd.nl/"))
    org.add(RDF.type, SDO.Organization)
    org.add(
        SDO.name,
        Literal("RKD – Nederlands Instituut voor Kunstgeschiedenis", lang="nl"),
    )
    org.add(SDO.name, Literal("RKD – Netherlands Institute for Art History", lang="en"))

    pers = Resource(g, URIRef("https://rkd.nl/explore/artists/338895"))
    pers.add(RDF.type, SDO.Person)
    pers.add(
        SDO.name, Literal("Abraham Bredius"),
    )

    for d in data["Collection"]:

        r, g = getResource(d, g)

        brediuscollection.add(SDO.hasPart, r.identifier)
        r.add(SDO.isPartOf, brediuscollection.identifier)

    g = getExcerpts(brediusdata, g)

    g.bind("schema", SDO)
    g.serialize(outfile, format="trig")


def getResource(
    d: dict, g: rdflib.Graph
) -> Union[rdflib.resource.Resource, rdflib.Graph]:
    """
    Parse an individual object from the JSON EAD.

    Args:
        d (dict): The JSON EAD data.
        g (rdflib.Graph): The graph.

    Returns:
        (rdflib.resource.Resource, rdflib.Graph): An RDFLib Resource object and the graph object.
    """

    r = Resource(g, URIRef(d["URI"]))
    r.add(RDF.type, SDO.ArchiveComponent)
    r.add(SDO.name, Literal(d["Titel"], lang="nl"))
    r.add(SDO.identifier, Literal(d["Inventarisnummer"]))

    if "Onderdelen" in d:
        for onderdeel in d["Onderdelen"]:
            o, g = getResource(onderdeel, g)

            r.add(SDO.hasPart, o.identifier)
            o.add(SDO.isPartOf, r.identifier)

    if "Personen" in d:
        for persoon in d["Personen"]:
            pURI = persoon["URI"].replace(
                "https://rkd.nl/explore/thesaurus/people/",
                "https://rkd.nl/explore/artists/",
            )
            p = Resource(g, URIRef(pURI))  # Klopt dit?
            p.add(RDF.type, SDO.Person)
            p.add(SDO.name, Literal(persoon["Naam"]))

            r.add(SDO.about, p.identifier)
            p.add(SDO.subjectOf, r.identifier)

    return r, g


def getExcerpts(brediusdata: str, g: rdflib.Graph) -> rdflib.Graph:
    """
    Connect the excerpts to the inventorynumber they came from using a 
    `schema:isPartOf` and `schema:hasPart` relation. This is done by 
    loading in the original data and a SELECT query. 

    Args:
        brediusdata (str): BrediusData object
        g (rdflib.Graph): Graph object
    
    Returns:
        rdflib.Graph: The graph object
    """

    cg = Graph(identifier="https://data.goldenagents.org/datasets/bredius/")
    cg.parse(brediusdata)
    cg += g

    q = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX schema: <https://schema.org/>

    SELECT * WHERE {

        ?excerpt a schema:Manuscript ;
            schema:identifier ?identifier .
    
        FILTER(CONTAINS(?identifier, '_'))
        BIND(STRBEFORE(?identifier, '_') AS ?inventorynumber)

        ?inventory schema:identifier ?inventorynumber .

    }
    """

    results = cg.query(q)

    for r in results:

        g.add((r.excerpt, SDO.isPartOf, r.inventory))
        g.add((r.inventory, SDO.hasPart, r.excerpt))

    return g


if __name__ == "__main__":

    INFILE = "NL-HaRKD-0380.ead.json"
    OUTFILE = "linkset_excerpt_inventories.trig"

    BREDIUSDATA = "../data/ga_20220926_BrediusExportVolledig.trig"

    main(INFILE, OUTFILE, BREDIUSDATA)

