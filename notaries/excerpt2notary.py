import pandas as pd
from rdflib import Graph, URIRef, Literal, RDF, SDO


def main(infile: str, outfile: str):
    """
    Convert a spreadsheet with excerpt and notary 
    information into a linkset using the `schema:author` property.

    Example:
        ```turtle

        <https://data.rkd.nl/collection/bredius/externalitem/777565> schema:author <https://data.goldenagents.org/datasets/notarissennetwerk/person/1946> .

        <https://data.goldenagents.org/datasets/notarissennetwerk/person/1946> a schema:Person ;
            schema:name "Palm Mathijsz" .

        ```

    Args:
        infile (str): The input file path in csv.
        outfile (str): the output file path in trig.
    """

    df = pd.read_csv(infile)

    g = Graph(identifier="https://data.goldenagents.org/datasets/bredius/")

    for r in df.to_dict(orient="records"):

        if pd.isna(r["notary"]):
            continue

        s = r["excerpt"].replace("/excerpts/", "/collection/bredius/externalitem/",)
        nn = URIRef(r["notary"])
        nname = r['notary_name']

        g.add((nn, RDF.type, SDO.Person))
        g.add((nn, SDO.name, Literal(nname)))
        g.add((URIRef(s), SDO.author, nn))

    g.bind("schema", SDO)
    g.serialize(outfile, format="trig")


if __name__ == "__main__":

    INFILE = "excerpt2notary.csv"
    OUTFILE = "linkset_excerpt2notary.trig"

    main(INFILE, OUTFILE)

