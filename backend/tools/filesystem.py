from pathlib import Path

IGNORED_DIRECTORIES = {
    "node_modules",
    ".venv",
    "__pycache__",
    ".git",
    "dist",
    "build",
}

IGNORED_FILES = {
    ".env",
}

#================LIST FILES================
def list_files(project_path: str)->list[str]:
   path = Path(project_path)

   if not path.exists():
      raise FileNotFoundError(f"Project path '{project_path}' does not exist.")

   if not path.is_dir():
      raise NotADirectoryError(f"Project path '{project_path}' is not a directory.")

   files = []
   for item in path.rglob("*"):
      if any(
          ignored_dir in item.parts
            for ignored_dir in IGNORED_DIRECTORIES
            ):
         continue

      if item.is_file() and item.name not in IGNORED_FILES:
        files.append(str(item.relative_to(path)))

   return files


#================READ FILE================
def read_file(project_path: str, file_path: str) -> str:
    project = Path(project_path).resolve()
    target_file = (project / file_path).resolve()

    if not project.exists():
        raise FileNotFoundError(f"Project path '{project_path}' does not exist.")

    if not project.is_dir():
         raise NotADirectoryError(f"Project path '{project_path}' is not a directory.")

    if project not in target_file.parents:
        raise PermissionError(
            "Access denied: file is outside the project directory."
        )

    if target_file.name in IGNORED_FILES:
        raise PermissionError(
            f"Access denied: {target_file.name} is a protected file."
        )

    if any(
        ignored_directory in target_file.parts
        for ignored_directory in IGNORED_DIRECTORIES
    ):
        raise PermissionError(
            "Access denied: file is inside an ignored directory."
        )


    if not target_file.exists():
        raise FileNotFoundError(f"File '{file_path}' does not exist.")

    if not target_file.is_file():
        raise ValueError(f"Path '{file_path}' is not a file.")

    return target_file.read_text(encoding="utf-8")


#================SEARCH CODE================
def search_code(project_path: str, query: str) -> list[dict]:
    project = Path(project_path).resolve()

    if not project.exists():
        raise FileNotFoundError(
            f"Project path does not exist: {project_path}"
        )

    if not project.is_dir():
        raise NotADirectoryError(
            f"Project path is not a directory: {project_path}"
        )

    if not query.strip():
        raise ValueError("Search query cannot be empty.")

    results = []

    for file_path in list_files(project_path):
        target_file = (project / file_path).resolve()

        try:
            content = target_file.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        for line_number, line in enumerate(content.splitlines(), start=1):
            if query.lower() in line.lower():
                results.append(
                    {
                        "file": file_path,
                        "line": line_number,
                        "content": line.strip(),
                    }
                )

    return results


if __name__ == "__main__":
   project_path = r"C:\Users\LOQ\OneDrive\Desktop\AgentForge"

   print("====Project Files====")

   files = list_files(project_path)
   for file in files:
      print(file)


   print("\n=====MAIN>PY=====")

   content = read_file(project_path, "backend/main.py")
   print(content)


   #print("\n======SECURITY TESTS======")

   # try:
      # read_file(project_path, "backend/.env")
   # except Exception as e:
       # print(e)


   print("\n===== SEARCH TEST =====")

   results = search_code(
    project_path,
    "FastAPI"
   )

   for result in results:
    print(
        f"{result['file']}:{result['line']} "
        f"-> {result['content']}"
    )