{
  lib,
  buildPythonPackage,
  fetchFromGitHub,
  poetry-core,
  aiohttp,
  anthropic,
  click,
  google-genai,
  grpcio,
  nest-asyncio,
  ollama,
  openai,
  opentelemetry-api,
  opentelemetry-exporter-otlp-proto-grpc,
  opentelemetry-sdk,
  portalocker,
  posthog,
  pyfiglet,
  pytest,
  pytest-asyncio,
  pytest-repeat,
  pytest-rerunfailures,
  pytest-xdist,
  requests,
  rich,
  sentry-sdk,
  setuptools,
  tabulate,
  tenacity,
  tqdm,
  typer,
  wheel,
}:

buildPythonPackage rec {
  pname = "deepeval";
  version = "3.3.5";
  pyproject = true;

  src = fetchFromGitHub {
    owner = "confident-ai";
    repo = "deepeval";
    rev = "v${version}";
    hash = "sha256-I8/ApJpYLeChAGwqP/yGBfuaRM2lXAEjFoiborplrN8=";
  };

  pythonRelaxDeps = [
    "posthog"
    "pytest-rerunfailures"
  ];

  build-system = [
    poetry-core
  ];

  dependencies = [
    aiohttp
    anthropic
    click
    google-genai
    grpcio
    nest-asyncio
    ollama
    openai
    opentelemetry-api
    opentelemetry-exporter-otlp-proto-grpc
    opentelemetry-sdk
    portalocker
    posthog
    pyfiglet
    pytest
    pytest-asyncio
    pytest-repeat
    pytest-rerunfailures
    pytest-xdist
    requests
    rich
    sentry-sdk
    setuptools
    tabulate
    tenacity
    tqdm
    typer
    wheel
  ];

  pythonImportsCheck = [
    "deepeval"
  ];

  meta = {
    description = "The LLM Evaluation Framework";
    homepage = "https://deepeval.com/";
    license = lib.licenses.asl20;
    maintainers = with lib.maintainers; [
      Luflosi
    ];
  };
}
