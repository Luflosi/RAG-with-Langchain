final: prev: {
  pythonPackagesExtensions = prev.pythonPackagesExtensions ++ [
    (python-final: python-prev: {
      deepeval = python-final.callPackage ./deepeval.nix { };
      ragas = python-final.callPackage ./ragas.nix { };
      stqdm = python-final.callPackage ./stqdm.nix { };
      streamlit-jupyter = python-final.callPackage ./streamlit-jupyter.nix { };
    })
  ];
}
