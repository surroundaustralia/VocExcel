import sys
from pathlib import Path

import pytest
from rdflib import Graph, URIRef, Literal, compare
from rdflib.namespace import SKOS

sys.path.append(str(Path(__file__).parent.parent.absolute()))
from vocexcel import convert
from vocexcel.utils import ConversionError


def test_empty_template():
    assert Path(
        Path(__file__).parent.parent / "templates" / "VocExcel-template_042.xlsx"
    ).is_file()
    with pytest.raises(ConversionError) as e:
        convert.excel_to_rdf(
            Path(__file__).parent.parent / "templates" / "VocExcel-template_042.xlsx",
            output_type="file",
        )
    assert "7 validation errors for ConceptScheme" in str(e)


def test_simple():
    convert.excel_to_rdf(
        Path(__file__).parent / "042_simple_example.xlsx", output_type="file"
    )
    g = Graph().parse(Path(__file__).parent / "042_simple_example.ttl")
    assert len(g) == 131
    assert (
        URIRef(
            "http://resource.geosciml.org/classifierscheme/cgi/2016.01/particletype"
        ),
        SKOS.prefLabel,
        Literal("Particle Type", lang="en"),
    ) in g, "PrefLabel for vocab is not correct"
    # tidy up
    Path(Path(__file__).parent / "042_simple_example.ttl").unlink()