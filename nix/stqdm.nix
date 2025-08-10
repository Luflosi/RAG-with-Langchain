{
  lib,
  buildPythonPackage,
  pythonOlder,
  fetchFromGitHub,
  setuptools,
  poetry-core,
  streamlit,
  tqdm,
}:

buildPythonPackage rec {
  pname = "stqdm";
  version = "0.0.5";
  pyproject = true;

  disabled = pythonOlder "3.9";

  src = fetchFromGitHub {
    owner = "Wirg";
    repo = "stqdm";
    tag = "v${version}";
    hash = "sha256-3ws5Naj1QMc4N6AcWvkQ/7+csyX0cxuW6nta+NtE+44=";
  };

  nativeBuildInputs = [
    setuptools
    poetry-core
  ];

  propagatedBuildInputs = [
    tqdm
    streamlit
  ];

  pythonImportsCheck = [
    "stqdm"
  ];

  meta = {
    homepage = "https://github.com/Wirg/stqdm";
    description = "Simplest way to handle a progress bar in streamlit app";
    maintainers = with lib.maintainers; [ Luflosi ];
    license = lib.licenses.asl20;
  };
}
