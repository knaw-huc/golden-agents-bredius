# Golden Agents / RKD - Bredius Notes

:warning: | This repository is work in progress and contains unfinished data. 
:---: | :---

Pipeline to transform the RKD's Bredius RDF data to fit in the [Golden Agents](https://www.goldenagents.org) infrastructure and to reconcile the Bredius notes to their origin: the [Notarial Deeds in the Amsterdam City Archives](https://archief.amsterdam/uitleg/indexen/49-notariele-archieven-1578-1915).

**Table of contents**
- [Golden Agents / RKD - Bredius Notes](#golden-agents--rkd---bredius-notes)
  - [Introduction](#introduction)
  - [Data](#data)
    - [Changes/additions](#changesadditions)
    - [Example](#example)
  - [Linksets / Reconciliation](#linksets--reconciliation)
  - [License](#license)
  - [Contact](#contact)

## Introduction
Early 2021 the RKD launched a crowdsourcing platform to digitize and index the archival material made by art historian Abraham Bredius (1855-1946), who was one of the first researchers to delve into the Dutch archives (which at the time were not open to the public), taking a systematic approach to his search for life facts about artists working between the late sixteenth and early eighteenth century. Bredius' research resulted in tens of thousands of excerpts: summaries of equally numerous archive entries, written on small scraps of paper. The data collected by Bredius still offers a wealth of information and presents an initial point of access to the original archives.

By digitizing this material, one obtains more information on place names, dates, persons and occupations, and record types that are relevant for art historical research. Further more, the Golden Agents project integrates this dataset in RDF/LOD in its infrastructure, by which it offers a researcher additional context on this material, for instance by reconciling it with the original (digitized/indexed) material that is kept in the Amsterdam City Archives, but also by connecting the actors that are described to other (biographical) datasets, leading to a more accessible entry to information on the lifes of both producers and consumers of creative goods in seventeenth and eighteenth century Amsterdam.

In this case study, we will connect the Bredius notes to the original (digitized/indexed) material that is kept in the Amsterdam City Archives through the index that is made in the [_Alle Amsterdamse Akten_ project](https://alleamsterdamseakten.nl/). This exercise resembles our earlier approach to reconcile the data by Michael Montias that is kept in the Getty Provenance Index to their original origin. For more information about this project, see: 

* Leon van Wissen, Chiara Latronico, Sandra van Ginhoven, Veruska Zamborlini (2020). "The Montias Case: an experiment with data reconciliation and provenance between research and cultural heritage institutions." In: Book of Abstracts DH2020, ADHO. [Paper](https://dh2020.adho.org/wp-content/uploads/2020/07/137_TheMontiasCaseanexperimentwithdatareconciliationandprovenancebetweenresearchandculturalheritageinstitutions.html) and [Demo](https://lvanwissen.github.io/ga-dh2020-demo/).  

More information on the notes and the crowdsourcing project can be read on the website of the RKD: https://rkd.nl/en/projects-publications/projects/916-bredius-notes. Documentation on the data transformation and the reconciliation to the original sources can be found in this repository. 

## Data
### Changes/additions
This repository hold the data coming from the crowdsourcing initative, as well as a script that modifies the data slightly so that it fits in the Golden Agents infrastructure. What is added and changed is the following:

  1. Add a `schema:url` to every `schema:Manuscript` (=index on an excerpt) to the public page of the excerpt, such as <<https://rkd.nl/explore/excerpts/778414>>
  2. Remove the `schema:additionalType` statement on persons and model their described roles in the excerpts using the `schema:Role` approach, in order to preserve context when these resources are disambiguated.
  3. Add a thumbnail of the excerpt in a `schema:image` statement to every excerpt.
  
The updated RDF in text/turtle (.ttl) can be found here: [ga_20210721brediusexportgoldenagents.ttl](data/ga_20210721brediusexportgoldenagents.ttl)
  
### Example

```turtle
<https://data.rkd.nl/excerpts/780314> a schema:ArchiveComponent,
        schema:Manuscript ;
    schema:about [ a schema:Role ;
            schema:about <https://data.rkd.nl/excerpts/780314/person/IDD0H5DSSR1SCFN1A5DU53OJU1KNT542P0OIQQ00KNCFUGXPBW5HEO> ;
            schema:name "Isaacq Dellenboom (merchant)"@en,
                "Isaacq Dellenboom (koopman)"@nl ;
            schema:roleName <https://data.rkd.nl/thesau/63026> ],
        [ a schema:Role ;
            schema:about <https://data.rkd.nl/excerpts/780314/person/IDO0YYBU40NYMTJDBADXGVRMYUUJ1NEKFJLTJG44J0DVUC2ACJKAN> ;
            schema:name "Pieter van Roon (notary)"@en,
                "Pieter van Roon (notaris)"@nl ;
            schema:roleName <https://data.rkd.nl/thesau/65019> ],
        <https://data.rkd.nl/thesau/3> ;
    schema:contentReferenceTime [ a schema:StructuredValue ;
            schema:endDate "1683-08-11"^^xsd:date ;
            schema:startDate "1683-08-05"^^xsd:date ] ;
    schema:identifier "0380.226_0021_02.C02",
        "780314" ;
    schema:image <https://images.rkd.nl/rkd/thumb/650x650/88d23d6d-d085-f3c2-0d57-536eb25ba9ef.jpg> ;
    schema:isBasedOn <https://data.rkd.nl/collection/bredius/externalitem/780314> ;
    schema:isPartOf <https://data.rkd.nl/collections/380> ;
    schema:url <https://rkd.nl/explore/excerpts/780314> .
    
<https://data.rkd.nl/excerpts/780314/person/IDD0H5DSSR1SCFN1A5DU53OJU1KNT542P0OIQQ00KNCFUGXPBW5HEO> a schema:Person ;
    schema:name "Isaacq Dellenboom" ;
    schema:subjectOf <https://data.rkd.nl/excerpts/780314> .

<https://data.rkd.nl/excerpts/780314/person/IDO0YYBU40NYMTJDBADXGVRMYUUJ1NEKFJLTJG44J0DVUC2ACJKAN> a schema:Person ;
    schema:name "Pieter van Roon" ;
    schema:subjectOf <https://data.rkd.nl/excerpts/780314> .

<https://data.rkd.nl/thesau/3> a schema:Place ;
    schema:name "The Hague"@en,
        "Den Haag"@nl .

<https://data.rkd.nl/collection/bredius/externalitem/780314> a schema:CreativeWork ;
    schema:name "Verbalen"@nl .
```

## Linksets / Reconciliation
WIP

## License

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)

The original data was created in the Bredius Notes project and is processed by the RKD (https://rkd.nl/en/). The data in this repository is licensed under a Creative Commons Attribution 4.0 International license and can be used freely, as long as you provide attribution to both the Golden Agents Project (e.g. by citation) as well as the RKD (e.g. by linking to individual excerpts on rkd.nl).

## Contact

More info and questions: https://www.goldenagents.org/about/ or l.vanwissen@uva.nl
