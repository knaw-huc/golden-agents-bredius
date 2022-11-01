# Golden Agents / RKD - Bredius Notes

Pipeline to transform the RKD's Bredius RDF data to fit in the [Golden Agents](https://www.goldenagents.org) infrastructure and to reconcile the Bredius notes to their origin: the [Notarial Deeds in the Amsterdam City Archives](https://archief.amsterdam/uitleg/indexen/49-notariele-archieven-1578-1915).

This release contains both the scripts to transform the data and the resulting data.

**Table of contents**
- [Golden Agents / RKD - Bredius Notes](#golden-agents--rkd---bredius-notes)
  - [Introduction](#introduction)
  - [Data](#data)
    - [Files](#files)
    - [Changes/additions](#changesadditions)
    - [Example](#example)
  - [Enrichments](#enrichments)
    - [Reconciliation with notaries](#reconciliation-with-notaries)
    - [Reconciliation with inventories](#reconciliation-with-inventories)
  - [Linksets / Reconciliation](#linksets--reconciliation)
    - [Person linkset](#person-linkset)
    - [Deed linkset](#deed-linkset)
  - [Statistics](#statistics)
  - [License and citation](#license-and-citation)
  - [Contact](#contact)

## Introduction
Early 2021 the RKD launched a crowdsourcing platform to digitize and index the archival material made by art historian Abraham Bredius (1855-1946), who was one of the first researchers to delve into the Dutch archives (which at the time were not open to the public), taking a systematic approach to his search for life facts about artists working between the late sixteenth and early eighteenth century. Bredius' research resulted in tens of thousands of excerpts: summaries of equally numerous archive entries, written on small scraps of paper. The data collected by Bredius still offers a wealth of information and presents an initial point of access to the original archives.

By digitizing this material, one obtains more information on place names, dates, persons and occupations, and record types that are relevant for art historical research. Further more, the Golden Agents project integrates this dataset in RDF/LOD in its infrastructure, by which it offers a researcher additional context on this material, for instance by reconciling it with the original (digitized/indexed) material that is kept in the Amsterdam City Archives, but also by connecting the actors that are described to other (biographical) datasets, leading to a more accessible entry to information on the lifes of both producers and consumers of creative goods in seventeenth and eighteenth century Amsterdam.

In this case study, we will connect the Bredius notes to the original (digitized/indexed) material that is kept in the Amsterdam City Archives through the index that is made in the [_Alle Amsterdamse Akten_ project](https://alleamsterdamseakten.nl/). This exercise resembles our earlier approach to reconcile the data by Michael Montias that is kept in both the Getty Provenance Index and the Montias Database of the Frick Collection to their original origin. For more information about this project, see: 

* Leon van Wissen, Chiara Latronico, Sandra van Ginhoven, Veruska Zamborlini (2020). "The Montias Case: an experiment with data reconciliation and provenance between research and cultural heritage institutions." In: Book of Abstracts DH2020, ADHO. [Paper](https://dh2020.adho.org/wp-content/uploads/2020/07/137_TheMontiasCaseanexperimentwithdatareconciliationandprovenancebetweenresearchandculturalheritageinstitutions.html) and [Demo](https://lvanwissen.github.io/ga-dh2020-demo/).  

More information on the notes and the crowdsourcing project can be read on the website of the RKD: https://rkd.nl/en/projects-publications/projects/916-bredius-notes. Documentation on the data transformation and the reconciliation to the original sources can be found in this repository. 

## Data
### Files
* [`data/ga_20220926_BrediusExportVolledig.trig`](data/ga_20220926_BrediusExportVolledig.trig): the Bredius excerpts (with changes and additions, see below)
* [`notaries/bredius_linkset_excerpt2notary.trig`](notaries/bredius_linkset_excerpt2notary.trig): linkset between the Bredius excerpts and notaries (Notarissennetwerk)
* [`inventories/bredius_linkset_excerpt2inventory.trig`](inventories/bredius_linkset_excerpt2inventory.trig): linkset between the Bredius excerpts and inventories (EAD)
* [`linksets/bredius_linkset_9d6ca8c8fb1bc3be9c08d7e791bd08e0_15_accepted.trig`](linksets/bredius_linkset_9d6ca8c8fb1bc3be9c08d7e791bd08e0_15_accepted.trig): linkset between persons in the Bredius excerpts and persons in the Amsterdam Notarial Archives. Created with Lenticular Lens. Contains only the accepted links. Pick [`linksets/bredius_linkset_persons.trig`](linksets/bredius_linkset_persons.trig) if you want a simplified version with just the `owl:sameAs` links.
* [`linksets/bredius_linkset_deeds.trig`](linksets/bredius_linkset_deeds.trig): linkset between external documents in the Bredius excerpts and deeds in the Amsterdam Notarial Archives.

Optional:
* [`data/rkdthesaurus.trig`](data/rkdthesaurus.trig): an integral dump of the RKD thesaurus, used to enrich the Bredius excerpts with thesaurus terms and labels. These labels are already integrated in the data through the schema.org vocabulary.

### Changes/additions
This repository hold the data coming from the crowdsourcing initative, as well as a script that modifies the data slightly so that it fits in the Golden Agents infrastructure. What is added and changed is the following (through `main.py`):

  1. Add a `schema:url` to every `schema:Manuscript` (=index on an excerpt) to the public page of the excerpt, such as <<https://rkd.nl/explore/excerpts/778414>>
  2. Remove the `schema:additionalType` statement on persons and model their described roles in the excerpts using the `schema:Role` approach, in order to preserve context when these resources are disambiguated.
  3. Add a thumbnail of the excerpt in a `schema:image` statement to every excerpt.
  4. Remove faulty labels from all thesaurus entries and replace them with the right ones. A full extract of the RKD Thesaurus is used for this. Also, incorrect URIs and dates are removed.
  5. Blank nodes are skolemized and all triples are packed inside a named graph. 
  
The updated RDF in application/trig (.trig) can be found here: [ga_20220926_BrediusExportVolledig.trig](data/ga_20220926_BrediusExportVolledig.trig)
  
### Example

```turtle
<https://data.rkd.nl/excerpts/780314> a schema:ArchiveComponent,
        schema:Manuscript ;
    schema:about <https://data.goldenagents.org/.well-known/genid/nbe4b578062e24d088ebe0290c9140592b31163>,
        <https://data.goldenagents.org/.well-known/genid/nbe4b578062e24d088ebe0290c9140592b31164>,
        <https://data.goldenagents.org/.well-known/genid/nbe4b578062e24d088ebe0290c9140592b31165>,
        <https://data.goldenagents.org/.well-known/genid/nbe4b578062e24d088ebe0290c9140592b31166>,
        <https://data.goldenagents.org/.well-known/genid/nbe4b578062e24d088ebe0290c9140592b31167>,
        <https://data.goldenagents.org/.well-known/genid/nbe4b578062e24d088ebe0290c9140592b31168>,
        <https://data.rkd.nl/thesaurus/3> ;
    schema:contentReferenceTime <https://data.goldenagents.org/.well-known/genid/nbe4b578062e24d088ebe0290c9140592b31169> ;
    schema:identifier "0380.226_0021_02.C02",
        "780314" ;
    schema:image <https://images.rkd.nl/rkd/thumb/650x650/88d23d6d-d085-f3c2-0d57-536eb25ba9ef.jpg> ;
    schema:isBasedOn <https://data.rkd.nl/collection/bredius/externalitem/780314> ;
    schema:isPartOf <https://data.rkd.nl/collections/380> ;
    schema:keywords <https://data.rkd.nl/thesaurus/96194> ;
    schema:url <https://rkd.nl/explore/excerpts/780314> .

<https://data.goldenagents.org/.well-known/genid/nbe4b578062e24d088ebe0290c9140592b31163> a schema:Role ;
    schema:about <https://data.rkd.nl/excerpts/780314/person/IDGCWSF2ZQJ5SHHYQ0NYIENHIG3PPXKM5P1UWFM3MXI42O4MBFRRON> ;
    schema:name "Adriaen Doncker (medicus)"@en,
        "Adriaen Doncker (medicus)"@nl ;
    schema:roleName <https://data.rkd.nl/thesaurus/84550> .

<https://data.goldenagents.org/.well-known/genid/nbe4b578062e24d088ebe0290c9140592b31164> a schema:Role ;
    schema:about <https://data.rkd.nl/excerpts/780314/person/IDTZORYOQQYDKNCQOCZFSNULZECI5YWUQ2HB51BJPHOMEV3KOXN0FH> ;
    schema:name "Anthoni de Haen (Unknown)"@en,
        "Anthoni de Haen (Onbekend)"@nl .

<https://data.goldenagents.org/.well-known/genid/nbe4b578062e24d088ebe0290c9140592b31165> a schema:Role ;
    schema:about <https://data.rkd.nl/excerpts/780314/person/IDA2IH1LBVCH2QGCLYMGJEFQK3ZJEO0UKJN2EDAZG1AESUSMXCNRWM> ;
    schema:name "Isaacq Dellenboom (merchant)"@en,
        "Isaacq Dellenboom (koopman)"@nl ;
    schema:roleName <https://data.rkd.nl/thesaurus/63026> .

<https://data.goldenagents.org/.well-known/genid/nbe4b578062e24d088ebe0290c9140592b31166> a schema:Role ;
    schema:about <https://data.rkd.nl/excerpts/780314/person/IDISZQO4AOGGJSLZIBA5OMUYKMGFSA1QZ2AC4S4VDR5RB2YRMFOBNJ> ;
    schema:name "Dina de Haen (requirant (no translation))"@en,
        "Dina de Haen (requirant)"@nl ;
    schema:roleName <https://data.rkd.nl/thesaurus/96280> .

<https://data.goldenagents.org/.well-known/genid/nbe4b578062e24d088ebe0290c9140592b31167> a schema:Role ;
    schema:about <https://data.rkd.nl/excerpts/780314/person/ID4OWCJJU0QBX4MITDBHNDXORGNIN3YE2BPWT3CGMDD2IXKRCJNACI> ;
    schema:name "Pieter van Roon (notary)"@en,
        "Pieter van Roon (notaris)"@nl ;
    schema:roleName <https://data.rkd.nl/thesaurus/65019> .

<https://data.goldenagents.org/.well-known/genid/nbe4b578062e24d088ebe0290c9140592b31168> a schema:Role ;
    schema:about <https://data.rkd.nl/excerpts/780314/person/IDQWJGJDW5CXXMPQTVMCCQY5FILIKO0KV4WPXLBWKY4NK5KHTB211C> ;
    schema:name "Seger van der Maes (Unknown)"@en,
        "Seger van der Maes (Onbekend)"@nl .

<https://data.goldenagents.org/.well-known/genid/nbe4b578062e24d088ebe0290c9140592b31169> a schema:StructuredValue ;
    schema:endDate "1683-08-11"^^xsd:date ;
    schema:startDate "1683-08-05"^^xsd:date .

<https://data.rkd.nl/thesau/3> a schema:Place ;
    schema:name "The Hague"@en,
        "Den Haag"@nl .

<https://data.rkd.nl/collection/bredius/externalitem/780314> a schema:CreativeWork ;
    schema:name "Verbalen"@nl .
```

## Enrichments 

### Reconciliation with notaries

We select all excerpts from which we think that they are based on deeds from the Amsterdam Notarial Archive by filtering on (1) mentioned place `Amsterdam`, and (2) the name of the external document that contains the prefix `Overige vindplaatsen: Notarieel Archief, notaris `:

```SPARQL
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <https://schema.org/>
SELECT ?excerpt ?name WHERE {
  ?excerpt a schema:Manuscript ;
    schema:about <https://data.rkd.nl/thesaurus/29> ; # Amsterdam
    schema:isBasedOn ?saa_deed .
  
  ?saa_deed a schema:CreativeWork ;
    schema:name ?deed_label .
  
  FILTER(CONTAINS(?deed_label, 'Overige vindplaatsen: Notarieel Archief, notaris '))
  
  BIND(STRAFTER(?deed_label, 'Overige vindplaatsen: Notarieel Archief, notaris ') AS ?notary_name)
  
} ORDER BY ?name
```

These are linked to their respective notary in the Notarissennetwerk (https://notarissennetwerk.nl/) in [`excerpt2notary.csv`](notaries/excerpt2notary.csv) and transformed into a linkset using the `schema:author` property in [`bredius_linkset_excerpt2notary.trig`](notaries/bredius_linkset_excerpt2notary.trig).

### Reconciliation with inventories

We link the excerpts to the inventories they came from. These are described seperately in the EAD of collection 'Archief Abraham Bredius' (https://rkd.nl/explore/archives/details/NL-HaRKD-0380). See [`bredius_linkset_excerpt2inventory.trig`](inventories/bredius_linkset_excerpt2inventory.trig).

## Linksets / Reconciliation

### Person linkset

A linkset between persons described in the Bredius excerpts and persons indexed in the Notarial Archives is created using the Lenticular Lens tool (https://lenticularlens.org/). Criteria for the match were:
1. The name of a person has a normalized levenshtein similarity of 0.7
2. Either the first or the second date mentioned in an excerpt is the date of the registration in the Notarial Archive
3. We only match against deeds from inventory numbers written by the notary that was entered in the Bredius dataset (via our enrichment, see above) 

This yielded a total of 971 found links, of which 860 were (manually) marked as correct. The resulting linkset (in application/trig, with and without extra reification) can be found in the [linksets](linksets) folder.

### Deed linkset

We can create a linkset on the deed level from the above described person linkset by using this query:

```SPARQL
PREFIX schema: <https://schema.org/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rpp: <https://data.goldenagents.org/ontology/roar/>
CONSTRUCT {
    ?external_deed owl:sameAs ?deed .
} { 
	?manuscript a schema:Manuscript ;
             schema:about/schema:about ?person ;
             schema:isBasedOn ?external_deed .
    
    ?person a schema:Person ;
            owl:sameAs ?saa_person . # through the linkset
    
    ?deed rpp:mentionsPerson ?saa_person .
    
}
```

The result can be found in [`bredius_linkset_deeds.trig`](linksets/bredius_linkset_deeds.trig).

## Statistics

| # | Property | Value |
| --- | --- | --- |
| 1 | Total number of statements | 511.838 |
| 2 | Total number of persons in excerpts | 30.295 |
| 3 | Total number of excerpts | 11.117 |
| 4 | Total number of excerpts linked to notaries | 3.731 |
| 5 | Total number of links | 860 |
| 6 | Total number of linked persons | 711 |
| 7 | Total number of linked deeds | 249 |

## License and citation

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/) 
[![DOI](https://zenodo.org/badge/399210210.svg)](https://zenodo.org/badge/latestdoi/399210210)

The original data was created in the Bredius Notes project and is processed by the RKD (https://rkd.nl/en/). The data in this repository is licensed under a Creative Commons Attribution 4.0 International license and can be used freely, as long as you provide attribution to both the Golden Agents Project (e.g. by citation) as well as the RKD (e.g. by linking to individual excerpts on rkd.nl).

* Van Wissen, L., Reinders, J., Golden Agents project, & RKD Netherlands Institute for Art History. (2022). Golden Agents / RKD - Bredius Notes (Version v1.0) [Data set]. https://github.com/knaw-huc/golden-agents-bredius/

```bibtex
@misc{van_Wissen_Golden_Agents_2022,
author = {van Wissen, Leon and Reinders, Jirsi and {Golden Agents project} and {RKD Netherlands Institute for Art History}},
month = {11},
title = {{Golden Agents / RKD - Bredius Notes}},
url = {https://github.com/knaw-huc/golden-agents-bredius/},
year = {2022}
}
```

## Contact

More info and questions: https://www.goldenagents.org/about/ or l.vanwissen@uva.nl
