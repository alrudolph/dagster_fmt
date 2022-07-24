from cgitb import text
from dagster_fmt import run
from pygls import lsp, server

MAX_WORKERS = 5
LSP_SERVER = server.LanguageServer(max_workers=MAX_WORKERS)


#
# SEE: https://github.com/microsoft/vscode-isort
#


@LSP_SERVER.feature(
    lsp.CODE_ACTION,
    lsp.CodeActionOptions(
        code_action_kinds=[
            lsp.CodeActionKind.QuickFix,
        ],
        resolve_provider=True,
    ),
)
def format(server: server.LanguageServer, params: lsp.CodeActionParams):
    text_document = server.workspace.get_document(params.text_document.uri)
    print(text_document)
    run(text_document)

    return [
        lsp.CodeAction(
            title="isort: Fix import sorting and/or formatting",
            kind=lsp.CodeActionKind.QuickFix,
            data=params.text_document.uri,
            edit=None,
            diagnostics=None,
        ),
    ]
