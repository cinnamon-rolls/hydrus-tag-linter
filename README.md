# Hydrus Tag Linter

This is a Python application written for the [Hydrus Network
Client](https://github.com/hydrusnetwork/hydrus). The purpose of the program is
to help you keep your tags consistent in your database by checking your files
and their tags against user-defined rules. Some default rules are provided in
the `default-rule` directory, but you are encouraged to write your own for your
specific needs.

Once launched, a server will be running which you can connect to using your
internet browser. The default URL is `http://localhost:45868/`, which you can
change using the command line arguments.

**Note:** anyone who can connect to this server will have indirect access to
your Hydrus Client. It is strongly recommended that you run this on `localhost`
only, unless you know what you're doing.

The workflow I intend is...

1. Run the program and get a report on what's wrong
2. Use your problem solving skills and the provided tools to fix it
3. [Repeat](https://github.com/hydrusnetwork/hydrus/blob/master/static/boned.jpg)

For more documentation, check the [Wiki](https://github.com/cinnamon-rolls/hydrus-tag-linter/wiki)

## Running

Dependencies: `flask`, `hydrus-api`

I have included a script named `example_run.sh` which has all the arguments you
need to get started. Open it up, paste in your access key, and then run it.
Note: the `example_run.sh` file may change between versions.

You can use the `--help` argument to get a list of command line arguments

More information is available at the wiki.

## Credits

Also, some of famfamfam's Silk Icons are used. You can download them for your
own project at http://www.famfamfam.com/lab/icons/silk/
