This book uses [lamindb](https://github.com/laminlabs/lamindb) to store, share, and load datasets and notebooks using the [theislab/sc-best-practices instance](https://lamin.ai/theislab/sc-best-practices).
We acknowledge free hosting from [Lamin Labs](https://lamin.ai/).

1. **Install lamindb**

- Install the lamindb Python package:
  ```bash
  pip install lamindb[bionty,jupyter,zarr]
  ```

2. **Optionally create a lamin account**

- Sign up and log in following [the instructions](https://docs.lamin.ai/setup#sign-up-log-in)

3. **Connect to the [theislab/sc-best-practices instance](https://lamin.ai/theislab/sc-best-practices)**

- Run the `lamin connect` command:

  ```bash
  lamin connect theislab/sc-best-practices
  ```

  You should now see `→ connected lamindb: theislab/sc-best-practices`.

4. **Verify your setup**

   - Run the `lamin connect` command:

   ```python
   import lamindb as ln

   ln.Artifact.df()
   ```

   You should now see up to 100 of the stored datasets.

5. **Accessing datasets (Artifacts)**

   - Search for the datasets on the [Artifacts page](https://lamin.ai/theislab/sc-best-practices/artifacts)
   - Load an Artifact and the corresponding object:

   ```python
   import lamindb as ln
   af = ln.Artifact.get(key="key_of_dataset", is_latest=True)
   obj = af.load()
   ```

   The object is now accessible in memory and is ready for analysis.

6. **Accessing notebooks (Transforms)**

   - Search for the notebook on the [Transforms page](https://lamin.ai/theislab/sc-best-practices/transforms)
   - Load the notebook:

   ```bash
   lamin load <notebook url>
   ```

   which will download the notebook to the current working directory.

7. \*\*On `ln.track()` and `ln.finish()`

   - These functions are currently only available for users with write access and may error. Please comment them out for now.
