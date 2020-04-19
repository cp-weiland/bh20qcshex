from rdflib import Graph, Namespace
from pyshex.evaluate import evaluate

metadatafn = "metadata.rdf"

def rdf_strings(fname):
    try: 
        with open(fname) as foo_rdf:
            return foo_rdf.read()
    except IOError as e:
        raise SystemExit("I/O error({0}): {1}".format(e.errno, e.strerror), sys.exc_info()[0])
    except: #handle other exceptions
        raise SystemExit("Unexpected error:", sys.exc_info()[0])


def qc_shex(rdf):
    shex = rdf_strings("validation_shape.rdf")
    #rdf = rdf_strings(metadata)

    START = Namespace("http://whatever/")
    DEFAULT = Namespace("file:///peters_repo/bh20-seq-resource/example/")
    g = Graph()
    g.parse(data=rdf, format="turtle")
    rslt, reason = evaluate(g, shex, DEFAULT.placeholder, START.submissionShape)
    return rslt
    
if __name__ == '__main__':
    print(qc_shex(rdf_strings(metadatafn)))
