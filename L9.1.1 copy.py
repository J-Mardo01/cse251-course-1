import subprocess

def main():
    subprocess.run(["ls", "-l", "jon.*"],)

if __name__ == "__main__":
    main()