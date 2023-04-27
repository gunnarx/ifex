----
# What is an overlay?

An overlay is a special term in the layering approach.  Just be aware that we are sometimes are less careful and simply call these "layers" as well.

Overlay is used to signify a file that uses the same syntax (layer type) as an original file.   It redefines or augments certain aspects that were already (partly) defined in another file, but it does not add a completely new type of information.  To add new types of information, other layers of new Layer Type would be used.

In theory overlays could be supported for any Layer Type, but many tools might omit this capability for layer types where such features are not expected to be needed.

However, it is explicitly anticipated that overlays would be written for the core interface descriptions.  In other words, base files and overlays are likely to be in the IFEX core IDL syntax and the overlay augments, or changes the interface description in some way within the information scope of the IFEX core IDL syntax only.

Example: A file defines an Interface containing some methods
         An overlay adds an additional methods to the Interface already defined.
         Another overlay adds an additional error return type to every method (for example as a result of deploying the interface on a new transport that has special error cases).

With overlay strategy, multiple files are of the same layer type but are simply kept in separate files to be able to show changes on top of a base definition.

----

# What is a Layer?

Most of the time when we say layer we mean a layer instance, but when speaking less carefully it might refer to layer type, depending on the context.

More generally, a layer (instance) is an instance of a Layer Type.  In other words it is a file written to follow the format that is required by the Layer Type, and it defines the actual values that this type of layer is supposed to provide.

----

# What is a Layer Type?

There can be multiple layer types that define different meta-data about the interface and the target/deployment environment.  

A Layer Type is the definition of the allowed syntax for a certain type of layer.  The Layer Type is defined in a formal language (JSON/YAML schema or python class file) and it acts as a specification and 'schema' to check the validity of layer instances.

The IFEX philosophy is that pure interface descriptions (written in IFEX core IDL) are kept separate from details that are target/deployment specific.  The IFEX Core IDL language is built to be maximally generic and reusable in different contexts.

In contrast to that, new layer types are very often specific to a certain deployment scenario, so they might be defined and documented near the implementation of specific tooling for a specific purpose.  

**Example**:  

A code generator implementation may define a specific Layer Type for target/deployment information. It specifies the type of information that the code generator needs in addition to the interface description that was provided in IFEX Core IDL.  It means that when using this code generator, an IFEX interface file plus an instance of the layer type is required as input for the code generator to be able to do its job.

For further explanation of the layer concept in general, please refer to the IFEX Core Specification.

----

# When files are combined, is there any kind of ranking property for different IFEX files so that there will be a absolute order?

Not as part of the general IFEX specification.  The simple approach is that each individual IFEX tool shall independently decide and document its behavior.  

Scenario 1: A layer that adds new deployment details means the order does not matter - the final model combines the IFEX core IDL description and the augmented data set by the new layer types.

Scenario 2: For overlays that redefine or affect a previous definitions, a simple and common behavior is that files are simply read in the order they are given on the command line to the tool, which means that "last file wins" if a property is redefined.

That "last file wins" behavior is the most likely, and more complex setups are unlikely to be a much better solution.  However, if it becomes needed in some case, it is definitely possible for a certain tool to implement another behavior and explain it. Some additional input-configuration is required for a particular tool to modify the prioritization behavior.

Tools are also encouraged to provide flags as part of command-line parameters, that can enable/disable information about the processing, or control the processing.  For example, a warning may be printed when some item is re-defined by a later processed interface-file, but this could be disabled if that is expected behavior, or there could be an option to treat re-definition of items as an Error.

