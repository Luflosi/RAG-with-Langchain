final: prev: {
  pythonPackagesExtensions = prev.pythonPackagesExtensions ++ [
    (python-final: python-prev: {
      ragas = python-final.callPackage ./ragas.nix { };
      stqdm = python-final.callPackage ./stqdm.nix { };
      streamlit-jupyter = python-final.callPackage ./streamlit-jupyter.nix { };
    })
  ];
}
