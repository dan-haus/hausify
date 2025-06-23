# `hausify`
Haus's python linter / formatter + pre-commit tool

Contributions welcome

## Why?
Over the past few years, I've grown weary of managing all the pre-commits and linters/formatters in monorepos that have different settings/preferences for subpackages.

So I wrote a single tool that does the following:

1. Allows for multiple config files for any tool, at multiple places throughout the source hierarchy.  `hausify` will find the configuration file that is closest in the parent directory path and use it for the tool + file combination.  No more attempting to have a one-size-fits-all config for all subdirectories/modules.
2. Manages all of the following tools; all tools can be run at once (suite), or each can be run individually; additionally, tools can be run in 'check' mode (default, and for pre-commits), or in 'fix' mode (for cli-based changes): 
    - Linting / Checking: `flake8`, `mypy`
    - Formatting: `docformatter`, `isort`, `black`
3. A pre-commit single rule (which can now be used as `https://github.com/dan-haus/hausify`).  See this own repo's pre-commit-config tool.
4. Non-interfering formatting.  Isort and Black should never overlap (because, let's face it... sometimes we want different isort/import configs that just don't play nice with black).  This tool calculates which parts of source are imports (from the AST), and excludes those lines from Black's formatting.
5. A vscode extension that replaces all of the above tools with a single LSP: `daniel-walt.hausify`
    - Performs diagnostics on python file open and save
    - Performs on-stop imports+format document formatting for python files

## Installation

`pipx install hausify`

This will install two tools:
1. `hausify`: a tool for checking and/or fixing python source files
2. `hausify-lsp`: a language server that can be used with the corresponding vscode extension `daniel-walt.hausify`

Alternatively, you can create a new virtualenvironment somewhere in your home directory, run a `pip install hausify` with this venv activated, and then either add that virtualenvironment's `/bin` path to your PATH, or link directly to the installed `.../bin/hausify` and `.../bin/hausify-lsp`

## Usage

From your source root (hopefully a git repository), simply run `hausify`.  This will run all tools in "check" mode (outputs the problems encountered by each tool, and exits with a non-zero code if ANY need to be fixed)

### Quick Fix-ing

If you'd like to apply all the changes automatically, `hausify --fix` will run all tools in fix mode, and your files will be updated in-place.

### Tool-based and Further Configs
Examples:
- `hausify --tool black` runs only the black tool
- `hausify --tool black --black-mode fix` runs only the black tool, and runs it in the 'fix' mode
- `hausify --rootdir` runs hausify with a specific root directory (will never search above this directory for files or configs)
- `hausify --exclude_dir .virtualenv/ --exclude_dir .second_virtualenv/` runs the command with additional excluded directories


### How to use the vscode extension:

Instructions to follow; let me know if you'd like to beta the pre-release version (it's publicly available, but might need some help getting it configured the first time)