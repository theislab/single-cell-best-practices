1. **Save the yml content**:

   - Copy the content from the yml tab into a file named `environment.yml`.

2. **Create the environment**:

   - Open a terminal or command prompt.
   - Run the following command:
     ```bash
     conda env create -f environment.yml
     ```

3. **Activate the environment**:

   - After the environment is created, activate it using:
     ```bash
     conda activate <environment_name>
     ```
   - Replace `<environment_name>` with the name specified in the `environment.yml` file. In the yml file it will look like this:
     ```yaml
     name: <environment_name>
     ```

4. **Verify the installation**:
   - Check that the environment was created successfully by running:
     ```bash
     conda env list
     ```
