This book uses [lamindb](https://github.com/laminlabs/lamindb) to store, share, and load datasets and notebooks using the [theislab/sc-best-practices instance](https://lamin.ai/theislab/sc-best-practices).
We acknowledge free hosting from [Lamin Labs](https://lamin.ai/).

1. **Install lamindb**
   - Install the lamindb Python package:

   ```bash
   pip install lamindb
   ```

2. **Optionally create a lamin account**
   - Sign up and log in following [the instructions](https://docs.lamin.ai/setup#sign-up-log-in)

3. **Verify your setup**
   - Run the `lamin connect` command:

   ```python
   import lamindb as ln

   ln.Artifact.connect("theislab/sc-best-practices").df()
   ```

   You should now see up to 100 of the stored datasets.

4. **Accessing datasets (Artifacts)**
   - Search for the datasets on the [Artifacts page](https://lamin.ai/theislab/sc-best-practices/artifacts)
   - Load an Artifact and the corresponding object:

   ```python
   import lamindb as ln
   af = ln.Artifact.connect("theislab/sc-best-practices").get(key="key_of_dataset", is_latest=True)
   obj = af.load()
   ```

   The object is now accessible in memory and is ready for analysis.
   Adapt the `ln.Artifact.connect("theislab/sc-best-practices").get("SOMEIDXXXX")` suffix to get respective versions.

5. **Accessing notebooks (Transforms)**
   - Search for the notebook on the [Transforms page](https://lamin.ai/theislab/sc-best-practices/transforms)
   - Load the notebook:

   ```bash
   lamin load <notebook url>
   ```

   which will download the notebook to the current working directory.
   Analogously to `Artifacts`, you can adapt the suffix ID to get older versions.
