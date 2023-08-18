[WARN] INCLUDE find no file <<generated-dev-toc.md>>
# IFEX Developers' Manual

This has information that is useful primarily for implementation of new IFEX tools, but occasionally also for people who develop software that uses artifacts that are generated to/from IFEX.   Before reading the developers' manual, make sure you have read the [IFEX Core IDL pecification](ifex-specification.md) and [FAQ](./FAQ.md) first.


# Datatype mapping

This is a general overview of how to approach mapping of fundamental datatypes between IFEX and another technical environment.

Based on this general advice, specific plans are typically written for the translation/mapping between IFEX and a certain technology.  They might be linked under the [Mapping documents](#mapping-documents) chapter.

## Common types that are trivially mapped to/from IFEX fundamental types

### (Direction Other -> IFEX)

| Generic data type | Explanation | IFEX Fundamental type | How to represent in IFEX if not fundamental type |
| --- | --- | --- | --- |
| Integer |  | uint32, int32, and other sizes... |  |
| Floating point |  | float, double   |  |
| Boolean |  | boolean |  |
| Tuple | A pair, triple, or larger group of objects, possibly of different type. | -- | Assumed to be represented by an array of fixed size (if identical types), or a `Struct` (if mixed types), or array of `Variant`s (if unknown/dynamic mixed types are needed)** |
| Union/Variant |  A data type that allows a variable to hold values of different data types at different times.   |  variant |  |
| Bit field | Efficient encoding of on/off true/false switches, as a collection of bits handled as an integer | -- |  Assumed to be represented by a fixed size integer\*\*, or (better, more descriptive and more generic) by an array of booleans\*\* |
| Enum class |  Enumeration type that provids type safety and scoping of constants.  |  Enumeration  |  |
| Set |  A collection of unique elements, where each element occurs only once. A set is typically used to store a collection of items that are unordered and where the order does not matter.   |  set (new)\* | |
| Map/Dictionary/Key-Value |  A collection of key-value pairs, where each key is associated with a value.  | map (new)\* |  |

\* Sets and Maps could have been represented in IFEX using the other fundamental types, possibly with a "Layer" that adds on the special behavior of Sets and Maps.  (How Set/Map can be simulated in environments that don't support them natively is described in the next chapter).  Despite this, it was decided that sets and maps in interfaces are common enough that IFEX Core IDL should support them as fundamental types.

\*\* These solutions propose to represent datatypes using a _comparable_ fundamental type in the IFEX interface description.  In many cases this is enough and carries the required behavior over to the IFEX Core IDL types.  However, in some cases this might be more like an approximation of the original type behavior.  If there are any constraints or type behavior that would be lost be translating to the IFEX Core IDL _only_, then an additional layer file can be created to include those aspects.  If this seems hard to understand, it is probably clearer when looking at the other direction IFEX -> Other, in which case such additional layers will be part of the input files to control how the IFEX representation shall be translated to the Other environment.  In any case, when processed, this combination of IFEX Core IDL and possibly additional layer can ensures the behavior remains according to the original type.  

For example: the generic interface description may contain several parameters that are of type array-of-boolean.  The usage might in some environments have a deployment model that specifies that (for one specific instance) it shall be represented as a bitfield, whereas other instances remain as array-of-boolean in the generated code.  Other code-generation environments may instead have a built in rule that bitfields shall be used as the _default_ translation.  In either case, these particular mapping rules are defined by the target environment, i.e. requirements on how the code-generator shall behave, including additional information that the deployment model may provide.  They are not in the core interface description, as represented by the IDL, but in additional layers, as well as the particular behavior of the code-generator (as described in its requirements or documentation).

### (Direction IFEX -> Other)

For primitive types, we won't repeat them here - in effect the table above can simply be referred to in reverse order.  From time to time a widening (using more bits) might be needed for ints and floats if the exact size is not available in the target environment.  We would expect widening mappings to be safe but when a mapping is reversed we should normally not use a narrowing mapping, unless it is known to be safe, for example through known value-range constraints.

Let's consider a few of the slightly more complex types.  

Consider this an example of how we may represent things on a data protocol that does not fundamentally know about specific type behaviors like Set and Map, but can fundamentally only transfer things like arrays and structs.

| IFEX Fundamental type | Explanation |  If Other does *not* support the type |
| --------------------- | -- | ---------------------------------- | ------------------------------------------------------------------|
| `set` |  A collection of unique elements, where each element occurs only once, and usually, the order does not matter | A set can simply be represented by a collection (array). That values shall be unique is either known and enforced on both sides of a server/client interface, and/or after data-transfer an actual Set type might be used in the rest of the program if the programming language supports it |
| `map` |  A collection of key-value pairs, where each key is associated with a value. | A map an be represented as a linear array of Variant (alternating keys and values), or better structured as an array of 2-tuples (pairs).  A tuple in turn is also either a 2-array, or a struct with two members.  The most natural choice is to represent it as an array of struct with one key and one value member, using Variant types, if either type is unknown. |
| `opaque` | An IFEX representation of a data type that is either not possible or not desired to describe in further detail | Can be equivalent to a void-pointer (low-level C), Variant<> type (where supported), or array-of-bytes.  When transferring Opaque across a data protocol, it might be `Variant` if supported, or simply be an array-of-bytes, where the server and client knows how to re-interpret the value on the other side |
| `variant` | ariant| An IFEX representation of a "union" or "variant" type - in other words a type that contains one (any) choice out of a list of multiple types.  In programming environments that support Variant types it is not an unknown binary-blob, but the _actual_ type of the object is known underneath.  Like opaque, there are several possible ways to creatively represent variant if the target environment does not have the type built in.  If the client and server side can be trusted to both convert the serialized representation back to the correct Variant type, then an anonymous "blob" (array of bytes) can of course be used for the data transfer.  If not, more creative solutions need to be created where we represent both the data, and the _actual_ type information explicitly (in a struct for example).|


## Additional types available in some programming environments

| Generic data type | Explanation | IFEX Fundamental type | How to represent in IFEX if not fundamental type |
| --- | --- | --- | --- |
| Function/Lambda  |  Some programming environments have functions as first class objects and can transfer them as arguments in interfaces. | -- |  The application of this would often be specific to a programming language environment, and it's unlikely that the interface description will be highly portable if this feature was represented in the interface description.  When needed it is possible to define an appropriate typedef for transferring code, for example as a string (interpreted language) or binary blob (compiled/bytecode), or as fallback "opaque".  Beyond this, the details are undefined in the core IDL scope and left open for a target environment to define. |
| Reference/Pointer  |  | -- |  This is not considered a _datatype_ in the IDL.  If we are truly speaking about a Type, that signifies a reference to something else, this could be modeled using a system-specific typedef, like using a string name/identifier to refer to an object, or any other appropriate encoding of that data.  That is the explaination why Reference/Pointer it is not seen as a _datatype_ in its own right.  To understand how _arguments are passed_ by pointer or reference (in C++ or other languages), see the separate section below. |
| Iterator  |  A data type that allows traversal of elements in a container, such as an array or linked list.   | -- |  Assumed to be represented by a primitive type such as integer (or struct if required)   |

## Opaque (special) type

If a system includes some data type that does not fit into any of the generalized types above, it can be modeled as the **opaque** type in the IFEX IDL.  This is a last resort and together with information that is probably provided by a deployment layer, a specific code generator would encode the type behavior that is necessary.

# Comments on pointers, references, etc.

The core interface description (IDL) does not prescribe how to transfer an argument to a method, only the type of the argument, and its in/out expectation.  In a lot of cases, IFEX will be used in an over-the-network IPC or RPC scenario where the question of pointers/reference is moot.  However, when used to represent a programming interface it may be worthwhile to comment on this.  From the general IFEX description we can deduce that a pass-by-value behavior is generally assumed for "in" parameters.  However, it is still up to the target environment code generator to decide if language features like pointers and references make sense.  The exact translation might be controlled by deployment layer information.  For example, some target environments could make use of immutable (const) references in the generated code for "in" parameters, and pointers or references for "out" parameters.  In either of these cases there is still no need to mention a specific reference type in the IFEX interface description - it is all decided in the particular target environment mapping.  This is a long way of saying that the IFEX core IDL does not need to support the concept of pointers or references, but in particular cases code-generators might use certain layer types to control if such features are used.



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

Let's identify two main ways that a tool can be configured:

- At invocation, for example using command-line flags/parameters
- Through IFEX "Layers" - which are input files in addition to the main IFEX core IDL file.

The layer inputs might not be considered any different from other input files

Q: When to put configurability into layers, vs. the tool?

A: Consider if the behavior changed "for all input", or in different ways for different objects mentioned in the main IFEX IDL file.

Layers are usually designed to refer to the individual items in the IFEX Core IDL description and add new metadata to their definitions.  Thus, layers are there to configure things _individually_ (or through some pattern matching) on each item that is described in the interface.   For example, one `Property` might have get/set methods generated for it, whereas another `Property` _in the same interface_ should only have subscribe/unsubscribe methods generated for it.   One `Method` might be marked as "asynchronous" to generate appropriate code for asynchronous invocation, whereas another is going to be synchronous/blocking.  And so on.

Just like different interface descriptions (IFEX Core IDL), _different_ layer files might be given to the tool on each invocation.

In contrast, parameters that affect mostly the _whole_ generation step equally and are not modifying individual items of the input, should be given directly to the tool.  Most commonly, this is done by designing command line parameters that the tool accepts when it is run, but it is up to the designer to decide if an some other file (perhaps YAML) file is provided as input also to control such global configurations.

______________________________________________________________________

