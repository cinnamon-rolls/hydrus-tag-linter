# Hydrus Tag Linter

This is a python script that searches your database for files that match a set
of rules, which are defined in `JSON` files. This is to assist in ensuring that
your tags don't get out of hand by saving all your tedious searches for 'messed
up' files in one place.

The results are printed into an `html` file. Once you run the script, open the
`html` document in a web browser, and copy one of the blocks of hashes. Then, go
to your Hydrus instance, and search by `system:hash`. Paste the block of hashes,
then click `search`.

The workflow I intend is...

1. Run the script, get a list of 'bad' files
2. Search for those files, then for each file...
   1. Adjust the files tags, OR
   2. Adjust the rule definition, OR
   3. Delete the file

Pull requests and issues are welcome, though I ask that the pull requests are
kept focused to a single feature/improvement. 

## Usage

I recommend that you create a folder named `my-rules` and put any rules you
don't want GitHub to track there.

I have included a script named `example_run.sh` which has all the arguments you
need to get started. Open it up, paste in your access key, and then run it.

## Rules

`Rule`s are defined as `JSON` objects, and many rules are stored inside of a
`rules` folder. The `rules` folder is set with the `--rules` or `-r` argument.

The layout of a `Rule` object is as follows

|    Key     |                       Value                       |
| :--------: | :-----------------------------------------------: |
|   `name`   |     The name of the rule (for human readers)      |
|   `note`   |    The description of the rule, like a comment    |
|  `search`  | The `Search` that reveals faulty files, see below |
| `disabled` | If a truthy value, then the file will be ignored  |

An example:

```json
{
    "name": "Character Without Series",
    "note": "Files with a 'character' tag should also have a 'series' tag.",
    "search": [
        "character:*",
        "-series:*",
        "-character:character request",
        "-meta:character request",
        "-character:original"
    ]
}
```

## Search Definitions

The simplest search definition is a single string, which will match all files in
the database to a single tag, *e.g.*

```json
"evil tag"
```

The single string definition is completely equivalent to passing an array of
strings with only one element

```json
[ "foo" ]
```

If an array is given with multiple elements, then it will match all files in the
database that have all of those tags *e.g.*

```json
[ "foo", "bar", "barfoo (...)" ]
```

To perform an "OR" search, use the following syntax, which is defined
recursively

```json
{
    "op": "union",
    "of": [
        "search definition...",
        "search definition...",
        "search definition (as many or as little as you'd like)..."
    ]
}
```

Tags can be negated by putting a `-` in front of the tag's name, and namespaces
can be searched with wildcards using the `*` character, e.g. `character:*`

## Comments

Comments are not permitted in any of the `JSON` files, but the `$comment` key may
be added and is guaranteed to always be ignored by all versions of this
software.
