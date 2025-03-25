# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install veloc-git
#
# You can edit this file again by typing:
#
#     spack edit veloc-git
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *
import shutil
import os

class VelocGit(Package):
    """
        VeloC is a multi-level checkpoint-restart runtime for HPC
        supercomputing infrastructures and large-scale data centers. It
        aims to delivers high performance and scalability for complex
        heterogeneous storage hierarchies without sacrificing ease of use
        and flexibility.
    """

    # url for veloc package
    homepage = "https://veloc.readthedocs.io/en/latest/"
    git = "https://github.com/ECP-VeloC/VELOC.git"

    version('main', branch='main')

    depends_on('python', type='build')
    depends_on('py-pip', type='build')
    depends_on('mpich')

    def install(self, spec, prefix):
        # Remove /tmp/veloc if it exists
        veloc_tmp_dir = '/tmp/veloc'
        if os.path.exists(veloc_tmp_dir):
            shutil.rmtree(veloc_tmp_dir)
        
        git = which('git')
        git('clone', self.git, 'veloc')
        with working_dir('veloc'):
            bash = which('bash')
            bash('./bootstrap.sh')
            pip = which('pip')
            pip('install', 'wget', 'bs4', 'urllib3')
            
            # Set environment variables for MPI
            os.environ['MPICC'] = spec['mpi'].mpicc
            os.environ['MPICXX'] = spec['mpi'].mpicxx
            os.environ['MPIFC'] = spec['mpi'].mpifc
            os.environ['MPI_HOME'] = spec['mpi'].prefix

            # Ensure CMake uses the correct MPI library
            cmake_args = [
                '-DMPI_C_COMPILER={0}'.format(spec['mpi'].mpicc),
                '-DMPI_CXX_COMPILER={0}'.format(spec['mpi'].mpicxx),
                '-DMPI_Fortran_COMPILER={0}'.format(spec['mpi'].mpifc),
                '-DMPI_C_LIBRARIES={0}'.format(spec['mpi'].libs.joined(';')),
                '-DMPI_CXX_LIBRARIES={0}'.format(spec['mpi'].libs.joined(';')),
                '-DMPI_Fortran_LIBRARIES={0}'.format(spec['mpi'].libs.joined(';'))
            ]
            
            python = which('python')
            python('./auto-install.py', prefix)
