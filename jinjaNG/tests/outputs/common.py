#!/usr/bin/env python3

from typing import Tuple, List, Union

from collections import defaultdict

from yaml import safe_load as yaml_load

from cbdevtools.addfindsrc import addfindsrc
from mistool.os_use        import PPath as Path


# ------------- #
# -- MESSAGE -- #
# ------------- #

def message(template, xtra = ""):
    if xtra:
        xtra = f'\n{xtra}'

    dirpb = template.parent

    return (
         "\n"
         "In the source dir, see the folder:"
         "\n"
        f"+ {dirpb}{xtra}"
         "\n"
    )


# ----------- #
# -- OUPUT -- #
# ----------- #

def build_output(
    builder,
    data,
    template
):
    output_found = template.parent / f"output_found{template.suffix}"

    builder.render(
        data     = data,
        template = template,
        output   = output_found
    )

    return output_found


def build_output_strpath(
    builder,
    data,
    template
):
    output_found = template.parent / f"output_found{template.suffix}"

    builder.render(
        data     = str(data),
        template = str(template),
        output   = str(output_found)
    )

    return output_found


def remove_output_found(subdir, template):
    (subdir / f"output_found{template.suffix}").unlink()


# ------------------------ #
# -- NON-STRICT CONTENT -- #
# ------------------------ #

def minimize_content(path):
    return [
        lstripped
        for l in path.read_text(encoding = 'utf-8').split('\n')
        if (lstripped:= l.rstrip())
    ]


# -------------------- #
# -- STRICT CONTENT -- #
# -------------------- #

# Verbatim equivalences of the contents except for the final empty lines that are striped.

def content(path):
    actualcontent = path.read_text(encoding = 'utf-8')

    if actualcontent.startswith('\ufeff'):
        actualcontent = actualcontent[len('\ufeff'):]

    return actualcontent.split('\n')


# -------------------- #
# -- USECASES DATA -- #
# -------------------- #

def yielddirs(pdir: Path) -> Path:
    if not pdir.is_dir():
        raise Exception(
            f"one dir expected, see:\n{pdir}"
        )

    for subdir in pdir.glob('*'):
        if(
            subdir.is_dir()
            and
            not subdir.name.startswith('.')
            and
            not subdir.name.startswith('x-')
        ):
            yield subdir


def extract_dto(pdir: Path) -> Tuple[Union[Path, None], Path, Path]:
    dto = {
        n: []
        for n in ['data', 'template', 'output']
    }

    for pfile in pdir.glob('*'):
        name = pfile.stem

        if name in dto:
            dto[pfile.stem].append(pfile)

    for name, pathsfound in dto.items():
        if len(pathsfound) != 1:
            nbpaths = len(pathsfound)

            howmany = 'no' if nbpaths == 0 else nbpaths
            plural  = ''   if nbpaths == 0 else 's'

            raise Exception(
                f"one mandatory single file can be named ''{name}'': "
                f"{howmany} file{plural} found. Look at the folder:\n{pdir}"
            )

    return tuple(
        p[0]
        for _, p in dto.items()
    )


def build_tests_data(data_dir: Path) -> List[Tuple]:
    tests_data_folders = defaultdict(list)

    for pdir in yielddirs(data_dir):
        kind = pdir.name

        for subdir in yielddirs(pdir):
            tests_data_folders[kind].append(subdir)

    tests_data = []

    for kind, sometests in tests_data_folders.items():
        for subdir in sometests:
            jngdata, template, output = extract_dto(subdir)

            tests_data.append(
                (
                    jngdata,
                    template,
                    output
                )
            )

    return tests_data


# -------------------- #
# -- USECASES DATA -- #
# -------------------- #

def build_docexas_data(
    docexa_yaml : Path
) -> Tuple[Path, List]:
    with docexa_yaml.open(
        encoding = 'utf-8',
        mode     = 'r'
    ) as f:
        docexa_totest = yaml_load(f)

    doc_content_dir = Path(docexa_totest['docdir'])
    docexa_totest   = docexa_totest['totest']

    return doc_content_dir, docexa_totest


# ---------------- #
# -- HOOKS DATA -- #
# ---------------- #

def what_we_want(
    data    : Path,
    template: Path,
    output  : Path
) -> dict:
    kwargs = {
        'data'    : data,
        'template': template,
        'output'  : output,
    }

    for name in list(kwargs.keys()):
        kwargs[f"{name}_stem"] = kwargs[name].parent / kwargs[name].stem


    whatfile = template.parent / 'what-we-want.yaml'

    if not whatfile.is_file():
        return {
            'files': []
        }

    with whatfile.open(
        encoding = 'utf-8',
        mode     = 'r'
    ) as f:
        whatwewant = yaml_load(f)

    if not 'files' in whatwewant:
        whatwewant['files'] = []

    for i, strpath in enumerate(whatwewant['files']):
        whatwewant['files'][i] = strpath.format(**kwargs)

    return whatwewant


def remove_xtra_hooks(whatwewant):
    for p in whatwewant['files']:
        p = Path(p)

        if p.is_file():
            p.unlink()
