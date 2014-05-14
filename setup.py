from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import sys

# set profiling globally
from Cython.Compiler.Options import directive_defaults
directive_defaults['profile'] = False

# extra compile flags
extra_compile_args = ["-O3"]
#extra_compile_args = []

#sys.argv.append("build_ext")
#sys.argv.append("--inplace")

extensions = [
    Extension("Polygon", ["src/Polygon.pyx"], extra_compile_args=extra_compile_args),
    Extension("Utils3d", ["src/Utils3d.pyx"], extra_compile_args=extra_compile_args),
    Extension("Mesh", ["src/Mesh.pyx"], extra_compile_args=extra_compile_args),
    Extension("Plasma", ["src/Plasma.pyx"], extra_compile_args=extra_compile_args),
    Extension("PlasmaPy", ["src/PlasmaPy.py"], extra_compile_args=extra_compile_args),
    Extension("PlasmaFractal", ["src/PlasmaFractal.pyx"], extra_compile_args=extra_compile_args),
    Extension("PlasmaFractal2", ["src/PlasmaFractal2.py"], extra_compile_args=extra_compile_args),
    Extension("Mandelbrot", ["src/Mandelbrot.pyx"], extra_compile_args=extra_compile_args),
    Extension("CoffeeBean", ["src/CoffeeBean.pyx"], extra_compile_args=extra_compile_args),
]

setup(
    name = "python-demoscene",
    version = "1.0",
    ext_modules = cythonize(extensions), # accepts a glob pattern
)
