package after_resolution

import rego.v1

# Collect all attribute keys referenced by any signal

referenced_attr_keys contains key if {
    some span in input.registry.spans
    some attr in span.attributes
    key := attr.key
}

referenced_attr_keys contains key if {
    some metric in input.registry.metrics
    some attr in metric.attributes
    key := attr.key
}

referenced_attr_keys contains key if {
    some event in input.registry.events
    some attr in event.attributes
    key := attr.key
}

# Warn for attributes not referenced by any signal

deny contains finding if {
    some attr in input.registry.attributes
    not attr.key in referenced_attr_keys
    finding := {
        "id": "unused_attribute",
        "context": {"attribute_key": attr.key},
        "message": sprintf("Attribute '%s' is not referenced by any signal (span, metric, or event)", [attr.key]),
        "level": "violation",
    }
}
