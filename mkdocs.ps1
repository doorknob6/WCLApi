
$WCLPath = Join-Path $PSScriptRoot "WCLApi"
$docsPath = Join-Path $PSScriptRoot "docs"
$falseDocsPaths = Join-Path $DocsPath "WCLApi"

pdoc $WCLPath --html --force -o $DocsPath

get-childitem -path $docsPath -filter *.html | remove-item
get-childitem -path $falseDocsPaths -filter *.html | ForEach-Object { copy-item $_.FullName -filter *.html -Destination $docsPath }
remove-item $falseDocsPaths -recurse
