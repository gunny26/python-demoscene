from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import sys

# set profiling globally
#from Cython.Compiler.Options import directive_defaults
#directive_defaults['profile'] = False

# extra compile flags
extra_compile_args = ["-O3"]
#extra_compile_args = []

#sys.argv.append("build_ext")
#sys.argv.append("--inplace")

extensions = [
    Extension("Vector", ["src/Vector.pyx"], extra_compile_args=extra_compile_args),
    Extension("Vector2", ["src/Vector2.pyx"], extra_compile_args=extra_compile_args),
    Extension("Vector3", ["src/Vector3.pyx"], extra_compile_args=extra_compile_args),
    Extension("Vector3h", ["src/Vector3h.pyx"], extra_compile_args=extra_compile_args),
    Extension("Matrix3d", ["src/Matrix3d.pyx"], extra_compile_args=extra_compile_args),
    Extension("Polygon", ["src/Polygon.pyx"], extra_compile_args=extra_compile_args),
    Extension("Utils3d", ["src/Utils3d.pyx"], extra_compile_args=extra_compile_args),
    Extension("Mesh", ["src/Mesh.pyx"], extra_compile_args=extra_compile_args),
]

setup(
    name = "Math3dfx",
    version = "1.0",
    ext_modules = cythonize(extensions), # accepts a glob pattern
)
