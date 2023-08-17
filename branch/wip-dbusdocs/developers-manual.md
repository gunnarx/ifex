[WARN] INCLUDE find no file <<generated-dev-toc.md>>
[WARN] INCLUDE find no file <<static-ifex-type-howto.md>>
# IFEX Developers' Manual


# Mapping documents

By "mapping" we mean to describe how we may interpret and ultimately translate IFEX to or from another interface description environment, or a particular output format (computing environment, protocol, programming language, etc.).  It can be such things as listing the "features" of IFEX and seeing how we may implement those features in the target environment (or the opposite direction, listing the features of the other environment and how IFEX can meet them).

General documents describe our general strategy for approaching mappings.

Individual documents describe particular target (or source) standards.

- [D-Bus](./static-mapping-dbus.md)

# Generators

When the documentation speaks about generators, it is simply programs that output (non-IFEX) output:

- Other IDL formats
- Traditional "code generation", i.e. the output is written in a programming language
- Documentation

etc.

## Configurability - when to create a layer?

There are two major ways that a tool can be configured

- At invocation, for example using command-line
- Through IFEX "Layers" as input

The layer inputs might not be considered any different from other input files

Q: When to put configurability into layers, vs. the tool?

Layers are usually designed to refer to the individual items in the IFEX Core IDL description and add new metadata to their definitions.  Thus, layers are there to configure things _individually_ (or through some pattern matching) on each item that is described in the interface.   For example, one `Property` might have get/set methods generated for it, whereas another `Property` _in the same interface_ should only have subscribe/unsubscribe methods generated for it.   One `Method` might be marked as "asynchronous" to generate appropriate code for asynchronous invocation, whereas another is going to be synchronous/blocking.  And so on.

Just like the interface descriptions (IFEX Core IDL), _different_ layer files are given to the tool on each invocation.

In contrast, parameters that affect mostly the _whole_ generation step equally and is not modifying individual items of the input, should be given directly to the tool.  Most commonly, this is done by designing command line parameters that the tool accepts when it is run, but it is up to the designer if the tool should perhaps have an external configuration ("dot-file") for example.

______________________________________________________________________

