echo -e "\n\n*** TEST ***\n\n"
export COVERAGE_PROCESS_START="$(dirname "${SRC_DIR}")/work/.coveragerc"
echo "import coverage; coverage.process_startup()" > "${SP_DIR}/subcov.pth"
mkdir -p "${CONDA_ROOT}/conda-bld/coverage"
rm -rf "${CONDA_ROOT}/conda-bld/coverage/*"
cd ../work \
&& ${PYTHON} setup.py test \
&& cp .coverage.* "${CONDA_ROOT}/conda-bld/coverage"
cd "${CONDA_ROOT}/conda-bld/coverage" && coverage combine && coverage html
