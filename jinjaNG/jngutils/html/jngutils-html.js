/***
prototype::
    action : the function ''jnghtml'' use a regex like replacement to
             transform a sequence like ''{{ jinja_basic_instr }}'' into
             ''<span style="color: red; ...">jinja_basic_instr</span>''
             where the text ''jinja_basic_instr'' is reproduced verbatim.


ref::
    The initial code comes from cf::''this post ;
                                      https://stackoverflow.com/a/74336061/4589608 ''.
***/
jnghtml = _ =>
    document.body.outerHTML = document.body.outerHTML
// VARIABLES
        .replace(
            /\{\{\s+(.*?)\s+\}\}/g,
              `<span style="color: red; font-weight: bold; `
            + `border: solid 1px; padding: 1px 3px">$1</span>`
        );
