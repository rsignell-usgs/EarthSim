import os, sys
from setuptools import setup, find_packages

########## autover ##########

def embed_version(basepath, ref='v0.2.2'):
    """
    Autover is purely a build time dependency in all cases (conda and
    pip) except for when you use pip's remote git support [git+url] as
    1) you need a dynamically changing version and 2) the environment
    starts off clean with zero dependencies installed.
    This function acts as a fallback to make Version available until
    PEP518 is commonly supported by pip to express build dependencies.
    """
    import io, zipfile, importlib
    try:    from urllib.request import urlopen
    except: from urllib import urlopen
    try:
        url = 'https://github.com/ioam/autover/archive/{ref}.zip'
        response = urlopen(url.format(ref=ref))
        zf = zipfile.ZipFile(io.BytesIO(response.read()))
        ref = ref[1:] if ref.startswith('v') else ref
        embed_version = zf.read('autover-{ref}/autover/version.py'.format(ref=ref))
        with open(os.path.join(basepath, 'version.py'), 'wb') as f:
            f.write(embed_version)
        return importlib.import_module("version")
    except:
        return None

def get_setup_version(reponame):
    """
    Helper to get the current version from either git describe or the
    .version file (if available).
    """
    import json
    basepath = os.path.split(__file__)[0]
    version_file_path = os.path.join(basepath, reponame, '.version')
    try:
        from param import version
    except:
        version = embed_version(basepath)
    if version is not None:
        return version.Version.setup_version(basepath, reponame, archive_commit="$Format:%h$")
    else:
        print("WARNING: param>=1.6.0 unavailable. If you are installing a package, this warning can safely be ignored. If you are creating a package or otherwise operating in a git repository, you should install param>=1.6.0.")
        return json.load(open(version_file_path, 'r'))['version_string']


########## dependencies ##########

# TODO: need to sort through these
install_requires = [
    'param >= 1.6'
    'fiona',
    'rasterio',
    'gdal',
    'json-rpc',
    'ulmo >=0.8.3.2',
    'pyyaml',
    'matplotlib',
    'click',
    'werkzeug',
    'peewee',
    'geopandas',
    'psutil',
    'pint',
    'pony',
    'scikit-image',
    'go-spatial',
    'jupyter',
    'descartes',
    'gsshapy',
    'cartopy',
    'bokeh',
    'xarray',
    'gssha',
    'datashader',
    'filigree',
    'param',
    'parambokeh',
    'paramnb',
    'numpy',
    # ?
    ### dependencies for pip installed packages
    # for quest
    'stevedore'
]

extras_require = {
    'tests': [
        'nbsmoke',
        #pytest-cov
    ],
    'docs': [
        'nbsite'
    ]
}    

########## metadata for setuptools ##########

setup_args = {}

setup_args.update(dict(
    name='earthsim',
    version=get_setup_version("EarthSim"),
    packages = find_packages(),
    include_package_data=True,
    install_requires = install_requires,
    extras_require = extras_require,
    tests_require = extras_require['tests'],
    python_requires = ">=3.5"
))

if __name__=="__main__":
    setup(**setup_args)
