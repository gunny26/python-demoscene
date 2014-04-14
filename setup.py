from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import sys

# set profiling globally
from Cython.Compiler.Options import directive_defaults
directive_defaults['profile'] = False

# extra compile flags
extra_compile_args = ["-O3"]

sys.argv.append("build_ext")
sys.argv.append("--inplace")

extensions = [
    Extension("Vector", ["Vector.pyx"], extra_compile_args=extra_compile_args),
]

setup(
    name = "python-demoscene",
    ext_modules = cythonize(extensions), # accepts a glob pattern
)
