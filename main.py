"""
Golden Agents RKD Bredius excerpts pipeline.

l.vanwissen@uva.nl
"""
import time
import requests
from json.decoder import JSONDecodeError
from isodate import parse_date

import rdflib
from rdflib import RDF, Namespace, BNode, URIRef, Literal

SCHEMA = Namespace("https://schema.org/")


def main(filepath: str, destination: str, thesaurusfile: str = "") -> None:

    # Load the file from the RKD, and load the thesaurus (in SKOS) separately
    print("1/7 Loading the file(s) into a memory store graph")
    g = loadRDF(filepath, thesaurusfile)

    # Remove all the wrong labels from the thesaurus entries
    print("2/7 Removing all the thesaurus labels")
    g = removeLabels(g)

    # Add a URL of the RKD website to the resources
    print("3/7 Adding the URL to the public permalink")
    g = addURL(g)

    # Correct the roles to schema.Role objects
    print("4/7 Correcting the schema:additionalType statements")
    g = correctRoles(g)

    # Add depictions to experpts from RKD API
    print("5/7 Adding a URI of a thumbnail")
    g = addImages(g)

    # Find incorrect dates
    print("6/7 Get a list of incorrectly formatted dates and remove these")
    g = fixDates(g)

    # Save the enriched/corrected file
    print("7/7 Saving the graph to a file")
    g.serialize(destination, format="turtle")


def loadRDF(filepath: str, thesauruspath: str = "") -> rdflib.ConjunctiveGraph:
    """
    Load in the RDF file (in RDF/XML) and return a graph object.

    Args:
        filepath: The path to the RDF file.
        thesauruspath: The path to the RDF thesaurus file.

    Returns:
        A graph object.
    """

    g = rdflib.ConjunctiveGraph()

    g.parse(filepath)

    if thesauruspath:
        g.parse(thesauruspath)

    return g


def removeLabels(g: rdflib.ConjunctiveGraph) -> rdflib.ConjunctiveGraph:
    """
    Due to a quirk in Adlib and the export and conversion script
    the thesaurus references have gotten multiple schema:name entries.
    A URI such as <https://data.rkd.nl/thesaurus/6> not only has the
    name "painter", but also has 100+ other names that are incorrect.
    In this function we remove these labels, since we have converted the RKD thesaurus separately. The name of the role of the

    Args:
        g: The graph object.

    Returns:
        The graph object without thesaurus labels.
    """

    q = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX schema: <https://schema.org/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

    SELECT DISTINCT * WHERE { 
        ?thesaurus schema:name ?label .
        
        FILTER(CONTAINS(STR(?thesaurus), 'thesaurus'))

        OPTIONAL {
            ?thesaurus skos:prefLabel ?labelEN .
                FILTER(LANG(?labelEN) = 'en')
        }

        OPTIONAL {
            ?thesaurus skos:prefLabel ?labelNL .
                FILTER(LANG(?labelNL) = 'nl')
        }
            
    }
    """

    results = g.query(q)

    for r in results:

        # Remove all the wrong ones
        g.remove((r.thesaurus, SCHEMA.name, r.label))

        # Add back the right ones to stick to the schema vocabulary
        if r.labelEN:
            g.add((r.thesaurus, SCHEMA.name, Literal(r.labelEN, lang="en")))

        if r.labelNL:
            g.add((r.thesaurus, SCHEMA.name, Literal(r.labelNL, lang="nl")))

    return g


def addURL(g: rdflib.ConjunctiveGraph) -> rdflib.ConjunctiveGraph:
    """
    Add a URL to the public permalink of the RKD website to each manuscript resource.

    Args:
        g: The graph object.

    Returns:
        The graph object with the URL added.
    """

    manuscripts = g.subjects(RDF.type, SCHEMA.Manuscript)

    for m in manuscripts:
        url = str(m).replace("data.rkd.nl", "rkd.nl/explore")

        g.add((m, SCHEMA.url, URIRef(url)))

    return g


def correctRoles(g: rdflib.ConjunctiveGraph) -> rdflib.ConjunctiveGraph:
    """
    Transform the schema:additionalType statements for each schema:Person to
    a schema:Role object. For consistency, also do this when there is no
    additionalType on the Person.

    Sometimes the schema:Person resources are described with a
    schema:additionalType to indicate their role in the excerpt. This function
    transforms this to a schema:Role object, so that the context of this statement
    is preserved when entities are e.g. disambiguated and when owl:sameAs reasoning
    is enabled.

    Informative labels in EN and NL are added to the schema:Role object,
    combining the person's name and their role.

    Args:
        g: The graph object.

    Returns:
        The graph object with corrected roles.
    """

    q = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX schema: <https://schema.org/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

    SELECT * WHERE {
        ?manuscript a schema:Manuscript ;
            schema:about ?person .

        ?person a schema:Person ;
            schema:name ?personName .

        OPTIONAL {
            ?person schema:additionalType ?additionalType .

            OPTIONAL {
                ?additionalType skos:prefLabel ?labelEN .
                FILTER(LANG(?labelEN) = 'en')
            }

            OPTIONAL {
                ?additionalType skos:prefLabel ?labelNL .
                FILTER(LANG(?labelNL) = 'nl')
            }
        }
    }
    """

    results = g.query(q)

    for r in results:

        print(r.additionalType)

        g.remove((r.manuscript, SCHEMA.about, r.person))

        roleBnode = BNode()
        g.add((roleBnode, RDF.type, SCHEMA.Role))
        g.add((roleBnode, SCHEMA.about, r.person))

        g.add((r.manuscript, SCHEMA.about, roleBnode))

        if r.additionalType:
            g.remove((r.person, SCHEMA.additionalType, r.additionalType))
            g.add((roleBnode, SCHEMA.roleName, r.additionalType))

            if r.labelEN:
                g.add(
                    (
                        roleBnode,
                        SCHEMA.name,
                        Literal(f"{r.personName} ({r.labelEN})", lang="en"),
                    )
                )
            if r.labelNL:
                g.add(
                    (
                        roleBnode,
                        SCHEMA.name,
                        Literal(f"{r.personName} ({r.labelNL})", lang="nl"),
                    )
                )
        else:
            g.add(
                (
                    roleBnode,
                    SCHEMA.name,
                    Literal(f"{r.personName} (Unknown)", lang="en"),
                )
            )
            g.add(
                (
                    roleBnode,
                    SCHEMA.name,
                    Literal(f"{r.personName} (Onbekend)", lang="nl"),
                )
            )

    return g


def addImages(g: rdflib.ConjunctiveGraph) -> rdflib.ConjunctiveGraph:
    """
    Add a URI of a thumbnail as depiction to each manuscript resource. Uses the
    RKD API to fetch the uuid of the image. Images are modelled in a schema:image
    statement.

    Args:
        g: The graph object.

    Returns:
        The graph object with images added to the manuscript resources.
    """

    manuscripts = g.subjects(RDF.type, SCHEMA.Manuscript)

    for m in manuscripts:
        piref = str(m).rsplit("/", 1)[-1]

        data = getAPI(identifier=piref)
        if not data:
            continue
        elif 'response' not in data:
            continue
        uuids = data["response"]["docs"][0]["picturae_images"]

        for uuid in uuids:
            image = URIRef(f"https://images.rkd.nl/rkd/thumb/650x650/{uuid}.jpg")
            g.add((m, SCHEMA.image, image))

    return g


def getAPI(identifier: str, retry=False) -> dict:
    """
    Fetch the RKD API for a single identifier and return the result as dict.

    Args:
        identifier: The excerpt identifier to fetch.
        retry: Whether to retry the request if the first attempt fails.

    Returns:
        The result of the API call as dict.
    """

    url = f"https://rkd.nl/api/record/excerpts/{identifier}"
    params = {"format": "json"}

    if retry:
        time.sleep(10)

    try:
        r = requests.get(url, params=params)
        return r.json()
    except JSONDecodeError:
        if retry:
            return {}
        else:
            return getAPI(identifier, retry=True)
    except requests.exceptions.ConnectionError:
        return getAPI(identifier, retry=True)


def fixDates(g: rdflib.ConjunctiveGraph) -> rdflib.ConjunctiveGraph:
    """
    Find and remove any incorrectly formatted dates that make a
    triplestore crash. This function prints the excerpt URI and
    the date to the console.

    Args:
        g: The graph object.

    Returns:
        The graph object without the incorrect dates
    """

    q = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX schema: <http://schema.org/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT * WHERE { 

        ?excerpt schema:contentReferenceTime ?sub .

        ?sub ?pred ?literal .
    
        FILTER(DATATYPE(?literal) = xsd:date)

    }
    """

    results = g.query(q)

    for r in results:
        try:
            parse_date(r.literal)
        except ValueError:
            print(r.excerpt, r.literal)
            g.remove((r.subject, r.predicate, r.literal))

    return g


if __name__ == "__main__":

    FILEPATH = "data/20220926_BrediusExportVolledig.xml"
    THESAURUSPATH = "data/rkdthesaurus.trig"
    # FILEPATH = "data/20210721brediusexportgoldenagents.xml"
    DESTINATION = "data/ga_20220926_BrediusExportVolledig.ttl"

    main(FILEPATH, DESTINATION)
