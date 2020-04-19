import schema_salad.schema
import schema_salad.ref_resolver
import logging
import pkg_resources
import logging
import traceback

import schema_salad.jsonld_context

def qc_metadata_rdf(metadatafile):
    schema_resource = pkg_resources.resource_stream(__name__, "bh20seq-schema.yml")
    cache = {"https://raw.githubusercontent.com/arvados/bh20-seq-resource/master/bh20sequploader/bh20seq-schema.yml": schema_resource.read().decode("utf-8")}
    (document_loader,
     avsc_names,
     schema_metadata,
     metaschema_loader) = schema_salad.schema.load_schema("https://raw.githubusercontent.com/arvados/bh20-seq-resource/master/bh20sequploader/bh20seq-schema.yml", cache=cache)

    if not isinstance(avsc_names, schema_salad.avro.schema.Names):
        print(avsc_names)
        return (False, None)

    try:
        doc, metadata = schema_salad.schema.load_and_validate(document_loader, avsc_names, metadatafile, True)
        g = schema_salad.jsonld_context.makerdf("workflow", doc, document_loader.ctx)
        rdf = g.serialize(format="turtle").decode("utf-8")
        return (True,rdf)
    except Exception as e:
        traceback.print_exc()
        logging.warn(e)
    return (False, None)

if __name__ == '__main__':

    qc_metadata("../example/metadata.yaml")
