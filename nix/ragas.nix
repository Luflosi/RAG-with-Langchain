{
  lib,
  pythonOlder,
  buildPythonPackage,
  fetchFromGitHub,
  setuptools-scm,
  numpy,
  datasets,
  tiktoken,
  pydantic,
  nest-asyncio,
  appdirs,
  diskcache,
  typer,
  rich,
  openai,
  tqdm,
  instructor,
  gitpython,
  pillow,
  langchain,
  langchain-core,
  langchain-community,
  langchain-openai,
}:

buildPythonPackage {
  pname = "ragas";
  version = "0.3.2"; # Actually 0.3.2-unstable-2025-08-27 but the package refuses to compile with this version
  pyproject = true;

  disabled = pythonOlder "3.9";

  src = fetchFromGitHub {
    owner = "explodinggradients";
    repo = "ragas";
    rev = "a03d0882bfbd326e97f84a5f87deec0d8b8422d9";
    hash = "sha256-/s7jqTWSi7C6cr1vhKIIOG4ZStL/oytH5HDZZoVTyhI=";
  };

  build-system = [
    setuptools-scm
  ];

  dependencies = [
    numpy
    datasets
    tiktoken
    pydantic
    nest-asyncio
    appdirs
    diskcache
    typer
    rich
    openai
    tqdm
    instructor
    gitpython
    pillow
    langchain
    langchain-core
    langchain-community
    langchain-openai
  ];

  pythonImportsCheck = [ "ragas" ];

  meta = {
    description = "Supercharge Your LLM Application Evaluations";
    homepage = "https://github.com/explodinggradients/ragas";
    license = lib.licenses.asl20;
    maintainers = with lib.maintainers; [ Luflosi ];
  };
}
