## Welcome to yogen!

yogen is a straighforward static site generator written in Python. It allows you to create and iterate websites by using Markdown or HTML files. Made for those looking for a no-fuss, quick to setup, not get in your way tool.

## Features

- Live editing for fast iteration
- Partial rebuilding
- Simple templating system
- Generation of RSS feeds

## Quick setup

You can install yogen via [PyPy](), or by downloading the [executable]().

## All the commands

- `yogen create name`: Creates your site's directory.
- `yogen build`: Compiles your site, generating the output in the `build` folder.
- `yogen serve [--no-live] [port]`: Serves the site locally on the given port (default: 8000). Add the --no-live option if you don't want live rebuilding of your site.
- `yogen deploy`: Push the results of the `build` into a remote repository. 
