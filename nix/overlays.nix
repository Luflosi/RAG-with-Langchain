final: prev: {
  pythonPackagesExtensions = prev.pythonPackagesExtensions ++ [
    (python-final: python-prev: {
      stqdm = python-final.callPackage ./stqdm.nix { };
      streamlit-jupyter = python-final.callPackage ./streamlit-jupyter.nix { };
    })
  ];
}
